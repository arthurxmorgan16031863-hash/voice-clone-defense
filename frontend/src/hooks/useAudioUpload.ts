import { useState } from 'react'
import { analyzeAudio } from '../services/analyze'
import { validateAudioFile } from '../utils/fileValidation'
import type { AudioFeatures } from '../types/analysis'

interface UseAudioUploadResult {
  isAnalyzing: boolean
  error: string | null
  features: AudioFeatures | null
  filename: string | null
  analyzeFile: (file: File) => Promise<void>
  reset: () => void
}

export function useAudioUpload(): UseAudioUploadResult {
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [features, setFeatures] = useState<AudioFeatures | null>(null)
  const [filename, setFilename] = useState<string | null>(null)

  const analyzeFile = async (file: File): Promise<void> => {
    setError(null)
    setFeatures(null)
    setFilename(null)

    const validationError = validateAudioFile(file)

    if (validationError) {
      setError(validationError)
      return
    }

    try {
      setIsAnalyzing(true)

      const result = await analyzeAudio(file)

      setFeatures(result.features)
      setFilename(result.filename)
    } catch (err) {
      const message =
        err instanceof Error ? err.message : 'Audio analysis failed.'

      setError(message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const reset = () => {
    setIsAnalyzing(false)
    setError(null)
    setFeatures(null)
    setFilename(null)
  }

  return {
    isAnalyzing,
    error,
    features,
    filename,
    analyzeFile,
    reset,
  }
}