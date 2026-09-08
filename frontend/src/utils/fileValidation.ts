const ALLOWED_EXTENSIONS = ['.wav', '.mp3', '.m4a', '.flac']
const MAX_FILE_SIZE = 25 * 1024 * 1024

export function validateAudioFile(file: File): string | null {
  if (!file) {
    return 'Please select an audio file.'
  }

  const fileName = file.name.toLowerCase()
  const isAllowed = ALLOWED_EXTENSIONS.some((extension) =>
    fileName.endsWith(extension)
  )

  if (!isAllowed) {
    return 'Unsupported audio format. Please use WAV, MP3, M4A, or FLAC.'
  }

  if (file.size > MAX_FILE_SIZE) {
    return 'File is too large. Maximum size is 25 MB.'
  }

  return null
}