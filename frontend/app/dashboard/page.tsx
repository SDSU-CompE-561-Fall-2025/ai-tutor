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

const ClassCard = ({ cls }: { cls: Class }) => {
  const { icon, bg } = getColorClasses(cls.color);
  return (
    <Link href={`/class/${cls.id}`}>
      <div className="h-56 border border-gray-300 rounded-lg p-6 hover:shadow-lg transition-shadow cursor-pointer bg-white flex flex-col">
        <div className={`w-12 h-12 ${bg} rounded-lg flex items-center justify-center mb-4`}>
          <BookOpen className={`w-6 h-6 ${icon}`} />
        </div>
        <h3 className="text-lg font-bold text-gray-900 mb-2">{cls.name}</h3>
        <p className="text-sm text-gray-600 mb-4 line-clamp-2 flex-grow">{cls.description}</p>
        <div className="flex items-center gap-2 text-sm text-gray-600 mt-auto">
          <FileText className="w-4 h-4" />
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

  useEffect(() => {
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
              console.error(`Failed to load files for course ${course.id}`, err);
            }

            return {
              id: course.id.toString(),
              name: course.name,
              description: "",
              docCount,
              color: COLOR_OPTIONS[index % COLOR_OPTIONS.length],
            } satisfies Class;
          }),
        );

        setClasses(enrichedCourses);
      } catch (err) {
        const message = err instanceof Error ? err.message : "Failed to load classes";
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
  }, [router]);

  // Filter classes based on search query
  const filteredClasses = useMemo(() => {
    return classes.filter((cls) =>
      cls.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cls.description.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery, classes]);

  const handleCreateClass = async (data: { name: string; description: string }) => {
    try {
      setError(null);
      const response = await createCourse({ name: data.name });
      const newClass: Class = {
        id: response.id.toString(),
        name: response.name,
        description: data.description || "",
        docCount: 0,
        color: COLOR_OPTIONS[classes.length % COLOR_OPTIONS.length],
      };
      setClasses([...classes, newClass]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create class";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
      }
      throw err;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main content area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header section */}
        <div className="bg-white border-b border-gray-200 px-8 py-6">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-900">Classes</h1>
            <p className="text-gray-600 mt-1">Manage your learning spaces and resources.</p>
          </div>

          {/* Search and Add Class section */}
          <div className="flex items-center gap-4">
            {/* Search bar */}
            <div className="flex-1 relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="w-5 h-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search classes..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Add Class button */}
            <button
              onClick={() => setIsModalOpen(true)}
              className="flex items-center gap-2 bg-white border border-gray-300 text-gray-900 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              <Plus className="w-5 h-5" />
              Add Class
            </button>
          </div>
        </div>

        {/* Classes grid */}
        <div className="flex-1 overflow-auto px-8 py-6">
          {error && (
            <div className="mb-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}
          {isLoading ? (
            <div className="flex items-center justify-center h-full text-gray-500">
              Loading classes...
            </div>
          ) : filteredClasses.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredClasses.map((cls) => (
                <ClassCard key={cls.id} cls={cls} />
              ))}
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <BookOpen className="w-16 h-16 text-gray-300 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No classes found</h3>
              <p className="text-gray-600">Try adjusting your search or add a new class to get started.</p>
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
