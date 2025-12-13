"use client";

import React, { useEffect, useState } from "react";
import { User, Mail } from "lucide-react";
import {
  getCurrentUser,
  getCourses,
  listMyVideos,
  getAllFiles,
  updateUserProfile,
  ApiError,
  clearAuthTokens,
} from "@/lib/api";
import { useRouter } from "next/navigation";
import { useDarkMode } from "@/contexts/DarkModeContext";

interface UserData {
  id: number;
  email: string;
  first_name?: string | null;
  last_name?: string | null;
}

interface UsageStats {
  activeClasses: number;
  videosGenerated: number;
  documentsProcessed: number;
}

export default function AccountPage() {
  const router = useRouter();
  const { isDark } = useDarkMode();
  const { isDark } = useDarkMode();
  const [user, setUser] = useState<UserData | null>(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [originalFirstName, setOriginalFirstName] = useState("");
  const [originalLastName, setOriginalLastName] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{
    type: "success" | "error";
    text: string;
  } | null>(null);
  const [stats, setStats] = useState<UsageStats>({
    activeClasses: 0,
    videosGenerated: 0,
    documentsProcessed: 0,
  });

  useEffect(() => {
    const loadUserData = async () => {
      try {
        // Fetch user profile from backend
        const userData = await getCurrentUser();
        setUser(userData);

        // Load first and last names from user data
        if (userData.first_name && userData.last_name) {
          setFirstName(userData.first_name);
          setLastName(userData.last_name);
          setOriginalFirstName(userData.first_name);
          setOriginalLastName(userData.last_name);
        } else {
          // If no names set in database, derive from email
          const emailName = userData.email.split("@")[0];
          const formattedName = emailName
            .split(/[._-]/)
            .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
          const nameParts = formattedName.split(" ");
          setFirstName(nameParts[0] || "");
          setLastName(nameParts.slice(1).join(" ") || "");
          setOriginalFirstName("");
          setOriginalLastName("");
        }

        // Fetch usage statistics
        const [courses, videosResponse, files] = await Promise.all([
          getCourses(),
          listMyVideos(),
          getAllFiles(),
        ]);

        setStats({
          activeClasses: courses.length,
          videosGenerated: videosResponse.videos?.length || 0,
          documentsProcessed: files.length,
        });
      } catch (err) {
        // Handle auth errors
        if (err instanceof ApiError && err.status === 401) {
          clearAuthTokens();
          router.push("/login");
        }
      } finally {
        setIsLoading(false);
      }
    };
    loadUserData();
  }, [router]);

  const handleSaveChanges = async () => {
    // Validate inputs (names aren't empty)
    if (!firstName.trim() || !lastName.trim()) {
      setSaveMessage({ type: "error", text: "First and last name cannot be empty" });
      return;
    }

    // Validate input length
    if (firstName.length > 15) {
      setSaveMessage({ type: "error", text: "First name must be 15 characters or less" });
      return;
    }

    if (lastName.length > 15) {
      setSaveMessage({ type: "error", text: "Last name must be 15 characters or less" });
      return;
    }

    setIsSaving(true);
    setSaveMessage(null);

    try {
      // Send updated user info to backend
      const updatedUser = await updateUserProfile({ 
        first_name: firstName.trim(), 
        last_name: lastName.trim()
      });

      // Update local state with new user info
      setUser(updatedUser);
      setOriginalFirstName(firstName.trim());
      setOriginalLastName(lastName.trim());
      setSaveMessage({ type: "success", text: "Changes saved successfully!" });

      // Clear success message after 3 seconds
      setTimeout(() => setSaveMessage(null), 3000);
    } catch (err) {
      if (err instanceof ApiError) {
        setSaveMessage({ type: "error", text: err.message });
      } else {
        setSaveMessage({ type: "error", text: "Failed to save changes" });
      }
    } finally {
      setIsSaving(false);
    }
  };

  const hasChanges =
    firstName.trim() !== originalFirstName ||
    lastName.trim() !== originalLastName;

  if (isLoading) {
    return (
      <div className={`p-8 flex items-center justify-center min-h-screen ${
        isDark ? "bg-gray-800" : ""
      }`}>
        <div className={isDark ? "text-gray-400" : "text-gray-500"}>
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div className={`p-8 max-w-4xl ${
      isDark ? "bg-gray-800 text-white min-h-screen" : ""
    }`}>
      {/* Header */}
      <div className="mb-8">
        <h1 className={`text-2xl font-bold ${
          isDark ? "text-white" : "text-gray-900"
        }`}>
          Account Settings
        </h1>
        <p className={isDark ? "text-gray-400" : "text-gray-500"}>
          Manage your profile and preferences.
        </p>
      </div>

      {/* Avatar Section */}
      <div className="flex items-center gap-6 mb-8">
        <div className={`w-20 h-20 rounded-full flex items-center justify-center border ${
          isDark
            ? "bg-gray-700 border-gray-600"
            : "bg-gray-100 border-gray-200"
        }`}>
          <User className={`w-10 h-10 ${
            isDark ? "text-gray-400" : "text-gray-400"
          }`} />
        </div>
        <div>
          <button className={`px-4 py-2 border rounded-lg text-sm font-medium transition-colors ${
            isDark
              ? "border-gray-600 text-gray-300 hover:bg-gray-700"
              : "border-gray-300 text-gray-700 hover:bg-gray-50"
          }`}>
            Change Avatar
          </button>
          <p className={`text-xs mt-2 ${
            isDark ? "text-gray-500" : "text-gray-500"
          }`}>
            JPG, GIF or PNG. Max size of 800K
          </p>
        </div>
      </div>

      {/* Profile Form */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <label className={`block text-sm font-medium mb-2 ${
            isDark ? "text-gray-300" : "text-gray-700"
          }`}>
            First Name
            <span className="text-xs text-gray-500 ml-2">({firstName.length}/15)</span>
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User
                className={`h-5 w-5 ${
                  isDark ? "text-gray-400" : "text-gray-400"
                }`}
              />
            </div>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              maxLength={15}
              className={`block w-full pl-10 pr-3 py-2.5 border rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent ${
                isDark
                  ? "border-gray-600 bg-gray-700 text-white"
                  : "border-gray-300 text-gray-900"
              }`}
              placeholder="John"
            />
          </div>
        </div>
        <div>
          <label className={`block text-sm font-medium mb-2 ${
            isDark ? "text-gray-300" : "text-gray-700"
          }`}>
            Last Name
            <span className="text-xs text-gray-500 ml-2">({lastName.length}/15)</span>
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User
                className={`h-5 w-5 ${
                  isDark ? "text-gray-400" : "text-gray-400"
                }`}
              />
            </div>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              maxLength={15}
              className={`block w-full pl-10 pr-3 py-2.5 border rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent ${
                isDark
                  ? "border-gray-600 bg-gray-700 text-white"
                  : "border-gray-300 text-gray-900"
              }`}
              placeholder="Doe"
            />
          </div>
        </div>
      </div>

      {/* Email Section */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <label className={`block text-sm font-medium mb-2 ${
            isDark ? "text-gray-300" : "text-gray-700"
          }`}>
            Email Address
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="email"
              value={user?.email || ""}
              readOnly
              className={`block w-full pl-10 pr-3 py-2.5 border rounded-lg cursor-not-allowed ${
                isDark
                  ? "border-gray-600 bg-gray-600 text-gray-300"
                  : "border-gray-300 bg-gray-50 text-gray-900"
              }`}
              placeholder="john@example.com"
            />
          </div>
        </div>
      </div>

      {/* Usage Statistics */}
      <div className="mb-8">
        <h2 className={`text-lg font-semibold mb-4 ${
          isDark ? "text-white" : "text-gray-900"
        }`}>
          Usage Statistics
        </h2>
        <div className="grid grid-cols-3 gap-4">
          <div className={`border rounded-xl p-6 ${
            isDark ? "border-gray-600 bg-gray-700" : "border-gray-200"
          }`}>
            <p className={`text-3xl font-bold ${
              isDark ? "text-white" : "text-gray-900"
            }`}>
              {stats.activeClasses}
            </p>
            <p className="text-sm text-gray-500 mt-1">Active Classes</p>
          </div>
          <div className={`border rounded-xl p-6 ${
            isDark ? "border-gray-600 bg-gray-700" : "border-gray-200"
          }`}>
            <p className={`text-3xl font-bold ${
              isDark ? "text-white" : "text-gray-900"
            }`}>
              {stats.videosGenerated}
            </p>
            <p className="text-sm text-gray-500 mt-1">Videos Generated</p>
          </div>
          <div className={`border rounded-xl p-6 ${
            isDark ? "border-gray-600 bg-gray-700" : "border-gray-200"
          }`}>
            <p className={`text-3xl font-bold ${
              isDark ? "text-white" : "text-gray-900"
            }`}>
              {stats.documentsProcessed}
            </p>
            <p className="text-sm text-gray-500 mt-1">Documents Processed</p>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="mb-8">
        <h2 className={`text-lg font-semibold mb-4 ${
          isDark ? "text-white" : "text-gray-900"
        }`}>
          Preferences
        </h2>
        <div className={`flex items-center justify-between py-4 border-b ${
          isDark ? "border-gray-600" : "border-gray-200"
        }`}>
          <div>
            <p className={`font-medium ${
              isDark ? "text-white" : "text-gray-900"
            }`}>
              Email Notifications
            </p>
            <p className="text-sm text-gray-500">
              Receive email updates about your account activity
            </p>
          </div>
          <button className={`px-4 py-2 border rounded-lg text-sm font-medium transition-colors ${
            isDark
              ? "border-gray-600 text-gray-300 hover:bg-gray-700"
              : "border-gray-300 text-gray-700 hover:bg-gray-50"
          }`}>
            Configure
          </button>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex items-center justify-end gap-4">
        {saveMessage && (
          <p
            className={`text-sm ${
              saveMessage.type === "success"
                ? isDark
                  ? "text-green-400"
                  : "text-green-600"
                : isDark
                ? "text-red-400"
                : "text-red-600"
            }`}
          >
            {saveMessage.text}
          </p>
        )}
        <button
          onClick={handleSaveChanges}
          disabled={isSaving || !hasChanges}
          className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all shadow-md ${
            hasChanges && !isSaving
              ? isDark
                ? "bg-blue-600 text-white hover:bg-blue-700"
                : "bg-gray-900 text-white hover:bg-gray-800"
              : isDark
              ? "bg-gray-700 text-gray-500 cursor-not-allowed"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          {isSaving ? "Saving..." : "Save Changes"}
        </button>
      </div>
    </div>
  );
}
