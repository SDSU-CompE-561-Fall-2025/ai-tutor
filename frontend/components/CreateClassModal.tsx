"use client";

import React from "react";
import { X } from "lucide-react";
import { useDarkMode } from "@/contexts/DarkModeContext";

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
  const { isDark } = useDarkMode();
  const [className, setClassName] = React.useState("");
  const [description, setDescription] = React.useState("");
  const [isLoading, setIsLoading] = React.useState(false);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    // Class name input validation
    if (!className.trim()) {
      alert("Please enter a class name");
      return;
    }

    if(className.length > 30) {
      alert("Class name must be 30 characters or less");
      return;
    }

    // Description input validation
    if(description.length > 100) {
      alert("Description must be 100 characters or less");
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
      <div className={`rounded-lg shadow-xl w-full max-w-md mx-4 ${
        isDark ? "bg-gray-700" : "bg-white"
      }`}>
        {/* Header */}
        <div className={`flex items-center justify-between px-6 py-4 border-b ${
          isDark ? "border-gray-600" : "border-gray-200"
        }`}>
          <div>
            <h2 className={`text-xl font-bold ${
              isDark ? "text-white" : "text-gray-900"
            }`}>Create New Class</h2>
            <p className={`text-sm mt-1 ${
              isDark ? "text-gray-400" : "text-gray-600"
            }`}>Add a new class to organize your documents and start learning.</p>
          </div>
          <button
            onClick={onClose}
            className={`p-1 rounded-lg transition-colors ${
              isDark ? "hover:bg-gray-600" : "hover:bg-gray-100"
            }`}
            aria-label="Close"
          >
            <X className={`w-5 h-5 ${
              isDark ? "text-gray-400" : "text-gray-500"
            }`} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Class Name */}
          <div>
            <label htmlFor="className" className={`block text-sm font-medium mb-2 ${
              isDark ? "text-gray-300" : "text-gray-700"
            }`}>
              Class Name
              <span className="text-xs text-gray-500 ml-2">({className.length}/30)</span>
            </label>
            <input
              id="className"
              type="text"
              placeholder="e.g. Advanced Calculus"
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              maxLength={30}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                isDark
                  ? "bg-gray-600 border-gray-500 text-white placeholder-gray-400"
                  : "bg-white border-gray-300 text-gray-900"
              }`}
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className={`block text-sm font-medium mb-2 ${
              isDark ? "text-gray-300" : "text-gray-700"
            }`}>
              Description
              <span className="text-xs text-gray-500 ml-2">({description.length}/100)</span>
            </label>
            <textarea
              id="description"
              placeholder="Brief description of the class content..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              maxLength={100}
              rows={3}
              className={`w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none ${
                isDark
                  ? "bg-gray-600 border-gray-500 text-white placeholder-gray-400"
                  : "bg-white border-gray-300 text-gray-900"
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
                  ? "border-gray-500 text-gray-300 hover:bg-gray-600"
                  : "border-gray-300 text-gray-900 hover:bg-gray-50"
              }`}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className={`flex-1 px-4 py-2 rounded-lg transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed ${
                isDark
                  ? "bg-blue-600 text-white hover:bg-blue-700"
                  : "bg-gray-900 text-white hover:bg-gray-800"
              }`}
            >
              {isLoading ? "Creating..." : "Create Class"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
