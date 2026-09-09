import { apiFetch } from './api'
import type { AnalyzeResponse } from '../types/analysis'

export async function analyzeAudio(
  file: File
): Promise<AnalyzeResponse> {
  const formData = new FormData()
  formData.append('file', file)

  return apiFetch<AnalyzeResponse>('/analyze', {
    method: 'POST',
    body: formData,
  })
}
