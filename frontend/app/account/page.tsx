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
import { useDarkMode } from "@/hooks/useDarkMode";

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
        // Fetch user profile
        const userData = await getCurrentUser();
        setUser(userData);

        // Load first and last names from user data
        if (userData.first_name && userData.last_name) {
          setFirstName(userData.first_name);
          setLastName(userData.last_name);
          setOriginalFirstName(userData.first_name);
          setOriginalLastName(userData.last_name);
        } else {
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
    if (!firstName.trim() || !lastName.trim()) {
      setSaveMessage({
        type: "error",
        text: "First and last name cannot be empty",
      });
      return;
    }

    setIsSaving(true);
    setSaveMessage(null);

    try {
      const updatedUser = await updateUserProfile({
        first_name: firstName.trim(),
        last_name: lastName.trim(),
      });
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
      <div
        className={`p-8 flex items-center justify-center min-h-screen ${
          isDark ? "bg-gray-800" : "bg-white"
        }`}
      >
        <div className={isDark ? "text-gray-300" : "text-gray-500"}>
          Loading...
        </div>
      </div>
    );
  }

  return (
    <div
      className={`p-8 max-w-4xl min-h-screen ${
        isDark ? "bg-gray-800 text-white" : "bg-white text-gray-900"
      }`}
    >
      {/* Header */}
      <div className="mb-8">
        <h1
          className={`text-2xl font-bold ${
            isDark ? "text-white" : "text-gray-900"
          }`}
        >
          Account Settings
        </h1>
        <p className={`mt-1 ${isDark ? "text-gray-300" : "text-gray-500"}`}>
          Manage your profile and preferences.
        </p>
      </div>

      {/* Avatar Section */}
      <div className="flex items-center gap-6 mb-8">
        <div className="w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center border-2 border-blue-300 shadow-lg">
          <User className="w-10 h-10 text-white" />
        </div>
        <div>
          <button className="px-4 py-2 border-2 border-blue-300 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg text-sm font-medium text-blue-700 hover:from-blue-100 hover:to-purple-100 transition-all shadow-sm hover:shadow-md">
            Change Avatar
          </button>
          <p className="text-xs text-gray-500 mt-2">
            JPG, GIF or PNG. Max size of 800K
          </p>
        </div>
      </div>

      {/* Profile Form */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <label
            className={`block text-sm font-medium mb-2 ${
              isDark ? "text-gray-200" : "text-gray-700"
            }`}
          >
            First Name
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
              maxLength={25}
              className={`block w-full pl-10 pr-3 py-2.5 border rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:border-transparent ${
                isDark
                  ? "border-gray-600 bg-gray-700 text-white focus:ring-blue-500"
                  : "border-gray-300 bg-white text-gray-900 focus:ring-gray-900"
              }`}
              placeholder="John"
            />
          </div>
        </div>
        <div>
          <label
            className={`block text-sm font-medium mb-2 ${
              isDark ? "text-gray-200" : "text-gray-700"
            }`}
          >
            Last Name
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
              maxLength={25}
              className={`block w-full pl-10 pr-3 py-2.5 border rounded-lg placeholder-gray-500 focus:outline-none focus:ring-2 focus:border-transparent ${
                isDark
                  ? "border-gray-600 bg-gray-700 text-white focus:ring-blue-500"
                  : "border-gray-300 bg-white text-gray-900 focus:ring-gray-900"
              }`}
              placeholder="Doe"
            />
          </div>
        </div>
      </div>

      {/* Email Section */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <label
            className={`block text-sm font-medium mb-2 ${
              isDark ? "text-gray-200" : "text-gray-700"
            }`}
          >
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
                  ? "border-gray-600 bg-gray-700/50 text-gray-300"
                  : "border-gray-300 bg-gray-50 text-gray-900"
              }`}
              placeholder="john@example.com"
            />
          </div>
        </div>
      </div>

      {/* Usage Statistics */}
      <div className="mb-8">
        <h2
          className={`text-lg font-semibold mb-4 ${
            isDark ? "text-white" : "text-gray-900"
          }`}
        >
          Usage Statistics
        </h2>
        <div className="grid grid-cols-3 gap-4">
          <div
            className={`border-2 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow ${
              isDark
                ? "border-blue-500/50 bg-gradient-to-br from-blue-900/30 to-blue-800/20"
                : "border-blue-300 bg-gradient-to-br from-blue-50 to-blue-100"
            }`}
          >
            <p
              className={`text-3xl font-bold ${
                isDark ? "text-blue-400" : "text-blue-600"
              }`}
            >
              {stats.activeClasses}
            </p>
            <p
              className={`text-sm mt-1 font-medium ${
                isDark ? "text-blue-300" : "text-blue-700"
              }`}
            >
              Active Classes
            </p>
          </div>
          <div
            className={`border-2 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow ${
              isDark
                ? "border-purple-500/50 bg-gradient-to-br from-purple-900/30 to-purple-800/20"
                : "border-purple-300 bg-gradient-to-br from-purple-50 to-purple-100"
            }`}
          >
            <p
              className={`text-3xl font-bold ${
                isDark ? "text-purple-400" : "text-purple-600"
              }`}
            >
              {stats.videosGenerated}
            </p>
            <p
              className={`text-sm mt-1 font-medium ${
                isDark ? "text-purple-300" : "text-purple-700"
              }`}
            >
              Videos Generated
            </p>
          </div>
          <div
            className={`border-2 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow ${
              isDark
                ? "border-green-500/50 bg-gradient-to-br from-green-900/30 to-green-800/20"
                : "border-green-300 bg-gradient-to-br from-green-50 to-green-100"
            }`}
          >
            <p
              className={`text-3xl font-bold ${
                isDark ? "text-green-400" : "text-green-600"
              }`}
            >
              {stats.documentsProcessed}
            </p>
            <p
              className={`text-sm mt-1 font-medium ${
                isDark ? "text-green-300" : "text-green-700"
              }`}
            >
              Documents Processed
            </p>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="mb-8">
        <h2
          className={`text-lg font-semibold mb-4 ${
            isDark ? "text-white" : "text-gray-900"
          }`}
        >
          Preferences
        </h2>
        <div
          className={`flex items-center justify-between py-4 border-b ${
            isDark ? "border-gray-700" : "border-gray-200"
          }`}
        >
          <div>
            <p
              className={`font-medium ${
                isDark ? "text-white" : "text-gray-900"
              }`}
            >
              Email Notifications
            </p>
            <p
              className={`text-sm ${
                isDark ? "text-gray-300" : "text-gray-500"
              }`}
            >
              Receive email updates about your account activity
            </p>
          </div>
          <button
            className={`px-4 py-2 border-2 rounded-lg text-sm font-medium transition-all shadow-sm hover:shadow-md ${
              isDark
                ? "border-purple-500/50 bg-gradient-to-r from-purple-900/30 to-pink-900/30 text-purple-300 hover:from-purple-800/40 hover:to-pink-800/40"
                : "border-purple-300 bg-gradient-to-r from-purple-50 to-pink-50 text-purple-700 hover:from-purple-100 hover:to-pink-100"
            }`}
          >
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
              ? "bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 hover:shadow-lg"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          {isSaving ? "Saving..." : "Save Changes"}
        </button>
      </div>
    </div>
  );
}
