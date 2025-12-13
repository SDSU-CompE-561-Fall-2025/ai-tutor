"use client";
import { Suspense, useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Loader } from "@/components/ui/loader";
import { register, storeAuthTokens } from "@/lib/api";
import Image from "next/image";
import { useDarkMode } from "@/contexts/DarkModeContext";

const SignupContent = () => {
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [loading, setLoading] = useState(false);
  const [passwordError, setPasswordError] = useState("");
  const { isDark, toggleDarkMode } = useDarkMode();
  const router = useRouter();
  const searchParams = useSearchParams();

  const validatePassword = (pwd: string) => {
    if (pwd.length < 8) return "Password must be at least 8 characters";
    if (pwd.length > 20) return "Password must be no more than 20 characters";
    if (!/[0-9]/.test(pwd)) return "Password must include at least 1 number";
    if (!/[a-zA-Z]/.test(pwd)) return "Password must include at least 1 letter";
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(pwd)) return "Password must include at least 1 special character";
    return "";
  };

  // Handle OAuth callback from Google
  useEffect(() => {
    const accessToken = searchParams.get("access_token");
    const refreshToken = searchParams.get("refresh_token");
    const expiry = searchParams.get("expiry");
    const userEmail = searchParams.get("email");
    const jwtToken = searchParams.get("jwt_token");
    const tokenType = searchParams.get("token_type");

    if (accessToken && refreshToken && expiry && userEmail && jwtToken) {
      // Store tokens from OAuth callback - use JWT token as the access_token for API calls
      storeAuthTokens({
        access_token: jwtToken,
        refresh_token: refreshToken,
        expiry: expiry,
        email: userEmail,
      });
      if (tokenType) {
        localStorage.setItem("token_type", tokenType);
      }
      // Mark setup as complete and redirect to dashboard
      localStorage.setItem("google_drive_setup_complete", "true");
      router.push("/dashboard");
    }
  }, [searchParams, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Validate password
    const pwdError = validatePassword(password);
    if (pwdError) {
      setError(pwdError);
      setLoading(false);
      return;
    }

    try {
      const data = await register(email, password, firstName, lastName);
      // Register returns a redirect_url for Google OAuth
      if (data.redirect_url) {
        window.location.href = data.redirect_url;
      } else {
        router.push("/dashboard");
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "An error occurred");
      setLoading(false);
    }
  };
  return (
    <div
      className={`flex min-h-screen flex-col ${
        isDark ? "bg-gray-800 text-white" : "bg-background"
      }`}
    >
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
          <nav
            className={`flex flex-end gap-6 text-sm font-medium px-4 mr-1 items-center ${
              isDark ? "text-white" : "text-muted-foreground"
            }`}
          >
            <button
              onClick={toggleDarkMode}
              className="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 rounded-lg font-semibold transition-colors"
            >
              {isDark ? "Light Mode" : "Dark Mode"}
            </button>
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
          <div
            className={`w-full max-w-md border-2 ${
              isDark
                ? "border-gray-600 bg-gray-700"
                : "border-gray-900 bg-white"
            } rounded-2xl p-8`}
          >
            <h1
              className={`text-2xl font-bold mb-2 ${
                isDark ? "text-white" : ""
              }`}
            >
              Create an account
            </h1>
            <p
              className={`text-sm mb-6 ${
                isDark ? "text-white" : "text-gray-600"
              }`}
            >
              Enter your email below to create your account
            </p>

            <form className="space-y-4" onSubmit={handleSubmit}>
              <div>
                <label
                  htmlFor="email"
                  className={`block text-sm font-medium mb-2 ${
                    isDark ? "text-white" : "text-gray-900"
                  }`}
                >
                  Email
                  <span className="text-xs text-gray-500 ml-2">(max 30 characters)</span>
                </label>
                <input
                  type="email"
                  id="email"
                  maxLength={30}
                  className={`w-full px-4 py-2 border-2 ${
                    isDark
                      ? "border-gray-500 bg-gray-600 text-white"
                      : "border-gray-900"
                  } rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent`}
                  placeholder="m@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label
                    htmlFor="firstName"
                    className={`block text-sm font-medium mb-2 ${
                      isDark ? "text-white" : "text-gray-900"
                    }`}
                  >
                    First Name
                    <span className="text-xs text-gray-500 ml-2">(max 15 chars)</span>
                  </label>
                  <input
                    type="text"
                    id="firstName"
                    maxLength={15}
                    className={`w-full px-4 py-2 border-2 ${
                      isDark
                        ? "border-gray-500 bg-gray-600 text-white"
                        : "border-gray-900"
                    } rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent`}
                    placeholder="John"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                  />
                </div>
                <div>
                  <label
                    htmlFor="lastName"
                    className={`block text-sm font-medium mb-2 ${
                      isDark ? "text-white" : "text-gray-900"
                    }`}
                  >
                    Last Name
                    <span className="text-xs text-gray-500 ml-2">(max 15 chars)</span>
                  </label>
                  <input
                    type="text"
                    id="lastName"
                    maxLength={15}
                    className={`w-full px-4 py-2 border-2 ${
                      isDark
                        ? "border-gray-500 bg-gray-600 text-white"
                        : "border-gray-900"
                    } rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent`}
                    placeholder="Doe"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="password"
                  className={`block text-sm font-medium mb-2 ${
                    isDark ? "text-white" : "text-gray-900"
                  }`}
                >
                  Password
                </label>
                <div className="mb-2 text-xs text-gray-500 space-y-1">
                  <p>Password must:</p>
                  <ul className="list-disc list-inside space-y-0.5">
                    <li className={password.length >= 8 && password.length <= 20 ? "text-green-600" : ""}>
                      Be 8-20 characters long
                    </li>
                    <li className={/[0-9]/.test(password) ? "text-green-600" : ""}>
                      Include at least 1 number
                    </li>
                    <li className={/[a-zA-Z]/.test(password) ? "text-green-600" : ""}>
                      Include at least 1 letter
                    </li>
                    <li className={/[!@#$%^&*(),.?":{}|<>]/.test(password) ? "text-green-600" : ""}>
                      Include at least 1 special character (!@#$%^&*...)
                    </li>
                  </ul>
                </div>
                {passwordError && (
                  <p className="text-xs text-red-600 mb-2">{passwordError}</p>
                )}
                <input
                  type="password"
                  id="password"
                  className={`w-full px-4 py-2 border-2 ${
                    isDark
                      ? "border-gray-500 bg-gray-600 text-white"
                      : "border-gray-900"
                  } rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent`}
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setPasswordError(validatePassword(e.target.value));
                  }}
                  required
                  minLength={8}
                  maxLength={20}
                />
              </div>

              <p className={`text-xs mt-4 ${
                isDark ? "text-gray-400" : "text-gray-600"
              }`}>
                📌 After signup, you'll be redirected to Google Sign-In to connect your Google Drive account.
              </p>

              <button
                type="submit"
                disabled={
                  !email || !password || !firstName || !lastName || loading
                }
                className={`w-full bg-gray-900 text-white py-2 px-4 rounded-lg font-semibold transition mt-4 ${
                  !email || !password || !firstName || !lastName || loading
                    ? "opacity-50 cursor-not-allowed"
                    : "hover:bg-gray-800"
                }`}
              >
                Sign Up
              </button>
              {loading && <Loader className="mt-2 mx-auto" />}
            </form>
            {error && <p className="text-red-500 mt-2 text-center">{error}</p>}

            <div
              className={`mt-4 text-center text-sm ${
                isDark ? "text-white" : "text-gray-600"
              }`}
            >
              Already have an account?{" "}
              <a
                href="/login"
                className="text-primary font-semibold hover:underline"
              >
                Log in
              </a>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

const Page = () => {
  return (
    <Suspense fallback={<Loader />}>
      <SignupContent />
    </Suspense>
  );
};

export default Page;
