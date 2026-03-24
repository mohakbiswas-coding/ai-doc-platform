// frontend/src/components/SectionCard.jsx
import { useState } from "react";
import api from "../api";

export default function SectionCard({ section, projectDocType, onUpdate }) {
  const [refinePrompt, setRefinePrompt] = useState("");
  const [comment, setComment] = useState(section.comment || "");
  const [loading, setLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);

  const handleRefine = async () => {
    if (!refinePrompt.trim()) return;
    setLoading(true);
    try {
      const res = await api.post("/ai/refine", {
        section_id: section.id,
        prompt: refinePrompt,
      });
      onUpdate(res.data);
      setRefinePrompt("");
    } catch (err) {
      alert("Refinement failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (feedback) => {
    const newFeedback = section.feedback === feedback ? "none" : feedback;
    const res = await api.patch(`/projects/sections/${section.id}`, { feedback: newFeedback });
    onUpdate(res.data);
  };

  const handleCommentSave = async () => {
    const res = await api.patch(`/projects/sections/${section.id}`, { comment });
    onUpdate(res.data);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden mb-4">
      {/* Header */}
      <div
        className="flex justify-between items-center p-4 cursor-pointer hover:bg-gray-50"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center gap-3">
          <span className="text-blue-600 font-bold text-sm bg-blue-50 px-2 py-1 rounded">
            {projectDocType === "pptx" ? "Slide" : "Section"}
          </span>
          <h3 className="font-semibold text-gray-800">{section.title}</h3>
        </div>
        <div className="flex items-center gap-2">
          {section.feedback === "liked" && <span className="text-green-500">👍</span>}
          {section.feedback === "disliked" && <span className="text-red-500">👎</span>}
          <span className="text-gray-400 text-sm">{isExpanded ? "▲" : "▼"}</span>
        </div>
      </div>

      {isExpanded && (
        <div className="px-4 pb-4 space-y-4">
          {/* Content Display */}
          <div className="bg-gray-50 rounded-lg p-4 min-h-20">
            {section.content ? (
              <p className="text-gray-700 whitespace-pre-wrap text-sm leading-relaxed">
                {section.content}
              </p>
            ) : (
              <p className="text-gray-400 italic text-sm">No content yet. Generate content from the top.</p>
            )}
          </div>

          {/* Feedback Buttons */}
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500">Feedback:</span>
            <button
              onClick={() => handleFeedback("liked")}
              className={`px-3 py-1 rounded-lg text-sm transition ${section.feedback === "liked"
                  ? "bg-green-100 text-green-600 font-medium"
                  : "bg-gray-100 text-gray-500 hover:bg-green-50"
                }`}
            >
              👍 Like
            </button>
            <button
              onClick={() => handleFeedback("disliked")}
              className={`px-3 py-1 rounded-lg text-sm transition ${section.feedback === "disliked"
                  ? "bg-red-100 text-red-600 font-medium"
                  : "bg-gray-100 text-gray-500 hover:bg-red-50"
                }`}
            >
              👎 Dislike
            </button>
            {section.revision_history?.length > 0 && (
              <span className="text-xs text-gray-400">
                {section.revision_history.length} revision(s)
              </span>
            )}
          </div>

          {/* AI Refine Prompt */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              ✨ Refine with AI
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={refinePrompt}
                onChange={(e) => setRefinePrompt(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !loading && handleRefine()}
                placeholder='e.g., "Make this more formal" or "Convert to bullet points"'
                className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleRefine}
                disabled={loading || !refinePrompt.trim()}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition"
              >
                {loading ? "..." : "Refine"}
              </button>
            </div>
          </div>

          {/* Comment Box */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">
              💬 Notes / Comments
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Add a note about this section..."
                className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleCommentSave}
                className="bg-gray-100 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition"
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
