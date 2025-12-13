"use client";

import React, { createContext, useContext, useState, useEffect } from "react";

const DARK_MODE_KEY = "darkMode";

interface DarkModeContextType {
  isDark: boolean;
  toggleDarkMode: () => void;
  mounted: boolean;
}

const DarkModeContext = createContext<DarkModeContextType | undefined>(undefined);

export function DarkModeProvider({ children }: { children: React.ReactNode }) {
  // Initialize state from localStorage lazily
  const [isDark, setIsDark] = useState(() => {
    if (typeof window === "undefined") return false;
    const stored = localStorage.getItem(DARK_MODE_KEY);
    return stored === "true";
  });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
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

  return (
    <DarkModeContext.Provider value={{ isDark, toggleDarkMode, mounted }}>
      {children}
    </DarkModeContext.Provider>
  );
}

export function useDarkMode() {
  const context = useContext(DarkModeContext);
  if (context === undefined) {
    throw new Error("useDarkMode must be used within a DarkModeProvider");
  }
  return context;
}
