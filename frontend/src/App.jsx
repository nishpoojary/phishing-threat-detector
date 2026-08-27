import { useState } from "react";
import "./App.css";

const API_URL =  import.meta.env.VITE_API_URL;

function App() {
  const [activeTab, setActiveTab] = useState("email");
  const [loading, setLoading] = useState(false);

  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");
  const [emailResult, setEmailResult] = useState(null);

  const [url, setUrl] = useState("");
  const [urlResult, setUrlResult] = useState(null);

  const analyzeEmail = async () => {
    if (!subject.trim() || !body.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/detect`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subject,
          body,
        }),
      });

      if (!response.ok) {
        throw new Error("Detection failed");
      }

      const data = await response.json();
      setEmailResult(data);
    } catch (error) {
      alert("Could not connect to the detection server.");
    } finally {
      setLoading(false);
    }
  };

  const analyzeUrl = async () => {
    if (!url.trim()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/detect-url`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url,
        }),
      });

      if (!response.ok) {
        throw new Error("URL detection failed");
      }

      const data = await response.json();
      setUrlResult(data);
    } catch (error) {
      alert("Could not connect to the detection server.");
    } finally {
      setLoading(false);
    }
  };

  const clearEmail = () => {
    setSubject("");
    setBody("");
    setEmailResult(null);
  };

  const clearUrl = () => {
    setUrl("");
    setUrlResult(null);
  };

  return (
    <div className="app">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="brand">
          <div className="brand-icon">🛡</div>

          <div>
            <div className="brand-name">PhishGuard AI</div>
            <div className="brand-subtitle">
              Threat Detection Platform
            </div>
          </div>
        </div>

        <div className="status">
          <span className="status-dot"></span>
          Detection Engine Online
        </div>
      </nav>

      {/* HERO */}
      <main>

        <section className="hero">

          <div className="hero-badge">
            <span>✦</span>
            AI-POWERED SECURITY
          </div>

          <h1>
            Detect threats
            <br />
            <span>before they deceive you.</span>
          </h1>

          <p>
            Analyze suspicious emails and URLs using machine-learning
            threat detection and receive an instant security assessment.
          </p>

        </section>

        {/* SCANNER */}
        <section className="scanner-section">

          <div className="scanner-header">
            <div>
              <span className="section-label">SECURITY ANALYZER</span>
              <h2>Inspect a threat</h2>
            </div>

            <div className="scanner-status">
              ● Ready to analyze
            </div>
          </div>

          {/* TABS */}
          <div className="scanner-tabs">

            <button
              className={
                activeTab === "email"
                  ? "scanner-tab active"
                  : "scanner-tab"
              }
              onClick={() => setActiveTab("email")}
            >
              <span className="tab-icon">✉</span>
              Email Scanner
            </button>

            <button
              className={
                activeTab === "url"
                  ? "scanner-tab active"
                  : "scanner-tab"
              }
              onClick={() => setActiveTab("url")}
            >
              <span className="tab-icon">↗</span>
              URL Scanner
            </button>

          </div>

          <div className="scanner-grid">

            {/* INPUT CARD */}
            <div className="panel">

              {activeTab === "email" ? (
                <>
                  <div className="panel-title">
                    <div className="panel-icon">✉</div>

                    <div>
                      <h3>Email Analysis</h3>
                      <p>
                        Paste the suspicious email below.
                      </p>
                    </div>
                  </div>

                  <label>Email Subject</label>

                  <input
                    type="text"
                    placeholder="e.g. Your account requires verification"
                    value={subject}
                    onChange={(e) => setSubject(e.target.value)}
                  />

                  <label>Email Content</label>

                  <textarea
                    placeholder="Paste the complete email message here..."
                    value={body}
                    onChange={(e) => setBody(e.target.value)}
                  />

                  <div className="action-row">

                    <button
                      className="clear-btn"
                      onClick={clearEmail}
                    >
                      Clear
                    </button>

                    <button
                      className="analyze-btn"
                      onClick={analyzeEmail}
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <span className="spinner"></span>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          Analyze Email
                          <span>→</span>
                        </>
                      )}
                    </button>

                  </div>
                </>
              ) : (
                <>
                  <div className="panel-title">
                    <div className="panel-icon">↗</div>

                    <div>
                      <h3>URL Analysis</h3>
                      <p>
                        Check a suspicious website address.
                      </p>
                    </div>
                  </div>

                  <label>Website URL</label>

                  <input
                    type="url"
                    placeholder="https://example.com/login"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                  />

                  <div className="url-help">
                    <span>ⓘ</span>
                    Enter the complete URL including
                    <strong> http:// </strong>
                    or
                    <strong> https://</strong>.
                  </div>

                  <div className="action-row url-actions">

                    <button
                      className="clear-btn"
                      onClick={clearUrl}
                    >
                      Clear
                    </button>

                    <button
                      className="analyze-btn"
                      onClick={analyzeUrl}
                      disabled={loading}
                    >
                      {loading ? (
                        <>
                          <span className="spinner"></span>
                          Analyzing...
                        </>
                      ) : (
                        <>
                          Analyze URL
                          <span>→</span>
                        </>
                      )}
                    </button>

                  </div>
                </>
              )}

            </div>

            {/* RESULT CARD */}
            <div className="panel result-panel">

              {!emailResult && !urlResult && (
                <div className="empty-result">

                  <div className="empty-icon">
                    ◉
                  </div>

                  <h3>Awaiting Analysis</h3>

                  <p>
                    Submit an email or URL to receive
                    its security assessment.
                  </p>

                  <div className="safe-message">
                    <span>✓</span>
                    Never click suspicious links before
                    verifying the sender.
                  </div>

                </div>
              )}

              {activeTab === "email" && emailResult && (
                <EmailResult result={emailResult} />
              )}

              {activeTab === "url" && urlResult && (
                <UrlResult result={urlResult} />
              )}

            </div>

          </div>
        </section>

        {/* FEATURES */}
        <section className="features">

          <div className="feature-card">
            <div className="feature-icon">◈</div>
            <div>
              <h4>Machine Learning</h4>
              <p>AI-powered threat classification</p>
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <div>
              <h4>Instant Analysis</h4>
              <p>Get results in seconds</p>
            </div>
          </div>

          <div className="feature-card">
            <div className="feature-icon">◉</div>
            <div>
              <h4>Risk Intelligence</h4>
              <p>Probability-based security scoring</p>
            </div>
          </div>

        </section>

      </main>

      {/* FOOTER */}
      <footer>
        <div>
          <strong>PhishGuard AI</strong>
          <span> · AI-powered threat detection</span>
        </div>

        <div>
          Local Analysis Engine · Secure by Design
        </div>
      </footer>

    </div>
  );
}


/* EMAIL RESULT */

function EmailResult({ result }) {
  const phishing = result.is_phishing;

  return (
    <div className="analysis-result">

      <div
        className={
          phishing
            ? "result-heading danger"
            : "result-heading safe"
        }
      >
        <div className="result-symbol">
          {phishing ? "!" : "✓"}
        </div>

        <div>
          <span>ANALYSIS RESULT</span>

          <h3>
            {phishing
              ? "Phishing Email Detected"
              : "Safe Email"}
          </h3>
        </div>
      </div>

      <div className="risk-box">

        <div>
          <span>RISK LEVEL</span>
          <strong>{result.risk_level}</strong>
        </div>

        <div className="probability">
          <span>PHISHING PROBABILITY</span>
          <strong>
            {result.phishing_probability}%
          </strong>
        </div>

      </div>

      <div className="progress-section">

        <div className="progress-label">
          <span>Phishing</span>
          <strong>
            {result.phishing_probability}%
          </strong>
        </div>

        <div className="progress">
          <div
            className="progress-danger"
            style={{
              width: `${result.phishing_probability}%`,
            }}
          ></div>
        </div>

        <div className="progress-label safe-label">
          <span>Safe</span>
          <strong>
            {result.safe_probability}%
          </strong>
        </div>

        <div className="progress">
          <div
            className="progress-safe"
            style={{
              width: `${result.safe_probability}%`,
            }}
          ></div>
        </div>

      </div>

      {result.indicators &&
        result.indicators.length > 0 && (
          <div className="indicators">

            <h4>Detection Indicators</h4>

            {result.indicators.map((item, index) => (
              <div className="indicator" key={index}>
                <span>!</span>
                {item}
              </div>
            ))}

          </div>
        )}

      <div className="recommendation">
        <strong>
          {phishing ? "⚠ High Risk" : "✓ Low Risk"}
        </strong>

        <p>
          {phishing
            ? "Avoid clicking links, downloading attachments, or providing personal information."
            : "No significant phishing characteristics were detected in this email."}
        </p>
      </div>

    </div>
  );
}


/* URL RESULT */

function UrlResult({ result }) {
  return (
    <div className="analysis-result">

      <div
        className={
          result.is_suspicious
            ? "result-heading danger"
            : "result-heading safe"
        }
      >

        <div className="result-symbol">
          {result.is_suspicious ? "!" : "✓"}
        </div>

        <div>
          <span>ANALYSIS RESULT</span>

          <h3>
            {result.is_suspicious
              ? "Suspicious URL Detected"
              : "Safe URL"}
          </h3>
        </div>

      </div>

      <div className="url-score">

        <span>RISK SCORE</span>

        <strong>
          {result.risk_score}
        </strong>

        <small>/ 100</small>

      </div>

      <div className="risk-box">

        <div>
          <span>RISK LEVEL</span>

          <strong>
            {result.risk_level}
          </strong>
        </div>

        <div>
          <span>CLASSIFICATION</span>

          <strong>
            {result.prediction}
          </strong>
        </div>

      </div>

      {result.indicators &&
        result.indicators.length > 0 && (
          <div className="indicators">

            <h4>Detection Indicators</h4>

            {result.indicators.map((item, index) => (
              <div className="indicator" key={index}>
                <span>!</span>
                {item}
              </div>
            ))}

          </div>
        )}

    </div>
  );
}

export default App;