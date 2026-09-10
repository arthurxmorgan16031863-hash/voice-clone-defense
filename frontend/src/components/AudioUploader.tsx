interface AudioUploaderProps {
  isAnalyzing: boolean
  onFileSelected: (file: File) => void
}

function AudioUploader({
  isAnalyzing,
  onFileSelected,
}: AudioUploaderProps) {
  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0]

    if (!file) {
      return
    }

    onFileSelected(file)
  }

  return (
    <div>
      <h2>Select Audio</h2>

      <input
        type="file"
        accept=".wav,.mp3,.m4a,.flac"
        onChange={handleFileChange}
        disabled={isAnalyzing}
      />
    </div>
  )
}

export default AudioUploader