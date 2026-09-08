export type UploadStatus = 'idle' | 'uploading' | 'success' | 'error'

export function getUploadStatusMessage(status: UploadStatus): string {
  switch (status) {
    case 'uploading':
      return 'Uploading audio...'
    case 'success':
      return 'Audio uploaded successfully.'
    case 'error':
      return 'Audio upload failed.'
    default:
      return ''
  }
}