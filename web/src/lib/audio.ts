export const MAX_RECORD_SECONDS = 180;

const CANDIDATE_MIMES = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4", "audio/wav"];

export function pickMimeType(): string {
  if (typeof MediaRecorder === "undefined") return "";
  for (const mime of CANDIDATE_MIMES) {
    try {
      if (MediaRecorder.isTypeSupported(mime)) return mime;
    } catch {
      // ignore and try next
    }
  }
  return "";
}

export interface Recorder {
  stop: () => Promise<Blob>;
  cancel: () => void;
}

export async function startRecording(): Promise<{ recorder: Recorder; stream: MediaStream; mimeType: string }> {
  if (!navigator.mediaDevices?.getUserMedia) {
    throw new Error("Microphone is not available in this browser.");
  }
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  const mimeType = pickMimeType();
  const rec = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
  const chunks: BlobPart[] = [];
  const done = new Promise<Blob>((resolve, reject) => {
    rec.ondataavailable = (e) => {
      if (e.data && e.data.size > 0) chunks.push(e.data);
    };
    rec.onerror = () => reject(new Error("Recording failed."));
    rec.onstop = () => {
      stream.getTracks().forEach((t) => t.stop());
      resolve(new Blob(chunks, { type: mimeType || rec.mimeType || "audio/webm" }));
    };
  });
  let settled = false;
  const timer = window.setTimeout(() => {
    if (!settled && rec.state !== "inactive") rec.stop();
  }, MAX_RECORD_SECONDS * 1000);
  rec.start(250);
  return {
    recorder: {
      stop: () => {
        settled = true;
        window.clearTimeout(timer);
        if (rec.state === "inactive") return done;
        rec.stop();
        return done;
      },
      cancel: () => {
        settled = true;
        window.clearTimeout(timer);
        if (rec.state !== "inactive") rec.stop();
        stream.getTracks().forEach((t) => t.stop());
      },
    },
    stream,
    mimeType: mimeType || rec.mimeType,
  };
}
