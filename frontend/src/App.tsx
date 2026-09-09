import AudioUploader from './components/AudioUploader'
import AnalysisResults from './components/AnalysisResults'
import StatusMessage from './components/StatusMessage'
import { useAudioUpload } from './hooks/useAudioUpload'

function App() {
  const {
    isAnalyzing,
    error,
    features,
    filename,
    analyzeFile,
  } = useAudioUpload()

  return (
    <div>
      <h1>Voice Clone Defense</h1>

      <AudioUploader
        isAnalyzing={isAnalyzing}
        onFileSelected={analyzeFile}
      />

      <StatusMessage
        isAnalyzing={isAnalyzing}
        error={error}
        filename={filename}
      />

      <AnalysisResults features={features} />
    </div>
  )
}

export default App