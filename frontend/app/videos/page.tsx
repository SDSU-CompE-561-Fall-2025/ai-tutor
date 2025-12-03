"use client";

import React, { useEffect, useState } from "react";
import { Search, Video, Loader2 } from "lucide-react";
import {
  searchDrive,
  generateVideo,
  listMyVideos,
  clearAuthTokens,
  ApiError,
} from "@/lib/api";
import Link from "next/link";
import { useRouter } from "next/navigation";

type DriveResult = {
  id: string;
  name: string;
  modifiedTime?: string;
};

type VideoItem = {
  filename: string;
  url: string;
  created: number;
};

export default function VideosPage() {
  const router = useRouter();
  const [videos, setVideos] = useState<VideoItem[]>([]);
  const [isLoadingVideos, setIsLoadingVideos] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [driveResults, setDriveResults] = useState<DriveResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedFileId, setSelectedFileId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadVideos = async () => {
      try {
        const resp = await listMyVideos();
        const baseUrl =
          process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
        const mapped = (resp.videos || []).map((v) => {
          const url = v.video_url || "";
          const fullUrl = url.startsWith("http") ? url : `${baseUrl}${url}`;
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

  const handleSearch = async () => {
    try {
      setIsSearching(true);
      setError(null);
      const results = await searchDrive(searchQuery.trim() || undefined);
      setDriveResults(
        results.map((item) => ({
          id: item.id,
          name: item.name,
          modifiedTime: item.modifiedTime,
        }))
      );
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Failed to search drive";
      setError(msg);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
      }
    } finally {
      setIsSearching(false);
    }
  };

  const handleGenerate = async () => {
    if (!selectedFileId) {
      setError("Please select a file to generate a video.");
      return;
    }
    try {
      setIsGenerating(true);
      setError(null);
      const title = searchQuery.trim() || "Video";
      await generateVideo({ file_id: selectedFileId, title });
      const resp = await listMyVideos();
      const baseUrl =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";
      const mapped = (resp.videos || []).map((v) => {
        const url = v.video_url || "";
        const fullUrl = url.startsWith("http") ? url : `${baseUrl}${url}`;
        return {
          filename: v.filename,
          url: fullUrl,
          created: v.created,
        };
      });
      setVideos(mapped);
      setSelectedFileId(null);
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

  return (
    <div className="p-8 space-y-8 ">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Video Generation</h1>
          <p className="text-sm text-gray-600">
            Search a Google Drive doc by name, select it, and generate a video.
          </p>
        </div>
      </div>

      {error && (
        <div className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 gap-6">
        {/* Search and selection */}
        <div className="lg:col-span-1 space-y-4">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="w-5 h-5 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search Google Drive..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-24 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <button
              onClick={handleSearch}
              disabled={isSearching}
              className="absolute inset-y-0 right-0 px-4 text-sm text-gray-700 hover:text-gray-900"
            >
              {isSearching ? "Searching..." : "Search"}
            </button>
          </div>

          <div className="border border-gray-200 rounded-lg p-3 max-h-80 overflow-auto space-y-2">
            {driveResults.length === 0 ? (
              <p className="text-sm text-gray-500">No results. Try a search.</p>
            ) : (
              driveResults.map((file) => (
                <label
                  key={file.id}
                  className={`flex items-center justify-between px-3 py-2 rounded-lg border ${
                    selectedFileId === file.id
                      ? "border-gray-900 bg-gray-50"
                      : "border-gray-200"
                  }`}
                >
                  <div>
                    <p className="text-sm font-medium text-gray-900">
                      {file.name}
                    </p>
                    {file.modifiedTime && (
                      <p className="text-xs text-gray-500">
                        Modified {new Date(file.modifiedTime).toLocaleString()}
                      </p>
                    )}
                  </div>
                  <input
                    type="radio"
                    name="file"
                    value={file.id}
                    checked={selectedFileId === file.id}
                    onChange={() => setSelectedFileId(file.id)}
                  />
                </label>
              ))
            )}
          </div>

          <button
            onClick={handleGenerate}
            disabled={isGenerating}
            className="w-full flex items-center justify-center gap-2 bg-gray-900 text-white py-2 rounded-lg hover:bg-gray-800 transition-colors"
          >
            {isGenerating ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Video className="w-4 h-4" />
            )}
            {isGenerating ? "Generating..." : "Generate Video"}
          </button>
        </div>

        {/* Videos list */}
        <div className="lg:col-span-2">
          <h2 className="text-lg font-semibold text-gray-900 mb-3">
            Your Videos
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {isLoadingVideos ? (
              <div className="col-span-2 text-gray-500">Loading videos...</div>
            ) : videos.length === 0 ? (
              <div className="col-span-2 text-gray-500">
                No videos yet. Generate one to see it here.
              </div>
            ) : (
              videos.map((video) => (
                <Link
                  key={video.filename}
                  href={video.url || "#"}
                  target="_blank"
                  className="border border-gray-200 rounded-lg overflow-hidden hover:shadow transition-shadow block"
                >
                  <video
                    controls
                    className="w-full h-48 bg-black"
                    src={video.url || undefined}
                  />
                  <div className="p-3 space-y-1">
                    <p className="text-sm font-medium text-gray-900">
                      {video.filename}
                    </p>
                    <p className="text-xs text-gray-500">
                      Created {new Date(video.created * 1000).toLocaleString()}
                    </p>
                    <p className="text-sm text-blue-600">Open video</p>
                  </div>
                </Link>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
