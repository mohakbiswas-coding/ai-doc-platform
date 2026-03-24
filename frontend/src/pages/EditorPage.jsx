// frontend/src/pages/EditorPage.jsx
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";
import SectionCard from "../components/SectionCard";

export default function EditorPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [sections, setSections] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProject();
  }, [projectId]);

  const fetchProject = async () => {
    try {
      const res = await api.get(`/projects/${projectId}`);
      setProject(res.data);
      setSections(res.data.sections.sort((a, b) => a.order_index - b.order_index));
    } catch (err) {
      alert("Failed to load project");
      navigate("/dashboard");
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateAll = async () => {
    const hasContent = sections.some((s) => s.content);
    if (hasContent && !confirm("Regenerate all content? This will overwrite existing content.")) {
      return;
    }
    setGenerating(true);
    try {
      await api.post(`/ai/generate/${projectId}`);
      await fetchProject(); // Reload with new content
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || "Generation failed. Check your API key.";
      alert(`Generation failed: ${errorMessage}`);
      console.error("Generation error:", err);
    } finally {
      setGenerating(false);
    }
  };

  const handleExport = async () => {
    setExporting(true);
    try {
      const res = await api.get(`/export/${projectId}`, {
        responseType: "blob", // Important: tells axios to handle binary data
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        `${project.title.replace(/\s+/g, "_")}.${project.doc_type}`
      );
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      alert("Export failed");
    } finally {
      setExporting(false);
    }
  };

  // Update a section in our local state after refinement
  const updateSection = (updatedSection) => {
    setSections(
      sections.map((s) => (s.id === updatedSection.id ? updatedSection : s))
    );
  };

  if (loading) return <p className="p-4">Loading...</p>;
  if (!project) return <p className="p-4">Project not found</p>;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <nav className="bg-white border-b px-6 py-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-bold text-blue-600">DocAI</h1>
          <p className="text-xs text-gray-500 mt-1">
            {project.title} • {project.doc_type === "docx" ? "Word" : "PowerPoint"}
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleGenerateAll}
            disabled={generating}
            className="bg-purple-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-purple-700 disabled:opacity-50 transition"
          >
            {generating ? "Generating..." : "🤖 Generate All"}
          </button>
          <button
            onClick={handleExport}
            disabled={exporting}
            className="bg-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-green-700 disabled:opacity-50 transition"
          >
            {exporting ? "Exporting..." : "📥 Export"}
          </button>
          <button
            onClick={() => navigate("/dashboard")}
            className="text-gray-500 px-4 py-2 rounded-lg text-sm hover:bg-gray-100 transition"
          >
            ← Back
          </button>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-3xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mb-1">Edit Sections</h2>
          <p className="text-gray-500 text-sm">
            Create AI-generated content and refine it section by section
          </p>
        </div>

        <div className="space-y-4">
          {sections.map((section) => (
            <SectionCard
              key={section.id}
              section={section}
              projectDocType={project.doc_type}
              onUpdate={updateSection}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
