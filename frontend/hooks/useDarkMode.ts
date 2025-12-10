"use client";

import { useState, useEffect } from "react";

const DARK_MODE_KEY = "darkMode";

export function useDarkMode() {
  const [isDark, setIsDark] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem(DARK_MODE_KEY);
    if (stored !== null) {
      setIsDark(stored === "true");
    }
  }, []);

  const toggleDarkMode = () => {
    const newValue = !isDark;
    setIsDark(newValue);
    localStorage.setItem(DARK_MODE_KEY, String(newValue));
  };

  return { isDark, toggleDarkMode, mounted };
}
