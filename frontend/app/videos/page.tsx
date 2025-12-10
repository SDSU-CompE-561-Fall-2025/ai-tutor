"use client";
// import necessary modules and components
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  listMyVideos,
  generateVideo,
  ApiError,
  clearAuthTokens,
  getFilesForCourse,
  getCourses,
} from "@/lib/api";
import { Play } from "lucide-react";
import { useDarkMode } from "@/hooks/useDarkMode";

// Type definitions for video data
// Type definitions are used to ensure correct data structure

// Ex: In the video type definition, each video has a filename, URL, and creation date
type Video = {
  filename: string;
  url: string;
  created: string;
};

type FileResponse = {
  id: number;
  name: string;
  google_drive_id?: string | null;
  course_name: string;
  created_at: string;
};

// VideosPage is the main component for displaying and generating videos
const VideosPage = () => {
  const router = useRouter();
  const { isDark } = useDarkMode();

  // State management
  const [videos, setVideos] = useState<Video[]>([]); // List of generated videos
  const [files, setFiles] = useState<FileResponse[]>([]); // List of files associated with courses
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null); // Currently selected file for video generation
  const [searchQuery, setSearchQuery] = useState(""); // Search query for filtering videos
  const [isLoadingVideos, setIsLoadingVideos] = useState(true); // Loading state for videos
  const [isGenerating, setIsGenerating] = useState(false); // Loading state for video generation
  const [error, setError] = useState<string | null>(null); // Error message for display

  // Load videos on component mount
  useEffect(() => {
    const loadVideos = async () => {
      try {
        // listMyVideos fetches the user's generated videos
        const resp = await listMyVideos();
        // baseurl is our backend API URL
        const baseUrl =
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
        const mapped = (resp.videos || []).map((v) => {
          const url = v.video_url || "";
          // If URL is already absolute, use it as-is; otherwise, join with baseUrl
          const fullUrl = url.startsWith("http")
            ? url
            : `${baseUrl}${url.startsWith("/") ? url : "/" + url}`;
          return {
            filename: v.filename,
            url: fullUrl,
            created: v.created,
          };
        });
        setVideos(mapped);
      } catch (err) {
        const msg =
          err instanceof Error ? err.message : "Failed to load videos";
        setError(msg);
        if (err instanceof ApiError && err.status === 401) {
          clearAuthTokens();
          router.push("/login");
        }
      } finally {
        setIsLoadingVideos(false);
      }
    };

    loadVideos();
  }, [router]);

  // Load courses and files for generation
  useEffect(() => {
    const loadData = async () => {
      try {
        const coursesData = await getCourses();

        // Load files from all courses
        if (coursesData.length > 0) {
          const allFiles = await Promise.all(
            coursesData.map((course) => getFilesForCourse(course.id))
          );
          setFiles(allFiles.flat());
        }
      } catch (err) {
        console.error("Failed to load courses/files:", err);
      }
    };

    loadData();
  }, []);

  // Handle video generation
  const handleGenerate = async () => {
    if (!selectedFileId) {
      setError("Please select a file to generate a video.");
      return;
    }
    try {
      setIsGenerating(true);
      setError(null);
      // Find the selected file to get its google_drive_id
      const selectedFile = files.find(
        (f) => f.id.toString() === selectedFileId
      );

      if (!selectedFile?.google_drive_id) {
        setError("Selected file does not have a valid Google Drive ID.");
        setIsGenerating(false);
        return;
      }

      // Use the title from input field, or default to "Generated Video"
      const title = searchQuery.trim() || "Generated Video";
      // Pass the google_drive_id instead of the database id
      await generateVideo({ file_id: selectedFile.google_drive_id, title });

      // Refresh video list
      const resp = await listMyVideos();
      const baseUrl =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
      const mapped = (resp.videos || []).map((v) => {
        const url = v.video_url || "";
        // If URL is already absolute, use it as-is; otherwise, join with baseUrl
        const fullUrl = url.startsWith("http")
          ? url
          : `${baseUrl}${url.startsWith("/") ? url : "/" + url}`;
        return {
          filename: v.filename,
          url: fullUrl,
          created: v.created,
        };
      });
      setVideos(mapped);
      setSelectedFileId(null);
      setSearchQuery("");
    } catch (err) {
      const msg =
        err instanceof Error ? err.message : "Failed to generate video";
      setError(msg);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
      }
    } finally {
      setIsGenerating(false);
    }
  };

  // Frontend
  return (
    <div
      className={`min-h-screen p-8 ${isDark ? "bg-gray-800" : "bg-background"}`}
    >
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="mb-8">
          <h1
            className={`text-3xl font-bold mb-2 ${
              isDark ? "text-white" : "text-foreground"
            }`}
          >
            Generated Videos
          </h1>
          <p className={isDark ? "text-gray-300" : "text-muted-foreground"}>
            Visual explanations generated from your source materials.
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div
            className={`mb-6 p-4 rounded-lg ${
              isDark
                ? "bg-red-900/30 border border-red-700/50 text-red-300"
                : "bg-destructive/10 border border-destructive/20 text-destructive"
            }`}
          >
            {error}
          </div>
        )}

        {/* Video Generation Section */}
        <div
          className={`mb-8 p-6 border rounded-lg ${
            isDark ? "bg-gray-700 border-gray-600" : "bg-card border-border"
          }`}
        >
          <h2
            className={`text-xl font-semibold mb-4 ${
              isDark ? "text-white" : "text-foreground"
            }`}
          >
            Generate New Video
          </h2>
          <div className="flex gap-4 flex-wrap">
            {/* File Selection */}
            <select
              value={selectedFileId || ""}
              onChange={(e) => setSelectedFileId(e.target.value || null)}
              className={`flex-1 min-w-[200px] px-4 py-2 border rounded-md focus:outline-none focus:ring-2 ${
                isDark
                  ? "bg-gray-600 border-gray-500 text-white focus:ring-blue-500"
                  : "bg-background border-input focus:ring-ring"
              }`}
              disabled={isGenerating}
            >
              <option value="">Select a file...</option>
              {files.map((file) => (
                <option key={file.id} value={file.id.toString()}>
                  {file.name} ({file.course_name})
                </option>
              ))}
            </select>

            {/* Title Input */}
            <input
              type="text"
              placeholder="Video title (optional)"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              maxLength={25}
              className={`flex-1 min-w-[200px] px-4 py-2 border rounded-md focus:outline-none focus:ring-2 ${
                isDark
                  ? "bg-gray-600 border-gray-500 text-white placeholder-gray-400 focus:ring-blue-500"
                  : "bg-background border-input focus:ring-ring"
              }`}
              disabled={isGenerating}
            />

            {/* Generate Button */}
            <Button
              onClick={handleGenerate}
              disabled={isGenerating || !selectedFileId}
              className="px-6"
            >
              {isGenerating ? "Generating..." : "Generate Video"}
            </Button>
          </div>
        </div>

        {/* Videos Grid */}
        {isLoadingVideos ? (
          <div className="flex items-center justify-center py-20">
            <div className={isDark ? "text-gray-300" : "text-muted-foreground"}>
              Loading videos...
            </div>
          </div>
        ) : videos.length === 0 ? (
          <div className="flex items-center justify-center py-20">
            <div className="text-center">
              <p
                className={
                  isDark ? "text-gray-300 mb-2" : "text-muted-foreground mb-2"
                }
              >
                No videos generated yet
              </p>
              <p
                className={`text-sm ${
                  isDark ? "text-gray-400" : "text-muted-foreground"
                }`}
              >
                Select a file and generate your first video!
              </p>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {videos.map((video) => {
              // Extract title from filename (remove user_id prefix and .mp4 extension)
              const cleanTitle = video.filename
                .replace(/^\d+_video_/, "") // Remove user_id_video_ prefix
                .replace(/\.mp4$/, "") // Remove .mp4 extension
                .replaceAll("_", " ") // Replace underscores with spaces
                .replace(/^([a-f0-9]{32})$/i, "Generated Video") // Replace UUID with generic name
                .trim();

              return (
                <div
                  key={video.url}
                  className={`border rounded-lg overflow-hidden hover:shadow-lg transition-shadow ${
                    isDark
                      ? "bg-gray-700 border-gray-600"
                      : "bg-card border-border"
                  }`}
                >
                  {/* Video Thumbnail/Player */}
                  <div
                    className={`relative aspect-video ${
                      isDark ? "bg-gray-600" : "bg-muted"
                    }`}
                  >
                    <video
                      src={video.url}
                      className="w-full h-full object-cover"
                      controls
                      preload="metadata"
                    >
                      Your browser does not support the video tag.
                    </video>

                    {/* Play Overlay (optional styling) */}
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-0 hover:opacity-100 transition-opacity">
                      <div className="bg-black/50 rounded-full p-4">
                        <Play className="w-8 h-8 text-white" />
                      </div>
                    </div>
                  </div>

                  {/* Video Info */}
                  <div className="p-5">
                    <h3
                      className={`font-semibold text-base line-clamp-2 leading-snug mb-4 ${
                        isDark ? "text-white" : "text-foreground"
                      }`}
                    >
                      {cleanTitle}
                    </h3>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => window.open(video.url, "_blank")}
                      className={`w-full ${
                        isDark
                          ? "border-gray-600 text-gray-200 hover:bg-gray-600"
                          : ""
                      }`}
                    >
                      View Full Screen
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideosPage;
