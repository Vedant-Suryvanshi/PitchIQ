export type AgentStatus = 'queued' | 'running' | 'completed' | 'failed'

export interface AgentProgress {
  intake:          AgentStatus
  market_research: AgentStatus
  funding:         AgentStatus
  vc_memo:         AgentStatus
  quality_review:  AgentStatus
}

export interface JobStatusResponse {
  job_id:         string
  status:         'queued' | 'running' | 'completed' | 'failed'
  agent_progress: AgentProgress
  error_message:  string | null
  created_at:     string
  updated_at:     string
  memo_available: boolean
}

export interface GenerateResponse {
  job_id:  string
  message: string
  status:  string
}

export interface QualityFlag {
  severity:       'high' | 'medium' | 'low'
  section:        string
  issue:          string
  recommendation: string
}

export interface MemoResponse {
  job_id:           string
  startup_name:     string | null
  industry:         string | null
  memo_markdown:    string
  confidence_score: number | null
  quality_flags:    QualityFlag[] | string[]
  created_at:       string
}