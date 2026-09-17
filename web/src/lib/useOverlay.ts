import {
  useCallback,
  useEffect,
  useRef,
  type KeyboardEvent as ReactKeyboardEvent,
  type RefObject,
} from "react";

const FOCUSABLE =
  'a[href], button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), [tabindex]:not([tabindex="-1"])';

export function useOverlay<T extends HTMLElement>({
  open,
  onClose,
  panelRef,
  triggerRef,
  initialFocusRef,
}: {
  open: boolean;
  onClose: () => void;
  panelRef: RefObject<T | null>;
  triggerRef?: RefObject<HTMLElement | null>;
  initialFocusRef?: RefObject<HTMLElement | null>;
}) {
  const openedOnce = useRef(false);

  useEffect(() => {
    if (open) {
      openedOnce.current = true;
      const target =
        initialFocusRef?.current ??
        panelRef.current?.querySelector<HTMLElement>(FOCUSABLE) ??
        null;
      target?.focus();
      return;
    }
    if (openedOnce.current) {
      openedOnce.current = false;
      triggerRef?.current?.focus();
    }
  }, [open, panelRef, triggerRef, initialFocusRef]);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open, onClose]);

  const trapFocus = useCallback(
    (event: ReactKeyboardEvent<HTMLElement>) => {
      if (event.key !== "Tab") return;
      const focusable = panelRef.current?.querySelectorAll<HTMLElement>(FOCUSABLE);
      if (!focusable || focusable.length === 0) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (!first || !last) return;
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    },
    [panelRef],
  );

  return { trapFocus };
}
