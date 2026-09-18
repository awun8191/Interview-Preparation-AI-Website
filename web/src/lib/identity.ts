const KEY = "theplan.user_id";

export function getUserId(): string {
  try {
    const existing = localStorage.getItem(KEY);
    if (existing) return existing;
    const id =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : `user-${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
    localStorage.setItem(KEY, id);
    return id;
  } catch {
    return "anonymous";
  }
}
