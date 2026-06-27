'use client'

import { motion } from 'framer-motion'
import { Check, Loader2, Clock, AlertCircle, FileSearch, TrendingUp, DollarSign, FileText, Shield } from 'lucide-react'
import type { AgentProgress as AgentProgressType, AgentStatus } from '@/types'

interface AgentConfig {
  key:         keyof AgentProgressType
  label:       string
  description: string
  icon:        React.ReactNode
}

const AGENTS: AgentConfig[] = [
  { key: 'intake',          label: 'Intake Agent',          description: 'Parsing startup profile',   icon: <FileSearch size={16} /> },
  { key: 'market_research', label: 'Market Research Agent', description: 'Analysing market trends',   icon: <TrendingUp size={16} /> },
  { key: 'funding',         label: 'Funding Intel Agent',   description: 'Finding comparable rounds', icon: <DollarSign size={16} /> },
  { key: 'vc_memo',         label: 'VC Memo Agent',         description: 'Drafting investor memo',    icon: <FileText size={16} /> },
  { key: 'quality_review',  label: 'Quality Review Agent',  description: 'Fact-checking & scoring',   icon: <Shield size={16} /> },
]

function StatusIcon({ status }: { status: AgentStatus }) {
  switch (status) {
    case 'completed': return <Check size={14} className="text-pitch-emerald" />
    case 'running':   return <Loader2 size={14} className="text-pitch-purple animate-spin" />
    case 'failed':    return <AlertCircle size={14} className="text-pitch-red" />
    default:          return <Clock size={14} className="text-pitch-cream-dim" />
  }
}

function statusColor(status: AgentStatus): string {
  switch (status) {
    case 'completed': return 'border-pitch-emerald/40 bg-pitch-emerald/5'
    case 'running':   return 'border-pitch-purple/60 bg-pitch-purple/10'
    case 'failed':    return 'border-pitch-red/40 bg-pitch-red/5'
    default:          return 'border-pitch-border bg-pitch-card/50'
  }
}

function statusLabel(status: AgentStatus): string {
  switch (status) {
    case 'completed': return 'Completed'
    case 'running':   return 'Running...'
    case 'failed':    return 'Failed'
    default:          return 'Queued'
  }
}

interface Props {
  progress:   AgentProgressType
  className?: string
}

export default function AgentProgress({ progress, className = '' }: Props) {
  const completedCount = Object.values(progress).filter((s) => s === 'completed').length
  const pct            = Math.round((completedCount / AGENTS.length) * 100)

  return (
    <div className={`space-y-4 ${className}`}>
      <div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-xs font-medium text-pitch-cream-dim uppercase tracking-wider">Pipeline Progress</span>
          <span className="text-xs font-mono text-pitch-lavender">{completedCount}/{AGENTS.length} · {pct}%</span>
        </div>
        <div className="h-1.5 bg-pitch-border rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-pitch-purple to-pitch-emerald rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          />
        </div>
      </div>

      <div className="space-y-2">
        {AGENTS.map((agent, i) => {
          const status = progress[agent.key] ?? 'queued'
          return (
            <motion.div
              key={agent.key}
              initial={{ opacity: 0, x: -16 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.07 }}
              className={`flex items-center gap-3 p-3 rounded-xl border transition-all duration-300 ${statusColor(status)}`}
            >
              <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
                status === 'running'   ? 'bg-pitch-purple/20 text-pitch-lavender' :
                status === 'completed' ? 'bg-pitch-emerald/15 text-pitch-emerald' :
                status === 'failed'    ? 'bg-pitch-red/15 text-pitch-red' :
                                         'bg-pitch-muted/40 text-pitch-cream-dim'
              }`}>
                {agent.icon}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-pitch-cream truncate">{agent.label}</p>
                <p className="text-xs text-pitch-cream-dim">{agent.description}</p>
              </div>
              <div className="flex items-center gap-1.5 flex-shrink-0">
                <StatusIcon status={status} />
                <span className={`text-xs font-medium ${
                  status === 'completed' ? 'text-pitch-emerald' :
                  status === 'running'   ? 'text-pitch-lavender' :
                  status === 'failed'    ? 'text-pitch-red' :
                                           'text-pitch-cream-dim'
                }`}>
                  {statusLabel(status)}
                </span>
              </div>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}