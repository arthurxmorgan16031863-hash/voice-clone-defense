import { useAudioUpload } from './hooks/useAudioUpload'

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
    <div>
      <h1>Voice Clone Defense</h1>

      <input
        type="file"
        accept=".wav,.mp3,.m4a,.flac"
        onChange={handleFileChange}
        disabled={isAnalyzing}
      />

      {isAnalyzing && <p>Analyzing audio...</p>}

      {error && <p>Analysis failed: {error}</p>}

      {filename && !error && !isAnalyzing && (
        <p>Analysis successful: {filename}</p>
      )}

      {features && (
        <div>
          <h2>Audio Analysis</h2>

          <p>
            Duration: {features.duration_seconds} seconds
          </p>

          <p>
            Sample Rate: {features.sample_rate} Hz
          </p>

          <p>
            Mean Pitch: {features.pitch_mean_hz.toFixed(2)} Hz
          </p>

          <p>
            Pitch Variability:{' '}
            {features.pitch_variability.toFixed(2)}
          </p>

          <p>
            Spectral Flatness:{' '}
            {features.spectral_flatness_mean.toExponential(4)}
          </p>

          <p>
            Silence Ratio:{' '}
            {(features.silence_ratio * 100).toFixed(2)}%
          </p>

          <p>
            Insufficient Audio:{' '}
            {features.insufficient_audio ? 'Yes' : 'No'}
          </p>

          {features.notes.length > 0 && (
            <div>
              <h3>Notes</h3>

              <ul>
                {features.notes.map((note, index) => (
                  <li key={index}>{note}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default App