"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";

const DARK_MODE_KEY = "darkMode";

interface DarkModeContextType {
  isDark: boolean;
  toggleDarkMode: () => void;
}

const DarkModeContext = createContext<DarkModeContextType | undefined>(undefined);

export function DarkModeProvider({ children }: { children: ReactNode }) {
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

  return (
    <DarkModeContext.Provider value={{ isDark, toggleDarkMode }}>
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
