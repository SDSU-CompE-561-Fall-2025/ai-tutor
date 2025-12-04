"use client";
import React from "react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Loader } from "@/components/ui/loader";
import { login } from "@/lib/api";
import Image from "next/image";

const page = () => {
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await login(email, password);
      // Store access token from login response
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("token_type", data.token_type);
      localStorage.setItem("email", email);
      
      // Redirect to dashboard
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message);
      setLoading(false);
    }
  };
  return (
    <div className="flex min-h-screen flex-col bg-background">
      <header className="sticky top-0 z-10 w-full border-b bg-background/95 backdrop-blur">
        <div className="w-full flex h-16 items-center justify-between py-4">
          <div
            className="flex items-center gap-1 font-bold text-xl hover:cursor-pointer"
            onClick={() => router.push("/")}
          >
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary">
              AI
            </div>
            <span> Tutor</span>
            <Image src="/logo.png" alt="AI Tutor Logo" width={68} height={68} />
          </div>
          <nav className="flex flex-end gap-6 text-sm font-medium text-muted-foreground px-4 mr-1">
            <a href="/login" className="hover:font-bold">
              Log In
            </a>
            <a href="/signup" className="hover:font-bold">
              Sign Up
            </a>
          </nav>
        </div>
      </header>
      {/* Sign Up FORM */}
      <main className="flex-1 mt-10 px-4 py-8">
        <div className="container mx-auto flex flex-col items-center justify-center min-h-[500px]">
          <div className="w-full max-w-md border-2 border-gray-900 rounded-2xl p-8 bg-white">
            <h1 className="text-2xl font-bold mb-2">Log in to your account</h1>
            <p className="text-sm text-gray-600 mb-6">
              Enter your email below to log in to your account
            </p>

            <form className="space-y-4" onSubmit={handleSubmit}>
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-900 mb-2"
                >
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  className="w-full px-4 py-2 border-2 border-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="m@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-900 mb-2"
                >
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  className="w-full px-4 py-2 border-2 border-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>

              <button
                type="submit"
                disabled={!email || !password || loading}
                className={`w-full bg-gray-900 text-white py-2 px-4 rounded-lg font-semibold transition mt-6 ${
                  !email || !password || loading
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:bg-gray-800"
                }`}
              >
                Log In
              </button>
              {error && (
                <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}
            </form>
            {loading && <Loader className="mt-2" />}

            <div className="mt-4 text-center text-sm text-gray-600">
              Don't have an account?{" "}
              <a
                href="/signup"
                className="text-primary font-semibold hover:underline"
              >
                Sign up
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default page;
