export interface AudioFeatures {
  duration_seconds: number
  sample_rate: number
  pitch_mean_hz: number
  pitch_variability: number
  spectral_flatness_mean: number
  silence_ratio: number
  insufficient_audio: boolean
  notes: string[]
}

export interface AnalyzeResponse {
  status: string
  filename: string
  features: AudioFeatures
}