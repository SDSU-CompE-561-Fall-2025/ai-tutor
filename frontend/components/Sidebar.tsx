"use client";

import React, { useEffect, useState } from "react";
import { BookOpen, Video, User, LogOut } from "lucide-react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { getCurrentUser, clearAuthTokens, ApiError } from "@/lib/api";

interface NavItem {
  label: string;
  icon: React.ReactNode;
  href: string;
}

interface UserData {
  email: string;
  first_name?: string;
  last_name?: string;
}

const NAV_ITEMS: NavItem[] = [
  {
    label: "Classes",
    icon: <BookOpen className="w-5 h-5" />,
    href: "/dashboard",
  },
  {
    label: "Videos",
    icon: <Video className="w-5 h-5" />,
    href: "/videos",
  },
  {
    label: "Account",
    icon: <User className="w-5 h-5" />,
    href: "/account",
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<UserData | null>(null);
  const [displayName, setDisplayName] = useState<string | null>(null);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const userData = await getCurrentUser();
        setUser({
          email: userData.email,
        });
        // Build display name from first and last name
        if (userData.first_name && userData.last_name) {
          setDisplayName(`${userData.first_name} ${userData.last_name}`);
        } else {
          const emailName = userData.email.split("@")[0];
          const formattedName = emailName
            .split(/[._-]/)
            .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
          setDisplayName(formattedName);
        }
      } catch (err) {
        if (err instanceof ApiError && err.status === 401) {
          clearAuthTokens();
        }
      }
    };
    loadUser();
  }, []);

  const handleLogout = async () => {
    clearAuthTokens();
    router.push("/");
  };

  // Get user initials for avatar
  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <div className="w-64 bg-white border-r border-gray-200 flex flex-col h-screen fixed left-0 top-0">
      {/* Logo section */}
      <div className="flex items-center gap-2 px-6 py-6 border-b border-gray-200">
        <div className="flex items-center justify-center w-8 h-8 bg-gray-900 rounded-lg">
          <BookOpen className="w-5 h-5 text-white" />
        </div>
        <span className="text-xl font-bold text-gray-900">AI Tutor</span>
      </div>

      {/* Navigation items */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {NAV_ITEMS.map((item) => {
          const isActive =
            pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link key={item.href} href={item.href}>
              <div
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? "bg-gray-100 text-gray-900 font-medium"
                    : "text-gray-600 hover:bg-gray-50"
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </div>
            </Link>
          );
        })}
      </nav>

      {/* User profile section */}
      <div className="flex items-center gap-3 px-2">
        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
          <span className="text-sm font-semibold text-white">
            {displayName ? getInitials(displayName) : "U"}
          </span>
        </div>

        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 truncate">
            {displayName || "User"}
          </p>
          <p className="text-xs text-gray-500 truncate">
            {user?.email || "Loading..."}
          </p>
        </div>
      </div>

      {/* Logout button */}
      <button
        onClick={handleLogout}
        className="w-full flex items-center justify-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors border border-gray-200"
      >
        <LogOut className="w-4 h-4" />
        <span>Logout</span>
      </button>
    </div>
  );
}
