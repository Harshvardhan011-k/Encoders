"use client";

import { useState, useEffect } from "react";

interface SampleProduct {
  id: string;
  name: string;
  ingredients: string;
}

interface AIResponse {
  what_stands_out: string;
  why_it_matters: string;
  uncertainty: string;
  recommendation: string;
  inferred_intent: string;
}

export default function Home() {
  const [ingredients, setIngredients] = useState("");
  const [samples, setSamples] = useState<SampleProduct[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AIResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchSamples();
  }, []);

  const fetchSamples = async () => {
    try {
      const res = await fetch("http://localhost:8000/sample-data");
      if (res.ok) {
        const data = await res.json();
        setSamples(data);
      }
    } catch (err) {
      console.error("Failed to fetch samples", err);
      // Fallback mock samples if backend is not running
      setSamples([
        { id: "1", name: "Energy Drink", ingredients: "Carbonated Water, High Fructose Corn Syrup, Caffeine, Red 40" },
        { id: "2", name: "Almond Milk", ingredients: "Filtered Water, Almonds, Sea Salt, Gellan Gum" },
        { id: "3", name: "Potato Chips", ingredients: "Potatoes, Vegetable Oil, Salt" }
      ]);
    }
  };

  const handleAnalyze = async (text?: string) => {
    const inputText = text || ingredients;
    if (!inputText) return;

    setLoading(true);
    setResult(null);
    setError("");

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ingredients_text: inputText })
      });

      if (res.ok) {
        const data = await res.json();
        setResult(data);
      } else {
        setError("Failed to analyze ingredients. Check if backend is running.");
      }
    } catch (err) {
      setError("An error occurred. Make sure the backend API is accessible.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <h1>Ingredient Copilot</h1>
        <p className="subtitle">Your AI-native health companion for mindful decisions.</p>
      </header>

      <main className="glass">
        <div className="input-section">
          <textarea
            className="text-area"
            placeholder="Paste ingredient list here, or select a sample..."
            value={ingredients}
            onChange={(e) => setIngredients(e.target.value)}
          />

          <div className="button-group">
            <button
              className="btn btn-primary"
              onClick={() => handleAnalyze()}
              disabled={loading || !ingredients}
            >
              {loading ? "Analyzing..." : "Analyze Ingredients"}
            </button>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setIngredients("");
                setResult(null);
              }}
            >
              Clear
            </button>
          </div>
        </div>

        {!result && !loading && (
          <div className="sample-section">
            <p style={{ marginBottom: '1rem', color: 'var(--text-secondary)', fontWeight: 600 }}>Or try a sample product:</p>
            <div className="sample-grid">
              {samples.map((sample) => (
                <div
                  key={sample.id}
                  className="sample-card"
                  onClick={() => {
                    setIngredients(sample.ingredients);
                    handleAnalyze(sample.ingredients);
                  }}
                >
                  <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>{sample.name}</h3>
                  <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {sample.ingredients}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {loading && (
          <div className="thinking">
            <div className="dot dot-1"></div>
            <div className="dot dot-2"></div>
            <div className="dot"></div>
            <span>Copilot is reasoning about your health...</span>
          </div>
        )}

        {error && (
          <div style={{ color: '#ef4444', marginTop: '1rem', textAlign: 'center' }}>
            {error}
          </div>
        )}

        {result && (
          <div className="response-container">
            <div className="response-section" style={{ borderBottom: '1px solid var(--glass-border)' }}>
              <div className="response-label">Inferred Intent</div>
              <div className="response-text" style={{ fontStyle: 'italic', color: 'var(--accent-secondary)' }}>
                "{result.inferred_intent}"
              </div>
            </div>

            <div className="response-section">
              <div className="response-label">What Stands Out</div>
              <div className="response-text">{result.what_stands_out}</div>
            </div>

            <div className="response-section">
              <div className="response-label">Why It Might Matter</div>
              <div className="response-text">{result.why_it_matters}</div>
            </div>

            <div className="response-section">
              <div className="response-label">What's Uncertain</div>
              <div className="response-text">{result.uncertainty}</div>
            </div>

            <div className="response-section">
              <div className="response-label">How To Think About It</div>
              <div className="response-text" style={{ padding: '1rem', background: 'rgba(129, 140, 248, 0.1)', borderRadius: '12px' }}>
                {result.recommendation}
              </div>
            </div>
          </div>
        )
        }
      </main >

      <footer>
        Made for Consumer Health Hackathon 2026
      </footer>
    </div >
  );
}
