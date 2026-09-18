import { ApiError } from "../lib/types";

export function ErrorBanner({
  error,
  onRetry,
  onDismiss,
}: {
  error: Error;
  onRetry?: () => void;
  onDismiss: () => void;
}) {
  const api = error instanceof ApiError ? error : null;
  const retryable = api?.retryable ?? false;

  return (
    <div className="notice" role="alert">
      <div>
        <strong>{api ? api.code.replaceAll("_", " ") : "Error"}</strong>
        <p>{error.message}</p>
        {api?.requestId && <span className="notice-meta">request {api.requestId}</span>}
      </div>
      <div className="notice-actions">
        {retryable && onRetry && (
          <button className="btn btn--ghost" onClick={onRetry}>
            Retry
          </button>
        )}
        <button className="btn btn--bare" onClick={onDismiss} aria-label="Dismiss error">
          ✕
        </button>
      </div>
    </div>
  );
}
