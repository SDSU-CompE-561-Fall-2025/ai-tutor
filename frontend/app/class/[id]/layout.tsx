import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../.././globals.css";
import Sidebar from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "Ai Tutor",
  description: "Your personal AI-powered tutor for learning and growth.",
  icons: {
    icon: "/logo.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex">
      <Sidebar />
      <div className="flex-1 ml-64">{children}</div>
    </div>
  );
}
