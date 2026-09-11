import React, { useState, useEffect } from "react";
import {
  Shield,
  MessageSquare,
  FileText,
  Globe,
  ArrowRight,
} from "lucide-react";

export default function App() {
  const [currentView, setCurrentView] = useState<
    "landing" | "assistant" | "tracker"
  >("landing");
  const [language, setLanguage] = useState<"en" | "bn" | "hi">("en");

  // Assistant State
  const [query, setQuery] = useState("");
  const [profile, setProfile] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  // Case Tracker State
  const [caseId, setCaseId] = useState("");
  const [caseData, setCaseData] = useState<any>(null);
  const [caseError, setCaseError] = useState("");

  // Stats counter animation for landing view
  useEffect(() => {
    if (currentView === "landing") {
      const stats = document.querySelectorAll(".stat-value");
      stats.forEach((el, index) => {
        const targets = [120, 99.99, 24, 2.4];
        const suffixes = ["ms", "%", "/7", "M"];
        let current = 0;
        const target = targets[index];
        const step = target / 30;
        const timer = setInterval(() => {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(timer);
          }
          el.textContent =
            (index === 1
              ? current.toFixed(2)
              : index === 3
                ? current.toFixed(1)
                : Math.floor(current)) + suffixes[index];
        }, 40);
      });
    }
  }, [currentView]);

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("query", query);
      formData.append("profile", profile);
      formData.append("language", language);

      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) {
        throw new Error(
          data.detail || `Request failed with status ${res.status}`,
        );
      }
      setResult(data);
    } catch (err) {
      console.error(err);
      alert(
        err instanceof Error
          ? err.message
          : "Failed to connect to backend server.",
      );
    } finally {
      setLoading(false);
    }
  };

  const handleTrackCase = async (e: React.FormEvent) => {
    e.preventDefault();
    const normalizedCaseId = caseId.trim().toUpperCase();
    if (!/^CG-[A-F0-9]{6}$/.test(normalizedCaseId)) {
      setCaseData(null);
      setCaseError("Enter a valid Case ID such as CG-F6AA65.");
      return;
    }

    setCaseId(normalizedCaseId);
    setCaseError("");
    try {
      const res = await fetch(
        `http://localhost:8000/api/cases/${encodeURIComponent(normalizedCaseId)}`,
      );
      const data = await res.json();
      if (!res.ok) {
        throw new Error(
          data.detail || `Request failed with status ${res.status}`,
        );
      }
      setCaseData(data);
    } catch (err) {
      console.error(err);
      setCaseError(err instanceof Error ? err.message : "Case not found.");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans selection:bg-white selection:text-black relative overflow-x-hidden">
      {/* 1. LANDING VIEW (Video Background) */}
      {currentView === "landing" && (
        <div className="relative h-screen h-[100dvh] flex flex-col justify-between p-[clamp(16px,2.4vh,28px)]_clamp(14px,3vw,32px)] overflow-hidden">
          {/* Background Video */}
          <div className="absolute inset-0 bg-black overflow-hidden pointer-events-none z-0">
            <video
              className="absolute inset-0 w-full h-full object-cover"
              autoPlay
              muted
              loop
              playsInline
            >
              <source
                src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260809_012548_ef22562c-c0ae-4816-ad9d-f8922af4e6a7.mp4"
                type="video/mp4"
              />
            </video>
          </div>

          {/* Header */}
          <header className="relative z-10 flex justify-center w-full">
            <div className="flex items-center max-w-[720px] w-full gap-[clamp(18px,2.8vw,28px)]">
              <div className="w-[clamp(40px,4.4vw,46px)] h-[clamp(40px,4.4vw,46px)] bg-white rounded-full flex items-center justify-center shadow-lg">
                <Shield className="w-6 h-6 text-black" />
              </div>
              <nav className="hidden md:flex items-center justify-around bg-white h-[clamp(44px,5.2vw,48px)] max-w-[430px] flex-1 px-4 rounded-full shadow-lg">
                <button
                  onClick={() => setCurrentView("landing")}
                  className="text-[#2e2e2e] font-medium text-sm opacity-100"
                >
                  Home
                </button>
                <button
                  onClick={() => setCurrentView("assistant")}
                  className="text-[#2e2e2e] font-medium text-sm opacity-50 hover:opacity-75"
                >
                  Assistant
                </button>
                <button
                  onClick={() => setCurrentView("tracker")}
                  className="text-[#2e2e2e] font-medium text-sm opacity-50 hover:opacity-75"
                >
                  Case Tracker
                </button>
              </nav>
              <button
                onClick={() => setCurrentView("assistant")}
                className="hidden md:flex items-center justify-center bg-[#28282a] text-[#c8c8c8] h-[clamp(44px,5.2vw,48px)] px-6 rounded-full font-medium text-sm hover:bg-[#323234] hover:text-white transition-all"
              >
                Launch App
              </button>
            </div>
          </header>

          {/* Hero */}
          <main className="relative z-10 flex-1 flex flex-col items-center justify-center text-center max-w-[900px] mx-auto w-full">
            <div className="inline-flex items-center mb-6">
              <span className="text-xs uppercase tracking-widest px-4 py-1.5 rounded-full bg-[#28282a] border border-white/20 text-[#c4c2c3]">
                AI-Powered Public-Service Navigator
              </span>
            </div>

            <h1 className="font-display font-normal text-white text-[clamp(32px,6.2vw,80px)] tracking-tighter leading-[1.12] mb-5">
              <span className="block">Intelligence</span>
              <span className="block">Designed To Evolve</span>
            </h1>

            <p className="font-sans font-normal text-[#d0d0d0]/80 text-[clamp(14px,1.5vw,17px)] leading-[1.55] max-w-[500px] mb-8">
              Build applications that reason, adapt and collaborate using a
              modular AI platform designed for public service and enterprise
              scale.
            </p>

            <button
              onClick={() => setCurrentView("assistant")}
              className="inline-flex items-center gap-2 bg-white text-black font-semibold text-[14px] px-7 py-3 rounded-full shadow-[0_0_22px_rgba(255,255,255,0.32)] hover:scale-105 transition-transform"
            >
              Get Started <ArrowRight className="w-4 h-4" />
            </button>
          </main>

          {/* Stats Footer */}
          <footer className="relative z-10 w-full max-w-[920px] mx-auto">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-left">
              <div className="flex flex-col">
                <span className="font-display text-xl text-white">&lt;</span>
                <span className="stat-value font-semibold text-lg">120ms</span>
                <span className="text-xs text-[#8e8e8e]">Inference Time</span>
              </div>
              <div className="flex flex-col">
                <span className="font-display text-xl text-white">%</span>
                <span className="stat-value font-semibold text-lg">99.99%</span>
                <span className="text-xs text-[#8e8e8e]">Platform Uptime</span>
              </div>
              <div className="flex flex-col">
                <span className="font-display text-xl text-white">*</span>
                <span className="stat-value font-semibold text-lg">24/7</span>
                <span className="text-xs text-[#8e8e8e]">
                  Autonomous Runtime
                </span>
              </div>
              <div className="flex flex-col">
                <span className="font-display text-xl text-white">#</span>
                <span className="stat-value font-semibold text-lg">2.4M</span>
                <span className="text-xs text-[#8e8e8e]">Context Windows</span>
              </div>
            </div>
          </footer>
        </div>
      )}

      {/* 2. APP VIEW (Assistant & Case Tracker Dashboard) */}
      {currentView !== "landing" && (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col">
          {/* Top Navbar */}
          <header className="bg-slate-900 border-b border-slate-800 px-6 py-4 flex items-center justify-between">
            <div
              className="flex items-center gap-3 cursor-pointer"
              onClick={() => setCurrentView("landing")}
            >
              <div className="w-9 h-9 bg-blue-600 rounded-lg flex items-center justify-center">
                <Shield className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg tracking-tight">
                CivicGuide AI
              </span>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={() => setCurrentView("assistant")}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${currentView === "assistant" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                <MessageSquare className="w-4 h-4" /> Assistant
              </button>
              <button
                onClick={() => setCurrentView("tracker")}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${currentView === "tracker" ? "bg-blue-600 text-white" : "text-slate-400 hover:text-white"}`}
              >
                <FileText className="w-4 h-4" /> Case Tracker
              </button>

              {/* Language Selector */}
              <div className="flex items-center gap-2 bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <Globe className="w-4 h-4 text-slate-400" />
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value as any)}
                  className="bg-transparent text-sm text-slate-200 outline-none cursor-pointer"
                >
                  <option value="en">English</option>
                  <option value="bn">বাংলা (Bengali)</option>
                  <option value="hi">हिंदी (Hindi)</option>
                </select>
              </div>
            </div>
          </header>

          {/* Main Dashboard Content */}
          <main className="flex-1 max-w-6xl w-full mx-auto p-6">
            {currentView === "assistant" && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Input Form */}
                <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800">
                  <h2 className="text-xl font-semibold mb-4">
                    Describe Your Need
                  </h2>
                  <form onSubmit={handleChatSubmit} className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-slate-400 mb-1">
                        Your Problem / Goal
                      </label>
                      <textarea
                        rows={3}
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="e.g., I want to start a micro-business and need financial assistance"
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-slate-400 mb-1">
                        Your Profile Details (Age, Income, etc.)
                      </label>
                      <input
                        type="text"
                        value={profile}
                        onChange={(e) => setProfile(e.target.value)}
                        placeholder="e.g., 28 years old, unemployed student"
                        className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-white text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 rounded-xl transition-all flex items-center justify-center gap-2"
                    >
                      {loading
                        ? "Processing via Groq & Gemini..."
                        : "Get AI Guidance"}
                    </button>
                  </form>
                </div>

                {/* Recommendations Output */}
                <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 flex flex-col">
                  <h2 className="text-xl font-semibold mb-4">
                    CivicGuide Recommendations & Assessment
                  </h2>
                  <div className="flex-1 bg-slate-950 rounded-xl p-4 border border-slate-800 overflow-y-auto">
                    {result ? (
                      <div className="space-y-4 text-sm">
                        <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                          <h3 className="font-semibold text-blue-400 mb-1">
                            Service Recommendation
                          </h3>
                          <p className="text-slate-300 whitespace-pre-wrap">
                            {result.service_recommendation}
                          </p>
                        </div>
                        <div className="p-3 bg-slate-900 rounded-lg border border-slate-800">
                          <h3 className="font-semibold text-emerald-400 mb-1">
                            Eligibility Assessment
                          </h3>
                          <p className="text-slate-300 whitespace-pre-wrap">
                            {result.eligibility_assessment}
                          </p>
                        </div>
                      </div>
                    ) : (
                      <div className="h-full flex flex-col items-center justify-center text-slate-500 text-center">
                        <MessageSquare className="w-10 h-10 mb-2 opacity-40" />
                        <p>
                          Submit your inquiry to receive AI-powered service
                          matching and eligibility reviews.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {currentView === "tracker" && (
              <div className="max-w-xl mx-auto bg-slate-900 p-6 rounded-2xl border border-slate-800">
                <h2 className="text-xl font-semibold mb-4">
                  Track Existing Case ("What is left?")
                </h2>
                <form onSubmit={handleTrackCase} className="flex gap-3 mb-6">
                  <input
                    type="text"
                    value={caseId}
                    onChange={(e) => setCaseId(e.target.value)}
                    placeholder="Enter Case ID (e.g., CG-F6AA65)"
                    className="flex-1 bg-slate-950 border border-slate-800 rounded-xl p-3 text-white text-sm outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                  <button
                    type="submit"
                    className="bg-blue-600 hover:bg-blue-500 px-6 py-3 rounded-xl font-semibold text-sm"
                  >
                    Search
                  </button>
                </form>

                {caseError && (
                  <p className="mb-6 text-sm text-rose-400" role="alert">
                    {caseError}
                  </p>
                )}

                {caseData && (
                  <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-400 text-sm">Status:</span>
                      <span className="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-full text-xs font-semibold">
                        {caseData.status}
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-400 text-sm block mb-1">
                        Missing Documents / Next Steps:
                      </span>
                      <p className="text-slate-200 text-sm bg-slate-900 p-3 rounded-lg">
                        {caseData.missing_documents ||
                          "All requirements satisfied!"}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}
          </main>
        </div>
      )}
    </div>
  );
}
