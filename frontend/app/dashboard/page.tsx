"use client";

import React, { useState, useMemo, useEffect } from "react";
import { Plus, Search, BookOpen, FileText } from "lucide-react";
import Link from "next/link";
import CreateClassModal from "@/components/CreateClassModal";
import { useRouter } from "next/navigation";
import {
  createCourse,
  getCourses,
  getFilesForCourse,
  getStoredAccessToken,
  clearAuthTokens,
  ApiError,
} from "@/lib/api";
import { useDarkMode } from "@/hooks/useDarkMode";

interface Class {
  id: string;
  name: string;
  description: string;
  docCount: number;
  color: "blue" | "green" | "purple" | "orange";
}

const COLOR_OPTIONS: Class["color"][] = ["blue", "green", "purple", "orange"];

const getColorClasses = (color: string) => {
  const colors: Record<string, { icon: string; bg: string }> = {
    blue: {
      icon: "text-blue-500",
      bg: "bg-blue-100",
    },
    green: {
      icon: "text-green-500",
      bg: "bg-green-100",
    },
    purple: {
      icon: "text-purple-500",
      bg: "bg-purple-100",
    },
    orange: {
      icon: "text-orange-500",
      bg: "bg-orange-100",
    },
  };
  return colors[color] || colors.blue;
};

const ClassCard = ({ cls, isDark }: { cls: Class; isDark: boolean }) => {
  const { icon, bg } = getColorClasses(cls.color);
  const borderColors: Record<string, string> = {
    blue: isDark
      ? "border-blue-500/50 hover:border-blue-400"
      : "border-blue-300 hover:border-blue-400",
    green: isDark
      ? "border-green-500/50 hover:border-green-400"
      : "border-green-300 hover:border-green-400",
    purple: isDark
      ? "border-purple-500/50 hover:border-purple-400"
      : "border-purple-300 hover:border-purple-400",
    orange: isDark
      ? "border-orange-500/50 hover:border-orange-400"
      : "border-orange-300 hover:border-orange-400",
  };
  return (
    <Link href={`/class/${cls.id}`}>
      <div
        className={`h-56 border-2 ${borderColors[cls.color]} ${
          isDark ? "bg-gray-700/80" : "bg-white"
        } rounded-lg p-6 hover:shadow-xl transition-all cursor-pointer flex flex-col transform hover:scale-[1.02]`}
      >
        <div
          className={`w-12 h-12 ${bg} rounded-lg flex items-center justify-center mb-4 shadow-md`}
        >
          <BookOpen className={`w-6 h-6 ${icon}`} />
        </div>
        <h3
          className={`text-lg font-bold mb-2 ${
            isDark ? "text-white" : "text-gray-900"
          }`}
        >
          {cls.name}
        </h3>
        <p
          className={`text-sm mb-4 line-clamp-2 grow ${
            isDark ? "text-gray-300" : "text-gray-600"
          }`}
        >
          {cls.description}
        </p>
        <div
          className={`flex items-center gap-2 text-sm mt-auto ${
            isDark ? "text-gray-300" : "text-gray-600"
          }`}
        >
          <FileText className={`w-4 h-4 ${icon}`} />
          <span>{cls.docCount} Docs</span>
        </div>
      </div>
    </Link>
  );
};

export default function DashboardPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [classes, setClasses] = useState<Class[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);
  const { isDark, toggleDarkMode } = useDarkMode();

  // Ensure component is mounted on client before checking auth
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    // Only run auth check after component has mounted on client
    if (!mounted) return;

    const fetchClasses = async () => {
      const token = getStoredAccessToken();
      if (!token) {
        setIsLoading(false);
        router.push("/login");
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        const courses = await getCourses();
        const enrichedCourses = await Promise.all(
          courses.map(async (course, index) => {
            let docCount = 0;
            try {
              const files = await getFilesForCourse(course.id);
              docCount = files.length;
            } catch (err) {
              console.error(
                `Failed to load files for course ${course.id}`,
                err
              );
            }

            return {
              id: course.id.toString(),
              name: course.name,
              description: course.description || "",
              docCount,
              color: COLOR_OPTIONS[index % COLOR_OPTIONS.length],
            } satisfies Class;
          })
        );

        setClasses(enrichedCourses);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : "Failed to load classes";
        setError(message);
        if (err instanceof ApiError && err.status === 401) {
          clearAuthTokens();
          router.push("/login");
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchClasses();
  }, [router, mounted]);

  // Filter classes based on search query
  const filteredClasses = useMemo(() => {
    return classes.filter(
      (cls) =>
        cls.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cls.description.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery, classes]);

  const handleCreateClass = async (data: {
    name: string;
    description: string;
  }) => {
    try {
      setError(null);
      const response = await createCourse({
        name: data.name,
        description: data.description,
      });
      const newClass: Class = {
        id: response.id.toString(),
        name: response.name,
        description: response.description || "",
        docCount: 0,
        color: COLOR_OPTIONS[classes.length % COLOR_OPTIONS.length],
      };
      setClasses([...classes, newClass]);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Failed to create class";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
      }
      throw err;
    }
  };

  return (
    <div
      className={`flex h-screen ${
        isDark ? "bg-gray-800 text-white" : "bg-gray-50"
      }`}
    >
      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header section */}
        <div
          className={`${
            isDark ? "bg-gray-700 border-gray-600" : "bg-white border-gray-200"
          } border-b px-8 py-6`}
        >
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1
                className={`text-3xl font-bold ${
                  isDark ? "text-white" : "text-gray-900"
                }`}
              >
                Classes
              </h1>
              <p className={`mt-1 ${isDark ? "text-white" : "text-gray-600"}`}>
                Manage your learning spaces and resources.
              </p>
            </div>
            <button
              onClick={toggleDarkMode}
              className="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-800 dark:text-gray-200 rounded-lg font-semibold transition-colors"
            >
              {isDark ? "Light Mode" : "Dark Mode"}
            </button>
          </div>

          {/* Search and Add Class section */}
          <div className="flex items-center gap-4">
            {/* Search bar */}
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search
                  className={`w-5 h-5 ${
                    isDark ? "text-gray-400" : "text-gray-400"
                  }`}
                />
              </div>
              <input
                type="text"
                placeholder="Search classes..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                maxLength={25}
                className={`w-full pl-10 pr-4 py-2 border ${
                  isDark
                    ? "border-gray-600 bg-gray-600 text-white placeholder-gray-400"
                    : "border-gray-300 bg-white text-gray-900"
                } rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all`}
              />
            </div>

            {/* Add Class button */}
            <button
              onClick={() => setIsModalOpen(true)}
              className={`flex items-center gap-2 border px-4 py-2 rounded-lg transition-all font-medium shadow-md hover:shadow-lg ${
                isDark
                  ? "bg-gradient-to-r from-blue-600 to-purple-600 border-blue-500 text-white hover:from-blue-700 hover:to-purple-700"
                  : "bg-gradient-to-r from-blue-500 to-purple-500 border-blue-400 text-white hover:from-blue-600 hover:to-purple-600"
              }`}
            >
              <Plus className="w-5 h-5" />
              Add Class
            </button>
          </div>
        </div>

        {/* Classes grid */}
        <div className="flex-1 overflow-auto px-8 py-6">
          {error && (
            <div
              className={`mb-4 rounded-md border px-4 py-3 text-sm ${
                isDark
                  ? "border-red-600 bg-red-900/30 text-red-300"
                  : "border-red-200 bg-red-50 text-red-700"
              }`}
            >
              {error}
            </div>
          )}
          {isLoading ? (
            <div
              className={`flex items-center justify-center h-full ${
                isDark ? "text-white" : "text-gray-500"
              }`}
            >
              Loading classes...
            </div>
          ) : filteredClasses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredClasses.map((cls) => (
                <ClassCard key={cls.id} cls={cls} isDark={isDark} />
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <BookOpen
                className={`w-16 h-16 mb-4 ${
                  isDark ? "text-gray-500" : "text-gray-300"
                }`}
              />
              <h3
                className={`text-lg font-medium mb-2 ${
                  isDark ? "text-white" : "text-gray-900"
                }`}
              >
                No classes found
              </h3>
              <p className={isDark ? "text-white" : "text-gray-600"}>
                Try adjusting your search or add a new class to get started.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Modal */}
      <CreateClassModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={handleCreateClass}
      />
    </div>
  );
}
