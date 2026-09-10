import { useAudioUpload } from './hooks/useAudioUpload'
import './App.css'

function App() {
  const {
    isAnalyzing,
    error,
    features,
    filename,
    analyzeFile,
  } = useAudioUpload()

  const handleFileChange = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0]

    if (!file) {
      return
    }

    await analyzeFile(file)
  }

  return (
    <div className="app">
      <header className="header">
        <div className="brand">
          <div className="brand-icon">🛡️</div>

          <div>
            <h1>Voice Clone Defense</h1>
            <p>AI-Powered Voice Authenticity Analysis</p>
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="hero-section">
          <div className="hero-badge">🔒 AI Voice Security</div>

          <h2>Detect suspicious voice recordings</h2>

          <p className="hero-description">
            Upload an audio recording to analyze its characteristics and
            identify potential signs of synthetic or manipulated speech.
          </p>
        </section>

        <section className="upload-card">
                  <section className="process-section">
          <div className="process-header">
            <p className="section-label">HOW IT WORKS</p>
            <h3>From recording to security insight</h3>
          </div>

          <div className="process-grid">
            <div className="process-step">
              <div className="process-number">01</div>
              <div className="process-icon">🎙️</div>
              <h4>Upload</h4>
              <p>
                Select a voice recording from your device.
              </p>
            </div>

            <div className="process-arrow">→</div>

            <div className="process-step">
              <div className="process-number">02</div>
              <div className="process-icon">📊</div>
              <h4>Analyze</h4>
              <p>
                Extract audio characteristics from the recording.
              </p>
            </div>

            <div className="process-arrow">→</div>

            <div className="process-step">
              <div className="process-number">03</div>
              <div className="process-icon">🛡️</div>
              <h4>Assess</h4>
              <p>
                Generate a probabilistic voice authenticity assessment.
              </p>
            </div>
          </div>
        </section>
          <div className="upload-icon">🎙️</div>

<div className="upload-badge">AUDIO ANALYSIS</div>

<h3>Upload a voice recording</h3>

<p className="upload-description">
  Check an audio recording for characteristics associated with
  synthetic or manipulated speech.
</p>
          <label className="upload-button">
            <span>Choose Audio File</span>

            <input
              type="file"
              accept=".wav,.mp3,.m4a,.flac"
              onChange={handleFileChange}
              disabled={isAnalyzing}
            />
          </label>

          <p className="file-info">
            WAV • MP3 • M4A • FLAC &nbsp;|&nbsp; Maximum 25 MB
          </p>

          {isAnalyzing && (
            <div className="status loading" role="status" aria-live="polite">
              <span className="spinner" />
              <span>Analyzing audio...</span>
            </div>
          )}

          {error && (
            <div className="status error" role="alert">
              <strong>Analysis failed</strong>
              <span>{error}</span>
            </div>
          )}

          {filename && !error && !isAnalyzing && (
  <>
    <div className="status success" role="status">
      <strong>Analysis complete</strong>
      <span>{filename}</span>
    </div>

    <label className="analyze-again-button">
      <span>↻ Analyze Another File</span>

      <input
        type="file"
        accept=".wav,.mp3,.m4a,.flac"
        onChange={handleFileChange}
      />
    </label>
  </>
)}
        </section>

        {features && (
          <section className="results-card">
            <div className="results-header">
              <div>
                <p className="section-label">ANALYSIS RESULTS</p>
                <h3>Audio characteristics</h3>
              </div>

              <span className="result-badge">Processed</span>
            </div>

            <div className="feature-grid">
              <div className="feature-item">
                <span>Duration</span>
                <strong>{features.duration_seconds} sec</strong>
              </div>

              <div className="feature-item">
                <span>Sample Rate</span>
                <strong>{features.sample_rate} Hz</strong>
              </div>

              <div className="feature-item">
                <span>Mean Pitch</span>
                <strong>{features.pitch_mean_hz.toFixed(2)} Hz</strong>
              </div>

              <div className="feature-item">
                <span>Pitch Variability</span>
                <strong>{features.pitch_variability.toFixed(2)}</strong>
              </div>

              <div className="feature-item">
                <span>Spectral Flatness</span>
                <strong>
                  {features.spectral_flatness_mean.toExponential(4)}
                </strong>
              </div>

              <div className="feature-item">
                <span>Silence Ratio</span>
                <strong>
                  {(features.silence_ratio * 100).toFixed(2)}%
                </strong>
              </div>
            </div>

            {features.insufficient_audio && (
              <div className="warning-box">
                <strong>Limited audio data</strong>

                <p>
                  The recording may not contain enough usable audio for a
                  reliable analysis.
                </p>
              </div>
            )}

            {features.notes.length > 0 && (
              <div className="notes-box">
                <h4>Analysis notes</h4>

                <ul>
                  {features.notes.map((note, index) => (
                    <li key={index}>{note}</li>
                  ))}
                </ul>
              </div>
            )}
          </section>
        )}

        {features && (
          <section className="risk-card">
            <div className="risk-header">
              <div>
                <p className="section-label">DETECTION STATUS</p>

                <h3>Voice authenticity assessment</h3>
              </div>

              <span className="risk-badge pending">Pending</span>
            </div>

            <div className="risk-main">
              <div className="risk-icon">🔍</div>

              <div>
                <h4>Detection model pending</h4>

                <p>
                  Raw audio analysis is complete. A final synthetic or
                  voice-cloning assessment will appear here once the detection
                  model is connected.
                </p>
              </div>
            </div>

            <div className="risk-details">
  <div>
    <span>Detection Result</span>
    <strong>Pending model analysis</strong>
  </div>

  <div>
    <span>Confidence</span>
    <strong>Not available yet</strong>
  </div>
</div>

<div className="explanation-box">
  <h4>Why is the result pending?</h4>

  <p>
    The system has extracted the recording's audio characteristics.
    The synthetic-voice detection model will use these features to
    provide a probabilistic assessment.
  </p>
</div>
          </section>
        )}

        {features && (
          <section className="recommendation-card">
            <div className="recommendation-icon">🛡️</div>

            <div className="recommendation-content">
              <p className="section-label">SECURITY RECOMMENDATION</p>

              <h3>Recommended Action</h3>

              <p>
                Final security guidance will appear after the detection model
                evaluates the recording.
              </p>
            </div>
          </section>
        )}
{!features && !isAnalyzing && !error && (
  <section className="empty-state">
    <div className="empty-state-icon">🎧</div>

    <h3>Ready for analysis</h3>

    <p>
      Upload a voice recording above to see its audio characteristics
      and authenticity assessment.
    </p>
  </section>
)}
        <section className="trust-section">
          <div>
            <span className="trust-icon">🔐</span>
            <strong>Privacy-conscious analysis</strong>
          </div>

          <p>
            Results are probabilistic and should be used as a security aid,
            not as absolute proof of authenticity.
          </p>
        </section>
      </main>

      <footer className="footer">
        <p>Voice Clone Defense • SIH 2026</p>
      </footer>
    </div>
  )
}

export default App