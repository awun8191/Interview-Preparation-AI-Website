import { useCallback, useEffect, useState } from "react";

export type Theme = "light" | "dark";

const KEY = "theplan.theme";

function systemTheme(): Theme {
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function storedTheme(): Theme {
  try {
    const value = localStorage.getItem(KEY);
    if (value === "light" || value === "dark") return value;
  } catch {
    /* storage unavailable */
  }
  return systemTheme();
}

export function useTheme() {
  const [theme, setTheme] = useState<Theme>(storedTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      localStorage.setItem(KEY, theme);
    } catch {
      /* storage unavailable */
    }
  }, [theme]);

  const toggle = useCallback(() => {
    setTheme((current) => (current === "dark" ? "light" : "dark"));
  }, []);

  return { theme, setTheme, toggle };
}
