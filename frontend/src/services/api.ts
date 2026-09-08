import type { ApiErrorResponse } from '../types/upload'

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export class ApiError extends Error {
  status: number

  constructor(message: string, status: number) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiFetch<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, options)

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`

    try {
      const errorBody = (await response.json()) as ApiErrorResponse

      if (errorBody?.detail) {
        message = errorBody.detail
      }
    } catch {
      // Keep the generic error message if the response isn't JSON.
    }

    throw new ApiError(message, response.status)
  }

  return response.json() as Promise<T>
}



