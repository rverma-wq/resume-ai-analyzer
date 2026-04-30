import React, { useState } from "react";
import axios from "axios";
import "./App.css";
import { motion, AnimatePresence } from "framer-motion";
import {
  UploadCloud,
  FileText,
  Briefcase,
  Sparkles,
  CheckCircle2,
  Loader2,
  ShieldCheck,
  ArrowRight,
} from "lucide-react";

console.log("ENV:", process.env.REACT_APP_API_URL);
function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (selectedFile) => {
    if (!selectedFile) return;
    setFile(selectedFile);
    setResults([]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Upload a resume first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      setResults([]);

      const API_URL = "https://resume-ai-analyzer-backend-6fz3.onrender.com";

      const response = await axios.post(`${API_URL}/predict`, formData);


      setResults(response.data.top_matches || []);
    } catch (error) {
      console.error(error);
      alert("Server error. Please check backend.");
    } finally {
      setLoading(false);
    }
  };
  const onDrop = (e) => {
    e.preventDefault();
    setDragActive(false);

    const droppedFile = e.dataTransfer.files?.[0];
    handleFileChange(droppedFile);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(59,130,246,0.18),transparent_30%),radial-gradient(circle_at_bottom_right,rgba(99,102,241,0.16),transparent_30%)]" />
      <div className="absolute inset-0 bg-grid-white/[0.03] bg-[size:32px_32px]" />

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12 md:py-20">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left */}
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="max-w-xl"
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300 mb-6 backdrop-blur">
              <Sparkles className="w-4 h-4 text-blue-400" />
              AI-powered resume analysis
            </div>

            <h1 className="text-4xl md:text-6xl font-bold leading-tight tracking-tight">
              Make resume screening
              <span className="block bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                smarter and faster
              </span>
            </h1>

            <p className="mt-6 text-lg text-slate-300 leading-8">
              Upload a resume and get an instant AI-based prediction of the
              most suitable career domain. Clean, fast, and built for a modern
              hiring workflow.
            </p>

            <div className="mt-8 grid sm:grid-cols-2 gap-4">
              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <div className="flex items-center gap-3 mb-2">
                  <Briefcase className="w-5 h-5 text-blue-400" />
                  <h3 className="font-semibold">Career Insight</h3>
                </div>
                <p className="text-sm text-slate-400">
                  Predict the most relevant job domain from resume content.
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur">
                <div className="flex items-center gap-3 mb-2">
                  <ShieldCheck className="w-5 h-5 text-indigo-400" />
                  <h3 className="font-semibold">Simple Workflow</h3>
                </div>
                <p className="text-sm text-slate-400">
                  Upload, analyze, and review results in just a few seconds.
                </p>
              </div>
            </div>


          </motion.div>

          {/* Right */}
          <motion.div
            initial={{ opacity: 0, y: 28 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.55, delay: 0.1 }}
            className="w-full"
          >
            <div className="rounded-3xl border border-white/10 bg-white/8 backdrop-blur-2xl shadow-2xl shadow-black/30 p-6 md:p-8">
              <div className="mb-6">
                <h2 className="text-2xl font-semibold">Upload Resume</h2>
                <p className="text-slate-400 mt-2 text-sm">
                  Supported formats: PDF, DOC, DOCX. Upload a candidate resume
                  to get an instant career-domain prediction.
                </p>
              </div>

              <input
                id="fileUpload"
                type="file"
                accept=".pdf,.doc,.docx"
                className="hidden"
                onChange={(e) => handleFileChange(e.target.files?.[0])}
              />

              <div
                onClick={() => document.getElementById("fileUpload").click()}
                onDragOver={(e) => {
                  e.preventDefault();
                  setDragActive(true);
                }}
                onDragLeave={() => setDragActive(false)}
                onDrop={onDrop}
                className={`group rounded-2xl border-2 border-dashed p-8 md:p-10 text-center cursor-pointer transition-all duration-300 ${dragActive
                  ? "border-blue-400 bg-blue-500/10"
                  : "border-slate-700 hover:border-blue-400 hover:bg-white/5"
                  }`}
              >
                <div className="mx-auto w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-indigo-500/20 flex items-center justify-center mb-5">
                  <UploadCloud className="w-8 h-8 text-blue-400" />
                </div>

                <h3 className="text-lg font-semibold">
                  Drag & drop your resume here
                </h3>
                <p className="text-slate-400 text-sm mt-2">
                  or click to browse files from your computer
                </p>

                <div className="mt-5 inline-flex items-center gap-2 rounded-full bg-white/5 border border-white/10 px-4 py-2 text-xs text-slate-300">
                  <FileText className="w-4 h-4" />
                  PDF, DOC, DOCX
                </div>

                {file && (
                  <div className="mt-6 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 px-4 py-3 flex items-center justify-center gap-3 text-emerald-300">
                    <CheckCircle2 className="w-5 h-5" />
                    <span className="text-sm font-medium truncate max-w-[240px]">
                      {file.name}
                    </span>
                  </div>
                )}
              </div>

              <button
                onClick={handleUpload}
                disabled={loading}
                className="w-full mt-6 rounded-2xl bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 px-5 py-4 font-semibold shadow-lg shadow-blue-900/30 transition-all duration-300 disabled:opacity-60 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Analyzing Resume...
                  </>
                ) : (
                  <>
                    Analyze Resume
                    <ArrowRight className="w-5 h-5" />
                  </>
                )}
              </button>

              <AnimatePresence>
                {results.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 18 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 18 }}
                    transition={{ duration: 0.35 }}
                    className="mt-6 rounded-2xl border border-blue-500/20 bg-gradient-to-br from-blue-500/10 to-indigo-500/10 p-6"
                  >
                    <p className="text-sm uppercase tracking-[0.2em] text-slate-400 mb-2">
                      Prediction Result
                    </p>
                    <h3 className="text-3xl font-bold text-blue-400">
                      {results[0].job} - {results[0].score}%
                    </h3>
                    <p className="mt-3 text-sm text-slate-300">
                      Based on the uploaded resume, this appears to be the most
                      suitable career domain predicted by the model.
                    </p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

export default App;