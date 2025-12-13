"use client";

import { useState, useEffect } from "react";

const DARK_MODE_KEY = "darkMode";

export function useDarkMode() {
  // Initialize state from localStorage lazily
  const [isDark, setIsDark] = useState(() => {
    if (typeof window === "undefined") return false;
    const stored = localStorage.getItem(DARK_MODE_KEY);
    return stored === "true";
  });

  // Sync changes to localStorage (only on client side)
  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem(DARK_MODE_KEY, String(isDark));
    }
  }, [isDark]);

  const toggleDarkMode = () => {
    setIsDark(!isDark);
  };

  return { isDark, toggleDarkMode };
}
