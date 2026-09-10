interface StatusMessageProps {
  isAnalyzing: boolean
  error: string | null
  filename: string | null
}

function StatusMessage({
  isAnalyzing,
  error,
  filename,
}: StatusMessageProps) {
  if (isAnalyzing) {
    return <p>Analyzing audio...</p>
  }

  if (error) {
    return <p>Analysis failed: {error}</p>
  }

  if (filename) {
    return <p>Analysis successful: {filename}</p>
  }

  return null
}

export default StatusMessage