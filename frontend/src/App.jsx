import { useState } from "react";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [course, setCourse] = useState("");
  const [title, setTitle] = useState("");
  const [prof, setProf] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function search() {
    setLoading(true);
    setError("");
    setResults([]);

    const params = new URLSearchParams();
    if (course.trim()) params.append("course", course.trim());
    if (title.trim()) params.append("title", title.trim());
    if (prof.trim()) params.append("prof", prof.trim());

    try {
      const res = await fetch(`${API_BASE}/search?` + params.toString());
      if (!res.ok) {
        throw new Error("Request failed");
      }
      const data = await res.json();
      setResults(data);
    } catch (e) {
      setError("Failed to load results");
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      search();
    }
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold mb-4">Search Classes</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium">Course</label>
          <input
            className="border rounded px-3 py-2"
            placeholder="CSCI200 or CSCI or 200"
            value={course}
            onChange={(e) => setCourse(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium">Title</label>
          <input
            className="border rounded px-3 py-2"
            placeholder="Data structures, thermodynamics..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium">Prof</label>
          <input
            className="border rounded px-3 py-2"
            placeholder="Hellman, Brice..."
            value={prof}
            onChange={(e) => setProf(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </div>
      </div>

      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={search}
      >
        Search
      </button>

      {loading && <div>Loading...</div>}
      {error && <div className="text-red-600">{error}</div>}

      {results.length > 0 && (
        <table className="w-full border mt-4">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">CRN</th>
              <th className="p-2 border">Course</th>
              <th className="p-2 border">Section</th>
              <th className="p-2 border">Title</th>
              <th className="p-2 border">Prof</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r) => (
              <tr key={r.crn}>
                <td className="border p-2">{r.crn}</td>
                <td className="border p-2">
                  {r.subject}
                  {r.number}
                </td>
                <td className="border p-2">{r.section}</td>
                <td className="border p-2">{r.title}</td>
                <td className="border p-2">{r.prof}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {!loading &&
        !error &&
        results.length === 0 &&
        (course.trim() || title.trim() || prof.trim()) && (
          <div className="mt-4">No results</div>
        )}
    </div>
  );
}
