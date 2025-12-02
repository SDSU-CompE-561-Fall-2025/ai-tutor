"use client";

import React, { useState, useMemo, use } from "react";
import { ArrowLeft, Upload, Search, Send, FileText, Download } from "lucide-react";
import Link from "next/link";

// Mock classes data - same as dashboard
const MOCK_CLASSES = [
  {
    id: "1",
    name: "Introduction to Machine Learning",
    description: "Learn the basics of ML algorithms and data...",
    docCount: 12,
    color: "blue" as const,
  },
  {
    id: "2",
    name: "Advanced Python Patterns",
    description: "Deep dive into decorators, generators, and context...",
    docCount: 8,
    color: "green" as const,
  },
  {
    id: "3",
    name: "System Design Fundamentals",
    description: "Scalability, reliability, and maintainability of large...",
    docCount: 24,
    color: "purple" as const,
  },
  {
    id: "4",
    name: "React Server Components",
    description: "Understanding the new architecture of React and...",
    docCount: 5,
    color: "orange" as const,
  },
];

interface Document {
  id: string;
  name: string;
  uploadedAt: string;
  size: string;
}

interface ChatMessage {
  id: string;
  sender: "user" | "ai";
  content: string;
  timestamp: string;
}

// Mock documents data
const MOCK_DOCUMENTS: Document[] = [
  {
    id: "1",
    name: "Lecture_Notes_Week_1.pdf",
    uploadedAt: "2 days ago",
    size: "2.4 MB",
  },
  {
    id: "2",
    name: "Lecture_Notes_Week_2.pdf",
    uploadedAt: "2 days ago",
    size: "2.4 MB",
  },
  {
    id: "3",
    name: "Lecture_Notes_Week_3.pdf",
    uploadedAt: "2 days ago",
    size: "2.4 MB",
  },
  {
    id: "4",
    name: "Lecture_Notes_Week_4.pdf",
    uploadedAt: "2 days ago",
    size: "2.4 MB",
  },
];

// Mock chat messages
const MOCK_MESSAGES: ChatMessage[] = [
  {
    id: "1",
    sender: "ai",
    content: "Hello! I'm your AI tutor for this class. How can I help you with the course materials today?",
    timestamp: "just now",
  },
];

export default function ClassDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const resolvedParams = use(params);
  const [activeTab, setActiveTab] = useState<"docs" | "chat">("docs");
  const [searchQuery, setSearchQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>(MOCK_MESSAGES);
  const [chatInput, setChatInput] = useState("");

  // Find the current class from mock data
  const currentClass = useMemo(() => {
    return MOCK_CLASSES.find((cls) => cls.id === resolvedParams.id);
  }, [resolvedParams.id]);

  // Filter documents based on search query
  const filteredDocuments = useMemo(() => {
    return MOCK_DOCUMENTS.filter((doc) =>
      doc.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery]);

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      content: chatInput,
      timestamp: "just now",
    };

    setMessages([...messages, userMessage]);
    setChatInput("");

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        sender: "ai",
        content: "That's a great question! Based on the documents in this class, I can help you understand this topic better. Could you provide more details about what you'd like to know?",
        timestamp: "just now",
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 500);
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Main content - Documents */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-8 py-6">
          <div className="flex items-center gap-4 mb-6">
            <Link href="/dashboard">
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <ArrowLeft className="w-5 h-5 text-gray-600" />
              </button>
            </Link>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{currentClass?.name || "Class"}</h1>
              <p className="text-sm text-gray-500">Class ID: {resolvedParams.id}</p>
            </div>
          </div>

          {/* Tabs and Upload */}
          <div className="flex items-center justify-between">
            <div className="flex gap-8">
              <button 
                onClick={() => setActiveTab("docs")}
                className={`pb-3 border-b-2 transition-colors ${
                  activeTab === "docs"
                    ? "border-gray-900 text-gray-900 font-medium"
                    : "border-transparent text-gray-500 hover:text-gray-900"
                }`}
              >
                Docs
              </button>
              <button 
                onClick={() => setActiveTab("chat")}
                className={`pb-3 border-b-2 transition-colors ${
                  activeTab === "chat"
                    ? "border-gray-900 text-gray-900 font-medium"
                    : "border-transparent text-gray-500 hover:text-gray-900"
                }`}
              >
                Chat
              </button>
            </div>
            {activeTab === "docs" && (
              <button className="flex items-center gap-2 bg-white border border-gray-300 text-gray-900 px-4 py-2 rounded-lg hover:bg-gray-50 transition-colors font-medium">
                <Upload className="w-4 h-4" />
                Upload
              </button>
            )}
          </div>
        </div>

        {/* Docs Tab Content */}
        {activeTab === "docs" && (
        <div className="flex-1 overflow-auto px-8 py-6 flex flex-col">
          {/* Search Bar */}
          <div className="mb-6">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="w-5 h-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search documents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          {/* Documents List */}
          <div className="space-y-3">
            {filteredDocuments.length > 0 ? (
              filteredDocuments.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center justify-between p-4 bg-white border border-gray-300 rounded-lg hover:shadow transition-shadow"
                >
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                      <p className="text-xs text-gray-500">Uploaded {doc.uploadedAt} • {doc.size}</p>
                    </div>
                  </div>
                  <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                    <Download className="w-4 h-4 text-gray-600" />
                  </button>
                </div>
              ))
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <FileText className="w-12 h-12 text-gray-300 mb-3" />
                <p className="text-gray-500">No documents found</p>
              </div>
            )}
          </div>
        </div>
        )}

        {/* Chat Tab Content */}
        {activeTab === "chat" && (
        <div className="flex-1 overflow-auto px-8 py-6 flex flex-col">
          <div className="flex flex-col h-full">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Class Discussion</h2>
            
            {/* Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 mb-4">
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-xs px-4 py-2 rounded-lg ${
                      msg.sender === "user"
                        ? "bg-gray-900 text-white"
                        : "bg-gray-100 text-gray-900"
                    }`}
                  >
                    <p className="text-sm">{msg.content}</p>
                  </div>
                </div>
              ))}
            </div>

            {/* Chat Input */}
            <div className="border-t border-gray-200 pt-4">
              <p className="text-xs text-gray-500 mb-3">
                AI can make mistakes. Please verify important information.
              </p>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Ask a question about your documents..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      handleSendMessage();
                    }
                  }}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                />
                <button
                  onClick={handleSendMessage}
                  className="p-2 bg-white border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
        )}
      </div>
    </div>
  );
}
