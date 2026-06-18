import { useState } from "react"
import axios from "axios"

const SUGGESTIONS = [
  "i wish", "no tool for", "why doesn't", "manually doing",
  "hate that", "frustrated with", "waste of time", "nobody solves",
  "i need a tool", "annoying that", "why isn't there"
]

export default function App() {
  const [input, setInput] = useState("")
  const [keywords, setKeywords] = useState([])
  const [platforms, setPlatforms] = useState(["hn"])
  const [redditCreds, setRedditCreds] = useState({ client_id: "", client_secret: "" })
  const [phApiKey, setPhApiKey] = useState("")
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [errors, setErrors] = useState({})
  const [pressed, setPressed] = useState(false)

  const filteredSuggestions = SUGGESTIONS.filter(
    s => s.includes(input.toLowerCase()) && input && !keywords.includes(s)
  )

  const addKeyword = (kw) => {
    if (!keywords.includes(kw)) setKeywords([...keywords, kw])
    setInput("")
  }

  const removeKeyword = (kw) => setKeywords(keywords.filter(k => k !== kw))

  const togglePlatform = (p) => {
    setPlatforms(prev =>
      prev.includes(p) ? prev.filter(x => x !== p) : [...prev, p]
    )
  }

  const handleScrape = async () => {
    if (keywords.length === 0) return
    setPressed(true)
    setLoading(true)
    setResults([])
    setErrors({})
    try {
      const res = await axios.post("https://pain-miner-production.up.railway.app/scrape", {
        keywords,
        platforms,
        limit: 20,
        reddit_client_id: redditCreds.client_id || null,
        reddit_client_secret: redditCreds.client_secret || null,
        producthunt_api_key: phApiKey || null,
      })
      setResults(res.data.results)
      setErrors(res.data.errors)
    } catch (e) {
      setErrors({ network: "Cannot reach backend" })
    }
    setLoading(false)
    setPressed(true)
    setTimeout(() => setPressed(false), 3000)
  }

  const downloadCSV = () => {
    const header = ["source", "title", "body", "url", "score", "author", "keyword_matched"]
    const rows = results.map(r => header.map(h => `"${(r[h] || "").toString().replace(/"/g, "'")}"`).join(","))
    const csv = [header.join(","), ...rows].join("\n")
    const blob = new Blob([csv], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "pain_points.csv"
    a.click()
  }

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: "40px 20px", fontFamily: "monospace" }}>
      <h1 style={{ fontSize: 28, marginBottom: 4 }}>🔍 Pain Miner</h1>
      <p style={{ color: "#666", marginBottom: 8 }}>Scrape platforms for startup ideas</p>

      {/* How to use */}
      <div style={{
        background: "#f0f9ff", border: "1px solid #bae6fd",
        borderRadius: 8, padding: "10px 16px", marginBottom: 24, fontSize: 13, color: "#0369a1"
      }}>
        💡 <strong>How to use:</strong> Type a keyword below and press <strong>Enter</strong> to add it → select platforms → click <strong>Run Scraper</strong>
      </div>

      {/* Keyword Input */}
      <div style={{ position: "relative", marginBottom: 16 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && input && addKeyword(input)}
          placeholder='Write your keyword and press Enter (e.g. "i wish", "no tool for")'
          style={{
            width: "100%", padding: "12px 16px", fontSize: 16,
            border: "2px solid #000", borderRadius: 8, boxSizing: "border-box"
          }}
        />
        {filteredSuggestions.length > 0 && (
          <div style={{
            position: "absolute", top: "110%", left: 0, right: 0,
            background: "#fff", border: "2px solid #000", borderRadius: 8,
            zIndex: 10, overflow: "hidden"
          }}>
            {filteredSuggestions.map(s => (
              <div
                key={s}
                onClick={() => addKeyword(s)}
                style={{ padding: "10px 16px", cursor: "pointer", borderBottom: "1px solid #eee" }}
                onMouseEnter={e => e.target.style.background = "#f5f5f5"}
                onMouseLeave={e => e.target.style.background = "#fff"}
              >
                {s}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Active Keywords */}
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 24, minHeight: 32 }}>
        {keywords.map(kw => (
          <span key={kw} onClick={() => removeKeyword(kw)} style={{
            background: "#000", color: "#fff", padding: "4px 12px",
            borderRadius: 20, fontSize: 14, cursor: "pointer"
          }}>
            {kw} ✕
          </span>
        ))}
      </div>

      {/* Platform Selector */}
      <div style={{ marginBottom: 16 }}>
        <p style={{ fontWeight: "bold", marginBottom: 8 }}>Platforms:</p>
        <div style={{ display: "flex", gap: 12 }}>
          {["hn", "reddit", "producthunt"].map(p => (
            <button
              key={p}
              onClick={() => togglePlatform(p)}
              style={{
                padding: "8px 20px", border: "2px solid #000", borderRadius: 8,
                cursor: "pointer", fontFamily: "monospace", fontSize: 14,
                background: platforms.includes(p) ? "#16a34a" : "#fff",
                color: platforms.includes(p) ? "#fff" : "#000"
              }}
            >
              {p === "hn" ? "Hacker News" : p === "reddit" ? "Reddit" : "Product Hunt"}
            </button>
          ))}
        </div>
      </div>

      {/* Reddit Info Box + Credentials — fixed height so button doesn't move */}
      <div style={{ minHeight: 160, marginBottom: 8 }}>
        {platforms.includes("reddit") && (
          <div style={{ marginBottom: 12 }}>
            <div style={{
              padding: 14, background: "#fffbe6", border: "1px solid #f0c000",
              borderRadius: 8, marginBottom: 12, fontSize: 13
            }}>
              <p style={{ fontWeight: "bold", marginBottom: 6 }}>📋 How to get Reddit API credentials:</p>
              <ol style={{ margin: 0, paddingLeft: 18, lineHeight: "1.8" }}>
                <li>Go to <a href="https://www.reddit.com/prefs/apps" target="_blank" rel="noreferrer" style={{ color: "#c05000" }}>reddit.com/prefs/apps</a></li>
                <li>Click <strong>"create another app"</strong> → select <strong>script</strong></li>
                <li>Name it anything, redirect URI: <code>http://localhost:8080</code></li>
                <li>Click <strong>create app</strong> → copy <strong>client_id</strong> and <strong>client_secret</strong></li>
              </ol>
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              <input
                placeholder="client_id"
                value={redditCreds.client_id}
                onChange={e => setRedditCreds({ ...redditCreds, client_id: e.target.value })}
                style={{
                  flex: 1, padding: "10px 12px", border: "1px solid #ccc",
                  borderRadius: 8, fontFamily: "monospace", fontSize: 14
                }}
              />
              <input
                placeholder="client_secret"
                type="password"
                value={redditCreds.client_secret}
                onChange={e => setRedditCreds({ ...redditCreds, client_secret: e.target.value })}
                style={{
                  flex: 1, padding: "10px 12px", border: "1px solid #ccc",
                  borderRadius: 8, fontFamily: "monospace", fontSize: 14
                }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Platform warning */}
      {platforms.length === 0 && (
        <p style={{ color: "red", fontSize: 14, marginBottom: 12 }}>Please select at least one platform</p>
      )}

      {/* Errors */}
      {Object.keys(errors).length > 0 && (
        <div style={{ marginBottom: 16, padding: 12, background: "#fff3f3", border: "1px solid #f00", borderRadius: 8 }}>
          {Object.entries(errors).map(([k, v]) => (
            <p key={k} style={{ margin: 0, color: "red", fontSize: 14 }}>⚠ {k}: {v}</p>
          ))}
        </div>
      )}

      {/* Scrape Button */}
      <button
        onClick={handleScrape}
        disabled={keywords.length === 0 || platforms.length === 0}
        style={{
          padding: "12px 32px",
          background: loading ? "#555" : pressed ? "#16a34a" : "#000",
          color: "#fff",
          border: "none",
          borderRadius: 8,
          fontSize: 16,
          cursor: keywords.length === 0 || platforms.length === 0 ? "not-allowed" : "pointer",
          fontFamily: "monospace",
          marginBottom: 32,
          opacity: keywords.length === 0 || platforms.length === 0 ? 0.5 : 1,
          transition: "background 0.4s ease"
        }}
      >
        {loading ? "Scraping..." : pressed ? "✓ Done" : "Run Scraper"}
      </button>

      {!loading && results.length === 0 && Object.keys(errors).length === 0 && pressed && (
        <div style={{
          padding: 16, background: "#fff3f3", border: "1px solid #f00",
          borderRadius: 8, marginBottom: 16, fontSize: 14, color: "#cc0000"
        }}>
          ⚠ No results found. Try different keywords or check your API credentials.
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <p style={{ fontWeight: "bold" }}>{results.length} results found</p>
            <button
              onClick={downloadCSV}
              style={{
                padding: "8px 20px", border: "2px solid #000", borderRadius: 8,
                cursor: "pointer", fontFamily: "monospace", background: "#fff"
              }}
            >
              Download CSV
            </button>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 14 }}>
            <thead>
              <tr style={{ background: "#000", color: "#fff" }}>
                {["Source", "Title", "Score", "Keyword", "Link"].map(h => (
                  <th key={h} style={{ padding: "10px 12px", textAlign: "left" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results.map((r, i) => (
                <tr key={i} style={{ borderBottom: "1px solid #eee", background: i % 2 === 0 ? "#fafafa" : "#fff" }}>
                  <td style={{ padding: "10px 12px" }}>{r.source}</td>
                  <td style={{ padding: "10px 12px", maxWidth: 300 }}>{r.title}</td>
                  <td style={{ padding: "10px 12px" }}>{r.score}</td>
                  <td style={{ padding: "10px 12px" }}>{r.keyword_matched}</td>
                  <td style={{ padding: "10px 12px" }}>
                    <a href={r.url} target="_blank" rel="noreferrer" style={{ color: "#000" }}>→</a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  )
}