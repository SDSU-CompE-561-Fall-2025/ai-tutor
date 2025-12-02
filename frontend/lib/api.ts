const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:3000";

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

export const getStoredAccessToken = () => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("access_token");
  }
  return null;
};
