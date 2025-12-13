"use client";

import Sidebar from "@/components/Sidebar";
import ".././globals.css";
import { useDarkMode } from "@/contexts/DarkModeContext";

export default function AccountLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { isDark } = useDarkMode();
  
  return (
    <div className={`flex ${isDark ? "bg-gray-800" : ""}`}>
      <Sidebar />
      <div className="flex-1 ml-64">{children}</div>
    </div>
  );
}
