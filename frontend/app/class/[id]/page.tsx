"use client";

import React, { useState, useMemo, useEffect } from "react";
import { ArrowLeft, Search, Send, FileText, Download, Plus } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import {
  createFile,
  getCourseById,
  getFilesForCourse,
  getStoredAccessToken,
  clearAuthTokens,
  ApiError,
  searchDrive,
  getTutorSessionsByCourse,
  createTutorSession,
  getTutorSessionMessages,
  sendMessage,
  updateCourse,
  deleteCourse,
} from "@/lib/api";

interface Document {
  id: string;
  name: string;
  uploadedAt: string;
}

interface ChatMessage {
  id: string;
  sender: "user" | "assistant";
  content: string;
  timestamp: string;
}

interface DriveResult {
  id: string;
  name: string;
  modifiedTime?: string;
}

const escapeHtml = (text: string) =>
  text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#039;");

const applyInlineMarkdown = (text: string) => {
  let result = text;
  result = result.replace(/`([^`]+)`/g, "<code>$1</code>");
  result = result.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  result = result.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return result;
};

const markdownToHtml = (raw: string) => {
  const lines = escapeHtml(raw).split(/\r?\n/);
  const htmlParts: string[] = [];
  let inList = false;

  const closeList = () => {
    if (inList) {
      htmlParts.push("</ul>");
      inList = false;
    }
  };

  lines.forEach((line) => {
    if (/^###\s+/.test(line)) {
      closeList();
      htmlParts.push(`<h3>${applyInlineMarkdown(line.replace(/^###\s+/, ""))}</h3>`);
    } else if (/^##\s+/.test(line)) {
      closeList();
      htmlParts.push(`<h2>${applyInlineMarkdown(line.replace(/^##\s+/, ""))}</h2>`);
    } else if (/^#\s+/.test(line)) {
      closeList();
      htmlParts.push(`<h1>${applyInlineMarkdown(line.replace(/^#\s+/, ""))}</h1>`);
    } else if (/^```/.test(line)) {
      // Start or end of code block: keep simple pre block
      closeList();
      const codeLines: string[] = [];
      let i = lines.indexOf(line) + 1;
      while (i < lines.length && !/^```/.test(lines[i])) {
        codeLines.push(lines[i]);
        i += 1;
      }
      htmlParts.push(`<pre><code>${codeLines.join("\n")}</code></pre>`);
      lines.splice(lines.indexOf(line), i - lines.indexOf(line) + 1);
    } else if (/^\-\s+/.test(line)) {
      if (!inList) {
        inList = true;
        htmlParts.push("<ul>");
      }
      htmlParts.push(`<li>${applyInlineMarkdown(line.replace(/^\-\s+/, ""))}</li>`);
    } else if (line.trim() === "") {
      closeList();
      htmlParts.push("<br />");
    } else {
      closeList();
      htmlParts.push(`<p>${applyInlineMarkdown(line)}</p>`);
    }
  });

  closeList();
  return htmlParts.join("");
};

export default function ClassDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const courseId = Number(params.id);
  const [activeTab, setActiveTab] = useState<"docs" | "chat" | "settings">("docs");
  const [searchQuery, setSearchQuery] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [tutorSessions, setTutorSessions] = useState<{ id: number; title: string | null }[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<number | null>(null);
  const [isLoadingSessions, setIsLoadingSessions] = useState(true);
  const [isSending, setIsSending] = useState(false);
  const [isWaitingForAi, setIsWaitingForAi] = useState(false);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [courseName, setCourseName] = useState<string>("Loading...");
  const [courseNameInput, setCourseNameInput] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [driveResults, setDriveResults] = useState<DriveResult[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      if (!params.id) return;
      const token = getStoredAccessToken();
      if (!token) {
        router.push("/login");
        return;
      }

      try {
        setIsLoading(true);
        setError(null);
        const [course, files] = await Promise.all([
          getCourseById(courseId),
          getFilesForCourse(courseId),
        ]);

        const sessions = await getTutorSessionsByCourse(courseId);
        setTutorSessions(sessions.map((s) => ({ id: s.id, title: s.title })));
        if (sessions.length > 0) {
          setActiveSessionId(sessions[0].id);
          const sessionMessages = await getTutorSessionMessages(sessions[0].id);
          setMessages(
            sessionMessages.map((m) => ({
              id: m.id.toString(),
              sender: m.role,
              content: m.message,
              timestamp: new Date(m.created_at).toLocaleString(),
            })),
          );
        }

        setIsLoadingSessions(false);

        setCourseName(course.name);
        setCourseNameInput(course.name);
        setDocuments(
          files.map((file) => ({
            id: file.id.toString(),
            name: file.name,
            uploadedAt: new Date(file.created_at).toLocaleString(),
          })),
        );
        if (sessions.length === 0) {
          setMessages([
            {
              id: "welcome",
              sender: "assistant",
              content:
                "Hello! I'm your AI tutor for this class. Create a session to start chatting.",
              timestamp: new Date().toLocaleString(),
            },
          ]);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : "Failed to load class";
        setError(message);
        if (err instanceof ApiError && err.status === 401) {
          clearAuthTokens();
          router.push("/login");
          return;
        }
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [courseId, params.id, router]);

  const displayedDocuments = useMemo(() => documents, [documents]);

  const handleSearchDrive = async () => {
    try {
      setIsSearching(true);
      setError(null);
      const results = await searchDrive(searchQuery.trim() || undefined);
      setDriveResults(
        results.map((item) => ({
          id: item.id,
          name: item.name,
          modifiedTime: item.modifiedTime,
        })),
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to search Drive";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    } finally {
      setIsSearching(false);
    }
  };

  const handleAddFile = async (driveFile: DriveResult) => {
    try {
      setError(null);
      await createFile({
        name: driveFile.name,
        google_drive_id: driveFile.id,
        course_id: courseId,
      });
      const files = await getFilesForCourse(courseId);
      setDocuments(
        files.map((f) => ({
          id: f.id.toString(),
          name: f.name,
          uploadedAt: new Date(f.created_at).toLocaleString(),
        })),
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to add file";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    }
  };

  const handleUpdateCourse = async () => {
    if (!courseNameInput.trim()) {
      setError("Course name cannot be empty");
      return;
    }
    try {
      setError(null);
      const updated = await updateCourse(courseId, { name: courseNameInput.trim() });
      setCourseName(updated.name);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to update course";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    }
  };

  const handleDeleteCourse = async () => {
    if (!confirm("Are you sure you want to delete this course? This cannot be undone.")) {
      return;
    }
    try {
      setError(null);
      await deleteCourse(courseId);
      router.push("/dashboard");
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to delete course";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    }
  };

  const handleSendMessage = async () => {
    if (!chatInput.trim() || !activeSessionId) return;
    const optimistic: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      content: chatInput,
      timestamp: new Date().toLocaleString(),
    };
    setMessages([...messages, optimistic]);
    setChatInput("");

    try {
      setIsSending(true);
      setIsWaitingForAi(true);
      const response = await sendMessage({
        tutor_session_id: activeSessionId,
        message: optimistic.content,
      });
      const refreshedMessages = await getTutorSessionMessages(activeSessionId);
      setMessages(
        refreshedMessages.map((m) => ({
          id: m.id.toString(),
          sender: m.role,
          content: m.message,
          timestamp: new Date(m.created_at).toLocaleString(),
        })),
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to send message";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    } finally {
      setIsSending(false);
      setIsWaitingForAi(false);
    }
  };

  const handleSelectSession = async (sessionId: number) => {
    setActiveSessionId(sessionId);
    try {
      setIsLoadingSessions(true);
      const sessionMessages = await getTutorSessionMessages(sessionId);
      setMessages(
        sessionMessages.map((m) => ({
          id: m.id.toString(),
          sender: m.role,
          content: m.message,
          timestamp: new Date(m.created_at).toLocaleString(),
        })),
      );
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to load session";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    } finally {
      setIsLoadingSessions(false);
    }
  };

  const handleCreateSession = async () => {
    try {
      setIsLoadingSessions(true);
      const title = new Date().toLocaleString();
      const session = await createTutorSession({ course_id: courseId, title });
      setTutorSessions([{ id: session.id, title: session.title }, ...tutorSessions]);
      setActiveSessionId(session.id);
      setMessages([]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Failed to create session";
      setError(message);
      if (err instanceof ApiError && err.status === 401) {
        clearAuthTokens();
        router.push("/login");
        return;
      }
    } finally {
      setIsLoadingSessions(false);
    }
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
              <h1 className="text-2xl font-bold text-gray-900">{courseName}</h1>
              <p className="text-sm text-gray-500">Class ID: {params.id}</p>
            </div>
          </div>

          {/* Tabs */}
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
              <button
                onClick={() => setActiveTab("settings")}
                className={`pb-3 border-b-2 transition-colors ${
                  activeTab === "settings"
                    ? "border-gray-900 text-gray-900 font-medium"
                    : "border-transparent text-gray-500 hover:text-gray-900"
                }`}
              >
                Settings
              </button>
            </div>
          </div>
        </div>

        {error && (
          <div className="mx-8 mt-4 rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Docs Tab Content */}
        {activeTab === "docs" && (
        <div className="flex-1 overflow-auto px-8 py-6 flex flex-col">
          {isLoading ? (
            <div className="flex-1 flex items-center justify-center text-gray-500">
              Loading files...
            </div>
          ) : (
            <>
          {/* Search Bar */}
          <div className="mb-6">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="w-5 h-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search your Google Drive..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-28 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleSearchDrive}
                className="absolute inset-y-0 right-0 flex items-center gap-2 pr-3 text-sm text-gray-700 hover:text-gray-900"
                disabled={isSearching}
              >
                <Search className="w-4 h-4" />
                {isSearching ? "Searching..." : "Search"}
              </button>
            </div>
          </div>

          {/* Documents List */}
          <div className="space-y-3">
            {displayedDocuments.length > 0 ? (
              displayedDocuments.map((doc) => (
                <div
                  key={doc.id}
                  className="flex items-center justify-between p-4 bg-white border border-gray-300 rounded-lg hover:shadow transition-shadow"
                >
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                      <p className="text-xs text-gray-500">Uploaded {doc.uploadedAt}</p>
                    </div>
                  </div>
                  <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors" aria-label="Download">
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
          {/* Drive search results */}
          <div className="mt-8">
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Google Drive results</h3>
            {driveResults.length === 0 ? (
              <p className="text-sm text-gray-500">Use the search button above to find files in your Drive.</p>
            ) : (
              <div className="space-y-3">
                {driveResults.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-center justify-between p-4 bg-white border border-gray-300 rounded-lg hover:shadow transition-shadow"
                  >
                    <div className="flex items-center gap-3">
                      <FileText className="w-5 h-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-900">{file.name}</p>
                        {file.modifiedTime && (
                          <p className="text-xs text-gray-500">Modified {new Date(file.modifiedTime).toLocaleString()}</p>
                        )}
                      </div>
                    </div>
                    <button
                      onClick={() => handleAddFile(file)}
                      className="flex items-center gap-1 px-3 py-1.5 border border-gray-300 rounded-lg text-sm text-gray-800 hover:bg-gray-50"
                    >
                      <Plus className="w-4 h-4" />
                      Add to class
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
          </>
          )}
        </div>
        )}

        {activeTab === "settings" && (
        <div className="flex-1 overflow-auto px-8 py-6 flex flex-col gap-6">
          <div className="max-w-xl space-y-4">
            <h2 className="text-lg font-semibold text-gray-900">Course Settings</h2>
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700" htmlFor="courseName">
                Course name
              </label>
              <input
                id="courseName"
                type="text"
                value={courseNameInput}
                onChange={(e) => setCourseNameInput(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleUpdateCourse}
                className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition-colors text-sm"
              >
                Save changes
              </button>
            </div>

            <div className="pt-4 border-t border-gray-200 space-y-2">
              <h3 className="text-sm font-semibold text-red-600">Danger zone</h3>
              <p className="text-sm text-gray-600">Deleting this course will remove it permanently.</p>
              <button
                onClick={handleDeleteCourse}
                className="px-4 py-2 border border-red-300 text-red-700 rounded-lg hover:bg-red-50 transition-colors text-sm"
              >
                Delete course
              </button>
            </div>
          </div>
        </div>
        )}

        {/* Chat Tab Content */}
        {activeTab === "chat" && (
        <div className="flex-1 overflow-auto px-8 py-6 flex flex-col">
          <div className="flex flex-col h-full gap-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-medium text-gray-900">Tutor Sessions</h2>
              <button
                onClick={handleCreateSession}
                className="px-3 py-1.5 text-sm border border-gray-300 rounded-lg hover:bg-gray-50"
                disabled={isLoadingSessions}
              >
                New Session
              </button>
            </div>

            {/* Session list */}
            <div className="flex gap-3 overflow-x-auto pb-2">
              {tutorSessions.length === 0 ? (
                <p className="text-sm text-gray-500">No sessions yet. Create one to start chatting.</p>
              ) : (
                tutorSessions.map((session) => (
                  <button
                    key={session.id}
                    onClick={() => handleSelectSession(session.id)}
                    className={`px-3 py-2 text-sm rounded-lg border ${
                      activeSessionId === session.id
                        ? "border-gray-900 bg-gray-900 text-white"
                        : "border-gray-300 text-gray-800 bg-white"
                    }`}
                  >
                    {session.title || `Session ${session.id}`}
                  </button>
                ))
              )}
            </div>

            <div className="flex-1 overflow-y-auto space-y-4 bg-white border border-gray-200 rounded-lg p-4">
              {isLoadingSessions ? (
                <p className="text-sm text-gray-500">Loading sessions...</p>
              ) : messages.length === 0 ? (
                <p className="text-sm text-gray-500">No messages yet. Ask a question to begin.</p>
              ) : (
                messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-2xl px-4 py-2 rounded-lg ${
                        msg.sender === "user"
                          ? "bg-gray-900 text-white"
                          : "bg-gray-100 text-gray-900"
                      }`}
                    >
          <div
            className="prose prose-sm dark:prose-invert max-w-none"
            dangerouslySetInnerHTML={{ __html: markdownToHtml(msg.content) }}
          />
                      <p className="text-[10px] opacity-70 mt-1">{msg.timestamp}</p>
                    </div>
                  </div>
                ))
              )}

              {isWaitingForAi && (
                <div className="flex justify-start">
                  <div className="max-w-2xl px-4 py-2 rounded-lg bg-gray-100 text-gray-900">
                    <p className="text-sm flex items-center gap-2">
                      <span className="inline-flex h-2 w-2 rounded-full bg-gray-500 animate-ping" />
                      AI is thinking...
                    </p>
                  </div>
                </div>
              )}
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
                  disabled={!activeSessionId || isSending}
                  className="p-2 bg-white border border-gray-300 text-gray-600 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
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
