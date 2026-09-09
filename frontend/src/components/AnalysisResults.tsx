import type { AudioFeatures } from '../types/analysis'

interface AnalysisResultsProps {
  features: AudioFeatures | null
}

function AnalysisResults({
  features,
}: AnalysisResultsProps) {
  if (!features) {
    return null
  }

  return (
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
  )
}

export default AnalysisResults