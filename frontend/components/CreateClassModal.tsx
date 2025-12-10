"use client";

import React from "react";
import { X } from "lucide-react";
import { useDarkMode } from "@/hooks/useDarkMode";

interface CreateClassModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: { name: string; description: string }) => void;
}

export default function CreateClassModal({
  isOpen,
  onClose,
  onSubmit,
}: CreateClassModalProps) {
  const [className, setClassName] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(false);
  const { isDark } = useDarkMode();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!className.trim()) {
      alert("Please enter a class name");
      return;
    }

    setIsLoading(true);
    try {
      await onSubmit({ name: className, description });
      setClassName("");
      setDescription("");
      onClose();
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div
        className={`${
          isDark ? "bg-gray-800 border-gray-700" : "bg-white"
        } rounded-lg shadow-xl w-full max-w-md mx-4 border-2 ${
          isDark ? "border-gray-700" : "border-blue-200"
        }`}
      >
        {/* Header */}
        <div
          className={`flex items-center justify-between px-6 py-4 border-b ${
            isDark
              ? "border-gray-700 bg-gradient-to-r from-blue-600/20 to-purple-600/20"
              : "border-gray-200 bg-gradient-to-r from-blue-50 to-purple-50"
          }`}
        >
          <div>
            <h2
              className={`text-xl font-bold ${
                isDark ? "text-white" : "text-gray-900"
              }`}
            >
              Create New Class
            </h2>
            <p
              className={`text-sm mt-1 ${
                isDark ? "text-gray-300" : "text-gray-600"
              }`}
            >
              Add a new class to organize your documents and start learning.
            </p>
          </div>
          <button
            onClick={onClose}
            className={`p-1 rounded-lg transition-colors ${
              isDark
                ? "hover:bg-gray-700 text-gray-300"
                : "hover:bg-gray-100 text-gray-500"
            }`}
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Class Name */}
          <div>
            <label
              htmlFor="className"
              className={`block text-sm font-medium mb-2 ${
                isDark ? "text-gray-200" : "text-gray-700"
              }`}
            >
              Class Name
            </label>
            <input
              id="className"
              type="text"
              placeholder="e.g. Advanced Calculus"
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              maxLength={25}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                isDark
                  ? "border-gray-600 bg-gray-700 text-white placeholder-gray-400"
                  : "border-gray-300 bg-white text-gray-900"
              }`}
            />
          </div>

          {/* Description */}
          <div>
            <label
              htmlFor="description"
              className={`block text-sm font-medium mb-2 ${
                isDark ? "text-gray-200" : "text-gray-700"
              }`}
            >
              Description
            </label>
            <textarea
              id="description"
              placeholder="Brief description of the class content..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              maxLength={25}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                isDark
                  ? "border-gray-600 bg-gray-700 text-white placeholder-gray-400"
                  : "border-gray-300 bg-white text-gray-900"
              }`}
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className={`flex-1 px-4 py-2 border rounded-lg transition-colors font-medium ${
                isDark
                  ? "border-gray-600 text-gray-200 hover:bg-gray-700"
                  : "border-gray-300 text-gray-900 hover:bg-gray-50"
              }`}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all font-medium disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
            >
              {isLoading ? "Creating..." : "Create Class"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
