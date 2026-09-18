import { useEffect, useState, type MouseEvent } from "react";
import { FRAMEWORKS, type Framework } from "./types";

export type Route = "/" | "/practice";

function readPath(): Route {
  const path = window.location.pathname.replace(/\/+$/, "");
  return path === "/practice" ? "/practice" : "/";
}

function readFramework(): Framework | null {
  const value = new URLSearchParams(window.location.search).get("framework");
  if (!value) return null;
  return FRAMEWORKS.some((f) => f.id === value) ? (value as Framework) : null;
}

export function useRoute(): { route: Route; framework: Framework | null } {
  const [location, setLocation] = useState(() => ({
    route: readPath(),
    framework: readFramework(),
  }));

  useEffect(() => {
    const sync = () => setLocation({ route: readPath(), framework: readFramework() });
    window.addEventListener("popstate", sync);
    return () => window.removeEventListener("popstate", sync);
  }, []);

  return location;
}

export function navigate(to: string) {
  const current = `${window.location.pathname}${window.location.search}`;
  if (current === to) return;
  window.history.pushState({}, "", to);
  window.dispatchEvent(new PopStateEvent("popstate"));
  window.scrollTo(0, 0);
}

export function linkProps(to: string) {
  return {
    href: to,
    onClick: (event: MouseEvent<HTMLAnchorElement>) => {
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      navigate(to);
    },
  };
}
