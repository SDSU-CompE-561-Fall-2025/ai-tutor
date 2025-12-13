"use client";

import { useState, useEffect, useLayoutEffect } from "react";

const DARK_MODE_KEY = "darkMode";

export function useDarkMode() {
  // Initialize state from localStorage lazily
  const [isDark, setIsDark] = useState(() => {
    if (typeof window === "undefined") return false;
    const stored = localStorage.getItem(DARK_MODE_KEY);
    return stored === "true";
  });
  const [mounted, setMounted] = useState(false);

  useLayoutEffect(() => {
    setMounted(true);
  }, []);

  // Sync changes to localStorage
  useEffect(() => {
    if (mounted) {
      localStorage.setItem(DARK_MODE_KEY, String(isDark));
    }
  }, [isDark, mounted]);

  const toggleDarkMode = () => {
    setIsDark(!isDark);
  };

  return { isDark, toggleDarkMode, mounted };
}
