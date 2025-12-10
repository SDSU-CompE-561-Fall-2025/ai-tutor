"use client";
import Image from "next/image";
import Link from "next/link";
import { ButtonColorful } from "@/components/ui/button-colorful";
import { useRouter } from "next/navigation";
import { SplineScene } from "@/components/ui/splite";
import { useDarkMode } from "@/hooks/useDarkMode";
export default function Home() {
  const router = useRouter();
  const { isDark, toggleDarkMode } = useDarkMode();
  return (
    <div
      className={`flex min-h-screen flex-col ${
        isDark ? "bg-gray-800 text-white" : "bg-background"
      }`}
    >
      {/* Header / Navbar Section */}
      <header className="sticky top-0 z-10 w-full border-b bg-background/95 backdrop-blur">
        <div className="w-full flex h-16 items-center justify-between py-4">
          <div className="flex items-center gap-1 font-bold text-xl">
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
            <Link href="/login" className="hover:font-bold">
              Log In
            </Link>
            <Link href="/signup" className="hover:font-bold">
              Sign Up
            </Link>
          </nav>
        </div>
      </header>
      {/* Main Content Section */}
      <main className="flex-1 mt-10 px-4  py-8">
        <section className="space-y-6 pb-8 pt-6 md:pt-10 md:pb-12">
          {/* Ai Plug  */}
          <div className="container flex mx-auto flex-col items-center gap-4 mt-10">
            <div className="rounded-2xl bg-muted px-4 py-1.5 text-sm font-medium">
              Powered by Google Drive MCP
            </div>
          </div>
          {/* Main Hero Section */}
          <div className="container flex mx-auto flex-col items-center text-center gap-6 px-10 mt-20">
            <h1
              className={`font-heading text-7xl lg:text-12xl font-bold text-balance tracking-tight px-12 ${
                isDark ? "text-white" : ""
              }`}
            >
              Master anything with your personal AI Tutor
            </h1>
            <p
              className={`text-balance leading-normal ${
                isDark ? "text-white" : "text-muted"
              }`}
            >
              Gain personalized insights, resources, and support to excel in
              your classes, now supporting{" "}
              <span className="font-bold">Google Drive</span> connection for the
              ultimate learning experience. Make learning personalized and never
              fail a class again!
            </p>
            {/* buttons in hero */}
            <div className="flex flex-row items-center gap-10">
              <ButtonColorful
                label="Get Started"
                className="dark hover:cursor-pointer"
                onClick={() => {
                  router.push("/signup");
                }}
              />
              <ButtonColorful
                label="See Demo"
                className="dark hover:cursor-pointer"
                onClick={() => {
                  router.push("https://youtu.be/ihNwD7CMXH0");
                }}
              />
            </div>
          </div>
        </section>
        {/* features section */}
        <section className="container mx-auto py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div
              className={`p-6 border rounded-lg hover:shadow-lg transition-shadow ${
                isDark ? "border-gray-600" : ""
              }`}
            >
              <h3
                className={`text-xl font-semibold mb-2 ${
                  isDark ? "text-white" : ""
                }`}
              >
                Personalized Learning
              </h3>
              <p className={isDark ? "text-white" : ""}>
                Tailored study plans and resources to fit your unique learning
                style and pace.
              </p>
            </div>
            <div
              className={`p-6 border rounded-lg hover:shadow-lg transition-shadow ${
                isDark ? "border-gray-600" : ""
              }`}
            >
              <h3
                className={`text-xl font-semibold mb-2 ${
                  isDark ? "text-white" : ""
                }`}
              >
                AI-Powered Assistance
              </h3>
              <p className={isDark ? "text-white" : ""}>
                Get instant help with difficult concepts and assignments using
                advanced AI technology.
              </p>
            </div>
            <div
              className={`p-6 border rounded-lg hover:shadow-lg transition-shadow ${
                isDark ? "border-gray-600" : ""
              }`}
            >
              <h3
                className={`text-xl font-semibold mb-2 ${
                  isDark ? "text-white" : ""
                }`}
              >
                Google Drive Integration
              </h3>
              <p className={isDark ? "text-white" : ""}>
                Seamlessly connect your Google Drive to access and manage your
                study materials in one place.
              </p>
            </div>
          </div>
        </section>

        <section className="container mx-auto py-8">
          <div className="bg-white/5 p-6 rounded-lg border border-white/10 transition-shadow">
            <h2
              className={`text-2xl mb-4 text-center ${
                isDark ? "text-white" : "text-black"
              }`}
            >
              Experience the Future of Learning
            </h2>
            <SplineScene
              scene="https://prod.spline.design/kZDDjO5HuC9GJUM2/scene.splinecode"
              className="w-full h-full hover:shadow-none"
            />
          </div>
        </section>
      </main>
    </div>
  );
}
