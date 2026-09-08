import { apiFetch } from './api'
import type { UploadResponse } from '../types/upload'

export async function uploadAudio(file: File): Promise<UploadResponse> {
  const formData = new FormData()

  formData.append('file', file)

  return apiFetch<UploadResponse>('/upload', {
    method: 'POST',
    body: formData,
  })
}