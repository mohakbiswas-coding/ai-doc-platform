// frontend/src/pages/ConfigurePage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function ConfigurePage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [docType, setDocType] = useState("docx");
  const [title, setTitle] = useState("");
  const [topic, setTopic] = useState("");
  const [sections, setSections] = useState(["Introduction", "Main Body", "Conclusion"]);
  const [newSection, setNewSection] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggesting, setSuggesting] = useState(false);

  // Add a new section/slide title
  const addSection = () => {
    if (newSection.trim()) {
      setSections([...sections, newSection.trim()]);
      setNewSection("");
    }
  };

  // Remove a section
  const removeSection = (index) => {
    setSections(sections.filter((_, i) => i !== index));
  };

  // Move section up
  const moveUp = (index) => {
    if (index === 0) return;
    const arr = [...sections];
    [arr[index - 1], arr[index]] = [arr[index], arr[index - 1]];
    setSections(arr);
  };

  // AI Suggest Outline (Bonus Feature)
  const suggestOutline = async () => {
    if (!topic.trim()) {
      alert("Please enter a topic first");
      return;
    }
    setSuggesting(true);
    try {
      const res = await api.post("/ai/suggest-outline", { topic, doc_type: docType });
      setSections(res.data.titles);
    } catch (err) {
      alert("Failed to suggest outline. Please try again.");
    } finally {
      setSuggesting(false);
    }
  };

  // Create the project
  const handleCreate = async () => {
    if (!title.trim() || !topic.trim() || sections.length === 0) {
      alert("Please fill all fields and add at least one section.");
      return;
    }
    setLoading(true);
    try {
      const res = await api.post("/projects/", {
        title,
        doc_type: docType,
        topic,
        sections,
      });
      navigate(`/editor/${res.data.id}`);
    } catch (err) {
      alert("Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-600">DocAI</h1>
        <button onClick={() => navigate("/dashboard")} className="text-gray-500 text-sm hover:text-gray-700">
          ← Back to Dashboard
        </button>
      </nav>

      <div className="max-w-2xl mx-auto px-6 py-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Create New Project</h2>

        {/* Step 1: Choose doc type */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-4">
          <h3 className="font-semibold text-gray-700 mb-3">1. Choose Document Type</h3>
          <div className="grid grid-cols-2 gap-3">
            {[
              { value: "docx", label: "📄 Word Document", desc: ".docx" },
              { value: "pptx", label: "📊 PowerPoint", desc: ".pptx" },
            ].map((opt) => (
              <button
                key={opt.value}
                onClick={() => setDocType(opt.value)}
                className={`p-4 rounded-lg border-2 text-left transition ${docType === opt.value
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:border-gray-300"
                  }`}
              >
                <div className="font-semibold">{opt.label}</div>
                <div className="text-sm text-gray-500">{opt.desc}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Step 2: Title and Topic */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-4">
          <h3 className="font-semibold text-gray-700 mb-3">2. Project Details</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-sm text-gray-600 mb-1">Project Title</label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g., EV Market Analysis 2025"
                className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-600 mb-1">Main Topic / Prompt</label>
              <textarea
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., A comprehensive market analysis of the electric vehicle industry in 2025, focusing on growth trends and key players"
                rows={3}
                className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        {/* Step 3: Sections */}
        <div className="bg-white rounded-xl shadow-sm border p-6 mb-6">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-semibold text-gray-700">
              3. {docType === "pptx" ? "Slide Titles" : "Section Headers"}
            </h3>
            <button
              onClick={suggestOutline}
              disabled={suggesting}
              className="text-sm bg-purple-50 text-purple-600 px-3 py-1 rounded-lg hover:bg-purple-100 transition disabled:opacity-50"
            >
              {suggesting ? "Generating..." : "✨ AI Suggest"}
            </button>
          </div>

          <div className="space-y-2 mb-3">
            {sections.map((s, i) => (
              <div key={i} className="flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2">
                <span className="text-gray-400 text-sm w-6">{i + 1}.</span>
                <span className="flex-1 text-gray-700">{s}</span>
                <button onClick={() => moveUp(i)} className="text-gray-400 hover:text-gray-600 text-sm px-1">
                  ↑
                </button>
                <button onClick={() => removeSection(i)} className="text-red-400 hover:text-red-600 text-sm px-1">
                  ✕
                </button>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <input
              type="text"
              value={newSection}
              onChange={(e) => setNewSection(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && addSection()}
              placeholder="Add a new section title..."
              className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={addSection}
              className="bg-gray-100 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
            >
              Add
            </button>
          </div>
        </div>

        <button
          onClick={handleCreate}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded-xl font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {loading ? "Creating..." : "Create Project & Generate Content →"}
        </button>
      </div>
    </div>
  );
}
