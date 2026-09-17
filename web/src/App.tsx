import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type CSSProperties,
} from "react";
import "./index.css";
import { Landing } from "./components/Landing";
import { PracticeWorkspace } from "./components/PracticeWorkspace";
import { linkProps, useRoute } from "./lib/router";
import { useTheme } from "./lib/theme";
import { useOverlay } from "./lib/useOverlay";

const MENU_BREAKPOINT = 620;

function ThemeToggle({ theme, onToggle }: { theme: string; onToggle: () => void }) {
  return (
    <div className="seg seg--compact" role="group" aria-label="Colour theme">
      <button
        type="button"
        aria-pressed={theme === "light"}
        onClick={() => theme !== "light" && onToggle()}
      >
        Light
      </button>
      <button
        type="button"
        aria-pressed={theme === "dark"}
        onClick={() => theme !== "dark" && onToggle()}
      >
        Dark
      </button>
    </div>
  );
}

export function App() {
  const { route, framework } = useRoute();
  const { theme, toggle } = useTheme();
  const [menuOpen, setMenuOpen] = useState(false);
  const menuButtonRef = useRef<HTMLButtonElement>(null);
  const closeButtonRef = useRef<HTMLButtonElement>(null);
  const drawerRef = useRef<HTMLDivElement>(null);

  const closeMenu = useCallback(() => setMenuOpen(false), []);

  const { trapFocus } = useOverlay<HTMLDivElement>({
    open: menuOpen,
    onClose: closeMenu,
    panelRef: drawerRef,
    triggerRef: menuButtonRef,
    initialFocusRef: closeButtonRef,
  });

  useEffect(() => {
    closeMenu();
  }, [route, closeMenu]);

  useEffect(() => {
    const onResize = () => {
      if (window.innerWidth > MENU_BREAKPOINT) setMenuOpen(false);
    };
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  return (
    <div className="app">
      <header className="masthead">
        <a className="wordmark" {...linkProps("/")}>
          The Plan
        </a>

        <div className="masthead-nav">
          <ThemeToggle theme={theme} onToggle={toggle} />
          {route === "/" ? (
            <a className="btn btn--ghost" {...linkProps("/practice")}>
              Start practising
            </a>
          ) : (
            <a className="btn btn--bare" {...linkProps("/")}>
              Overview
            </a>
          )}
        </div>

        <button
          type="button"
          className="menu-toggle"
          ref={menuButtonRef}
          aria-label="Open menu"
          aria-expanded={menuOpen}
          aria-controls="site-menu"
          onClick={() => setMenuOpen(true)}
        >
          <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
            <path
              d="M3 9h18M3 15h18"
              fill="none"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
        </button>
      </header>

      <div
        id="site-menu"
        className="drawer"
        data-open={menuOpen}
        inert={!menuOpen}
        role="dialog"
        aria-modal="true"
        aria-label="Site menu"
        ref={drawerRef}
        onKeyDown={trapFocus}
      >
        <div className="drawer-top">
          <button
            type="button"
            className="drawer-close"
            ref={closeButtonRef}
            aria-label="Close menu"
            onClick={closeMenu}
          >
            <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
              <path
                d="M6 6l12 12M18 6L6 18"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
              />
            </svg>
          </button>
          <span className="wordmark">The Plan</span>
        </div>

        <nav className="drawer-nav">
          <a className="drawer-link" style={{ "--i": 0 } as CSSProperties} {...linkProps("/")}>
            <span className="drawer-link-label">Overview</span>
            <span className="drawer-link-note">What this is, and the eleven methodologies</span>
          </a>
          <a
            className="drawer-link"
            style={{ "--i": 1 } as CSSProperties}
            {...linkProps("/practice")}
          >
            <span className="drawer-link-label">Start practising</span>
            <span className="drawer-link-note">Pick a framework and deliver an answer</span>
          </a>
        </nav>

        <div className="drawer-foot">
          <span className="smallcaps">Theme</span>
          <ThemeToggle theme={theme} onToggle={toggle} />
        </div>
      </div>

      {route === "/" ? (
        <Landing />
      ) : (
        <PracticeWorkspace key={framework ?? "default"} initialFramework={framework} />
      )}

      <footer className="footer">
        <span>The Plan — executive communication practice</span>
      </footer>
    </div>
  );
}

export default App;
