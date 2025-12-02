"use client";

import React from "react";
import { X } from "lucide-react";

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
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-bold text-gray-900">Create New Class</h2>
            <p className="text-sm text-gray-600 mt-1">Add a new class to organize your documents and start learning.</p>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-lg transition-colors"
            aria-label="Close"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {/* Class Name */}
          <div>
            <label htmlFor="className" className="block text-sm font-medium text-gray-700 mb-2">
              Class Name
            </label>
            <input
              id="className"
              type="text"
              placeholder="e.g. Advanced Calculus"
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Description */}
          <div>
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id="description"
              placeholder="Brief description of the class content..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-900 rounded-lg hover:bg-gray-50 transition-colors font-medium"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="flex-1 px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? "Creating..." : "Create Class"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
