"use client";

import React, { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, MoreVertical, Play, Plus } from "lucide-react";

// TODO: 
// import { fetchVideos, type VideoListItem } from "../../lib/api";

interface Video {
  id: string;
  title: string;
  generated: string;
  thumbnail: string;
  duration?: string;
}

// Mock data - Replace with actual API call
const mockVideos: Video[] = [
  {
    id: "1",
    title: "Understanding Neural Networks",
    generated: "Generated 2 days ago",
    thumbnail: "/thumbs/neural.jpg",
    duration: "12:45",
  },
  {
    id: "2",
    title: "Backpropagation Explained",
    generated: "Generated 3 days ago",
    thumbnail: "/thumbs/backprop.png",
    duration: "08:30",
  },
  {
    id: "3",
    title: "Gradient Descent Visualization",
    generated: "Generated 1 week ago",
    thumbnail: "/thumbs/gradient.jpg",
    duration: "15:20",
  },
];

function VideoCard({ video }: { video: Video }) {
  return (
    <Card className="overflow-hidden hover:shadow-lg transition-shadow">
      {/* Video Thumbnail */}
      <div className="relative h-48 w-full bg-gray-100">
        <Image
          src={video.thumbnail}
          alt={`${video.title} thumbnail`}
          fill
          sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          style={{ objectFit: "cover" }}
          className="bg-gradient-to-br from-gray-200 to-gray-300"
        />
        {video.duration && (
          <Badge className="absolute right-2 bottom-2 bg-black/75 text-white border-0">
            {video.duration}
          </Badge>
        )}
      </div>

      <CardHeader className="pb-3">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-lg leading-snug">{video.title}</CardTitle>
          <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0">
            <MoreVertical className="h-4 w-4" />
          </Button>
        </div>
        <CardDescription className="flex items-center gap-1">
          <Clock className="h-4 w-4" />
          {video.generated}
        </CardDescription>
      </CardHeader>

      <CardFooter>
        <Button variant="outline" className="w-full" asChild>
          <Link href={`/videos/${video.id}`}>
            <Play className="mr-2 h-4 w-4" />
            View Video
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}

export default function VideosPage() {
  const [videos] = useState<Video[]>(mockVideos);
  const [loading] = useState(false);
  const [error] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-gray-50 px-8 py-10">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Generated Videos
          </h1>
          <p className="text-gray-600">
            Visual explanations generated from your course materials.
          </p>
        </header>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            <p className="ml-3 text-gray-600">Loading videos...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="mb-6 border-red-200 bg-red-50">
            <CardContent className="pt-6">
              <p className="text-sm text-red-600">
                <strong>Error:</strong> {error}
              </p>
              <p className="text-xs text-gray-600 mt-1">
                Make sure the backend is running and you're logged in.
              </p>
            </CardContent>
          </Card>
        )}

        {/* Videos Grid */}
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {videos.map((video) => (
            <VideoCard key={video.id} video={video} />
          ))}
        </div>

        {/* Empty State */}
        {!loading && videos.length === 0 && (
          <Card className="text-center py-12">
            <CardContent className="pt-6">
              <div className="flex justify-center mb-4">
                <div className="rounded-full bg-gray-100 p-3">
                  <Play className="h-8 w-8 text-gray-400" />
                </div>
              </div>
              <CardTitle className="mb-2">No videos yet</CardTitle>
              <CardDescription className="mb-6">
                Generate your first video from course materials.
              </CardDescription>
              <Button asChild>
                <Link href="/videos/generate">
                  <Plus className="mr-2 h-4 w-4" />
                  Generate Video
                </Link>
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </main>
  );
}
