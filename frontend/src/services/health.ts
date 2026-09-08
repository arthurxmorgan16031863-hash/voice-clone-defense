import { apiFetch } from './api'
import type { HealthResponse } from '../types/health'

export async function checkHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>('/health', {
    method: 'GET',
  })
}