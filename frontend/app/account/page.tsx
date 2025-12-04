"use client";

import React, { useEffect, useState } from "react";
import { User, Mail } from "lucide-react";
import { getCurrentUser, getCourses, listMyVideos, getAllFiles, updateUserProfile, ApiError, clearAuthTokens } from "@/lib/api";
import { useRouter } from "next/navigation";

interface UserData {
  id: number;
  email: string;
  name?: string | null;
}

interface UsageStats {
  activeClasses: number;
  videosGenerated: number;
  documentsProcessed: number;
}

export default function AccountPage() {
  const router = useRouter();
  const [user, setUser] = useState<UserData | null>(null);
  const [fullName, setFullName] = useState("");
  const [originalName, setOriginalName] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
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
        
        // Use saved name or generate from email
        if (userData.name) {
          setFullName(userData.name);
          setOriginalName(userData.name);
        } else {
          const emailName = userData.email.split("@")[0];
          const formattedName = emailName
            .split(/[._-]/)
            .map((word: string) => word.charAt(0).toUpperCase() + word.slice(1))
            .join(" ");
          setFullName(formattedName);
          setOriginalName("");
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
    if (!fullName.trim()) {
      setSaveMessage({ type: "error", text: "Name cannot be empty" });
      return;
    }

    setIsSaving(true);
    setSaveMessage(null);

    try {
      const updatedUser = await updateUserProfile({ name: fullName.trim() });
      setUser(updatedUser);
      setOriginalName(fullName.trim());
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

  const hasChanges = fullName.trim() !== originalName;

  if (isLoading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-4xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Account Settings</h1>
        <p className="text-gray-500 mt-1">Manage your profile and preferences.</p>
      </div>

      {/* Avatar Section */}
      <div className="flex items-center gap-6 mb-8">
        <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center border border-gray-200">
          <User className="w-10 h-10 text-gray-400" />
        </div>
        <div>
          <button className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
            Change Avatar
          </button>
          <p className="text-xs text-gray-500 mt-2">JPG, GIF or PNG. Max size of 800K</p>
        </div>
      </div>

      {/* Profile Form */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Full Name
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <User className="h-5 w-5 text-gray-400" />
            </div>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:border-transparent"
              placeholder="John Doe"
            />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
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
              className="block w-full pl-10 pr-3 py-2.5 border border-gray-300 rounded-lg text-gray-900 bg-gray-50 cursor-not-allowed"
              placeholder="john@example.com"
            />
          </div>
        </div>
      </div>

      {/* Usage Statistics */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Usage Statistics</h2>
        <div className="grid grid-cols-3 gap-4">
          <div className="border border-gray-200 rounded-xl p-6">
            <p className="text-3xl font-bold text-gray-900">{stats.activeClasses}</p>
            <p className="text-sm text-gray-500 mt-1">Active Classes</p>
          </div>
          <div className="border border-gray-200 rounded-xl p-6">
            <p className="text-3xl font-bold text-gray-900">{stats.videosGenerated}</p>
            <p className="text-sm text-gray-500 mt-1">Videos Generated</p>
          </div>
          <div className="border border-gray-200 rounded-xl p-6">
            <p className="text-3xl font-bold text-gray-900">{stats.documentsProcessed}</p>
            <p className="text-sm text-gray-500 mt-1">Documents Processed</p>
          </div>
        </div>
      </div>

      {/* Preferences */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Preferences</h2>
        <div className="flex items-center justify-between py-4 border-b border-gray-200">
          <div>
            <p className="font-medium text-gray-900">Email Notifications</p>
            <p className="text-sm text-gray-500">Receive email updates about your account activity</p>
          </div>
          <button className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors">
            Configure
          </button>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex items-center justify-end gap-4">
        {saveMessage && (
          <p className={`text-sm ${saveMessage.type === "success" ? "text-green-600" : "text-red-600"}`}>
            {saveMessage.text}
          </p>
        )}
        <button 
          onClick={handleSaveChanges}
          disabled={isSaving || !hasChanges}
          className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-colors ${
            hasChanges && !isSaving
              ? "bg-gray-900 text-white hover:bg-gray-800"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          {isSaving ? "Saving..." : "Save Changes"}
        </button>
      </div>
    </div>
  );
}
