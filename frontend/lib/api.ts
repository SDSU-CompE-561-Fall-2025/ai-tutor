const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";

type Course = {
  id: number;
  name: string;
};

type FileResponse = {
  id: number;
  name: string;
  google_drive_id?: string | null;
  course_name: string;
  created_at: string;
};

type FileCreate = {
  name: string;
  google_drive_id: string;
  course_id: number;
};

type DriveFile = {
  id: string;
  name: string;
  mimeType?: string;
  modifiedTime?: string;
};

type TutorSession = {
  id: number;
  title: string | null;
  course_name: string;
  created_at: string;
};

type ChatMessage = {
  id: number;
  role: "user" | "assistant";
  message: string;
  tutor_session_title?: string | null;
  created_at: string;
};

type UserProfile = {
  id: number;
  email: string;
};

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export const getStoredAccessToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
};

export const clearAuthTokens = () => {
  if (typeof window !== "undefined") {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("expiry");
    localStorage.removeItem("email");
  }
};

const buildAuthHeaders = (headers?: HeadersInit) => {
  const token = getStoredAccessToken();
  if (!token) {
    throw new Error("Not authenticated");
  }

  const merged = new Headers(headers);
  merged.set("Authorization", `Bearer ${token}`);
  merged.set("Accept", "application/json");
  return merged;
};

const handleResponse = async <T>(response: Response) => {
  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`;
    try {
      const data = await response.json();
      errorMessage = data.detail || data.message || errorMessage;
    } catch (err) {
      console.error("Failed to parse error response", err);
    }
    throw new ApiError(errorMessage, response.status);
  }
  return response.json() as Promise<T>;
};

export const login = async (email: string, password: string) => {
  try {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    const response = await fetch(`${API_URL}/api/v1/user/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || "Login failed");
    }
    return response.json();
  } catch (error) {
    console.error("Login error:", error);
    throw error;
  }
};

export const register = async (email: string, password: string) => {
  try {
    const response = await fetch(`${API_URL}/api/v1/user/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.message || "Registration failed");
    }
    return response.json();
  } catch (error) {
    console.error("Registration error:", error);
    throw error;
  }
};

export const getCourses = async (): Promise<Course[]> => {
  const headers = buildAuthHeaders();
  const response = await fetch(`${API_URL}/api/v1/courses/`, {
    method: "GET",
    headers,
  });

  return handleResponse<Course[]>(response);
};

export const createCourse = async (course: { name: string }): Promise<Course> => {
  const headers = buildAuthHeaders({ "Content-Type": "application/json" });
  const response = await fetch(`${API_URL}/api/v1/courses/`, {
    method: "POST",
    headers,
    body: JSON.stringify(course),
  });

  return handleResponse<Course>(response);
};

export const updateCourse = async (
  courseId: number,
  course: { name: string },
): Promise<Course> => {
  const headers = buildAuthHeaders({ "Content-Type": "application/json" });
  const response = await fetch(`${API_URL}/api/v1/courses/${courseId}`, {
    method: "PUT",
    headers,
    body: JSON.stringify(course),
  });

  return handleResponse<Course>(response);
};

export const deleteCourse = async (courseId: number): Promise<void> => {
  const headers = buildAuthHeaders();
  const response = await fetch(`${API_URL}/api/v1/courses/${courseId}`, {
    method: "DELETE",
    headers,
  });

  await handleResponse<void>(response);
};

export const getCurrentUser = async (): Promise<UserProfile> => {
  const headers = buildAuthHeaders();
  const response = await fetch(`${API_URL}/api/v1/user/me`, {
    method: "GET",
    headers,
  });

  return handleResponse<UserProfile>(response);
};

export const getCourseById = async (courseId: number): Promise<Course> => {
  const headers = buildAuthHeaders();
  const response = await fetch(`${API_URL}/api/v1/courses/${courseId}`, {
    method: "GET",
    headers,
  });

  return handleResponse<Course>(response);
};

export const getFilesForCourse = async (
  courseId: number,
): Promise<FileResponse[]> => {
  const headers = buildAuthHeaders();
  const response = await fetch(`${API_URL}/api/v1/files/course/${courseId}`, {
    method: "GET",
    headers,
  });

  return handleResponse<FileResponse[]>(response);
};

export const createFile = async (payload: FileCreate): Promise<FileResponse> => {
  const headers = buildAuthHeaders({ "Content-Type": "application/json" });
  const response = await fetch(`${API_URL}/api/v1/files/`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });

  return handleResponse<FileResponse>(response);
};

export const searchDrive = async (query?: string): Promise<DriveFile[]> => {
  const headers = buildAuthHeaders();
  const url = new URL(`${API_URL}/api/v1/drive/search/`);
  if (query) {
    url.searchParams.append("query", query);
  }

  const response = await fetch(url.toString(), {
    method: "GET",
    headers,
  });

  return handleResponse<DriveFile[]>(response);
};

export const getTutorSessionsByCourse = async (
  courseId: number,
): Promise<TutorSession[]> => {
  const headers = buildAuthHeaders();
  const response = await fetch(`${API_URL}/api/v1/courses/${courseId}/tutor-sessions`, {
    method: "GET",
    headers,
  });

  return handleResponse<TutorSession[]>(response);
};

export const createTutorSession = async (
  payload: { course_id: number; title?: string | null },
): Promise<TutorSession> => {
  const headers = buildAuthHeaders({ "Content-Type": "application/json" });
  const response = await fetch(`${API_URL}/api/v1/tutor-session/chat`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      course_id: payload.course_id,
      title: payload.title ?? "New Session",
    }),
  });

  return handleResponse<TutorSession>(response);
};

export const getTutorSessionMessages = async (
  tutorSessionId: number,
): Promise<ChatMessage[]> => {
  const headers = buildAuthHeaders();
  const response = await fetch(
    `${API_URL}/api/v1/tutor-session/${tutorSessionId}/messages`,
    {
      method: "GET",
      headers,
    },
  );

  return handleResponse<ChatMessage[]>(response);
};

export const sendMessage = async (
  payload: { tutor_session_id: number; message: string },
): Promise<ChatMessage> => {
  const headers = buildAuthHeaders({ "Content-Type": "application/json" });
  const response = await fetch(`${API_URL}/api/v1/chat-messages/`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      tutor_session_id: payload.tutor_session_id,
      message: payload.message,
      role: "user",
    }),
  });

  return handleResponse<ChatMessage>(response);
};

export const storeAuthTokens = (tokens: {
  access_token: string;
  refresh_token: string;
  expiry: string;
  email: string;
}) => {
  localStorage.setItem("access_token", tokens.access_token);
  localStorage.setItem("refresh_token", tokens.refresh_token);
  localStorage.setItem("expiry", tokens.expiry);
  localStorage.setItem("email", tokens.email);
};
