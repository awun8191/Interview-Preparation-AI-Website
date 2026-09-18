"""Firebase Firestore persistence gateway for project theplan-9311e."""

import asyncio
import json
import logging
import os
import uuid
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1 import Query

from app.core.config import Settings, get_settings
from app.core.errors import FirestoreError
from app.models.session import SessionRecord, UserRecord

logger = logging.getLogger(__name__)


def get_firestore_client(settings: Settings) -> FirestoreClient:
    """Initialize firebase_admin app and return a Firestore client instance."""
    project_id = settings.FIREBASE_PROJECT_ID or "theplan-9311e"
    emulator_host = settings.FIRESTORE_EMULATOR_HOST or os.environ.get("FIRESTORE_EMULATOR_HOST")

    if not firebase_admin._apps:
        try:
            if emulator_host:
                logger.info("Initializing Firebase Admin with Emulator: %s", emulator_host)
                firebase_admin.initialize_app(options={"projectId": project_id})
            elif raw_json := os.environ.get("FIREBASE_CREDENTIALS_JSON"):
                cred_dict = json.loads(raw_json)
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred, options={"projectId": project_id})
            elif cred_path := (
                settings.FIREBASE_CREDENTIALS_PATH
                or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
            ):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, options={"projectId": project_id})
            else:
                # Default Application Default Credentials on GCP
                cred = credentials.ApplicationDefault()
                firebase_admin.initialize_app(cred, options={"projectId": project_id})
        except Exception as exc:
            logger.warning("Firebase Admin initialization with credentials failed: %s", exc)
            # Try initializing without explicit creds (e.g. emulator or ADC fallback)
            try:
                firebase_admin.initialize_app(options={"projectId": project_id})
            except Exception as inner_exc:
                logger.error("Unable to initialize Firebase Admin app: %s", inner_exc)
                raise FirestoreError(
                    message=f"Failed to initialize Firebase Admin: {inner_exc}",
                ) from inner_exc

    return firestore.client()


class FirestoreGateway:
    """Gateway for reading and writing user and session documents in Cloud Firestore."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: Any | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._client = client

    @property
    def client(self) -> FirestoreClient:
        if self._client is None:
            self._client = get_firestore_client(self.settings)
        return self._client

    async def save_user(self, user: UserRecord) -> None:
        """Upsert a user record in the users collection."""
        try:
            user_dict = user.model_dump(mode="json")
            doc_ref = self.client.collection("users").document(user.user_id)
            await asyncio.to_thread(doc_ref.set, user_dict, merge=True)
        except Exception as exc:
            logger.error("Error saving user %s: %s", user.user_id, exc)
            raise FirestoreError(
                message=f"Failed to save user to Firestore: {exc}",
                details={"user_id": user.user_id},
            ) from exc

    async def get_user(self, user_id: str) -> UserRecord | None:
        """Retrieve a user record by user_id."""
        try:
            doc_ref = self.client.collection("users").document(user_id)
            doc = await asyncio.to_thread(doc_ref.get)
            if not doc.exists:
                return None
            data = doc.to_dict() or {}
            return UserRecord(**data)
        except Exception as exc:
            logger.error("Error retrieving user %s: %s", user_id, exc)
            raise FirestoreError(
                message=f"Failed to get user from Firestore: {exc}",
                details={"user_id": user_id},
            ) from exc

    async def save_session(self, session: SessionRecord) -> str:
        """Persist an evaluation session and return the session_id."""
        try:
            session_id = session.session_id or str(uuid.uuid4())
            session_dict = session.model_dump(mode="json")
            session_dict["session_id"] = session_id

            doc_ref = self.client.collection("sessions").document(session_id)
            await asyncio.to_thread(doc_ref.set, session_dict)
            return session_id
        except Exception as exc:
            logger.error("Error saving session %s: %s", session.session_id, exc)
            raise FirestoreError(
                message=f"Failed to save session to Firestore: {exc}",
                details={"session_id": session.session_id},
            ) from exc

    async def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20,
        cursor: str | None = None,
    ) -> list[SessionRecord]:
        """Query user sessions ordered by created_at descending with pagination."""
        try:
            query = (
                self.client.collection("sessions")
                .where("user_id", "==", user_id)
                .order_by("created_at", direction=Query.DESCENDING)
            )

            if cursor:
                cursor_doc = await asyncio.to_thread(
                    self.client.collection("sessions").document(cursor).get
                )
                if cursor_doc.exists:
                    query = query.start_after(cursor_doc)

            query = query.limit(limit)
            docs = await asyncio.to_thread(lambda: list(query.stream()))

            results: list[SessionRecord] = []
            for doc in docs:
                data = doc.to_dict()
                if data:
                    results.append(SessionRecord(**data))

            return results
        except Exception as exc:
            logger.error("Error querying sessions for user %s: %s", user_id, exc)
            raise FirestoreError(
                message=f"Failed to query user sessions from Firestore: {exc}",
                details={"user_id": user_id},
            ) from exc
