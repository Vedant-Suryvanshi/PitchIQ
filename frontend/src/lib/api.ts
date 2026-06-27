import axios, { AxiosError } from 'axios'
import type { GenerateResponse, JobStatusResponse, MemoResponse } from '@/types'

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000'

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 120_000,
  headers: { 'Content-Type': 'application/json' },
})

apiClient.interceptors.response.use(
  (res) => res,
  (err: AxiosError<{ detail: string }>) => {
    const message = err.response?.data?.detail || err.message || 'An unexpected error occurred'
    return Promise.reject(new Error(message))
  }
)

export async function generateMemo(description: string): Promise<GenerateResponse> {
  const { data } = await apiClient.post<GenerateResponse>('/api/generate', { description })
  return data
}

export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  const { data } = await apiClient.get<JobStatusResponse>(`/api/status/${jobId}`)
  return data
}

export async function getMemo(jobId: string): Promise<MemoResponse> {
  const { data } = await apiClient.get<MemoResponse>(`/api/memo/${jobId}`)
  return data
}

export function pollJobStatus(
  jobId: string,
  onUpdate: (status: JobStatusResponse) => void,
  onComplete: (status: JobStatusResponse) => void,
  onError: (error: string) => void,
  intervalMs = 2500
): () => void {
  let stopped = false

  const poll = async () => {
    while (!stopped) {
      try {
        const status = await getJobStatus(jobId)
        onUpdate(status)
        if (status.status === 'completed') { onComplete(status); return }
        if (status.status === 'failed')    { onError(status.error_message || 'Generation failed'); return }
      } catch (err) {
        onError(err instanceof Error ? err.message : 'Polling failed')
        return
      }
      await new Promise((r) => setTimeout(r, intervalMs))
    }
  }

  poll()
  return () => { stopped = true }
}