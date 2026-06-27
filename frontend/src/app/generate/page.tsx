'use client'

import { useState, useCallback } from 'react'
import { useRouter } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Zap, AlertCircle, Lightbulb, ArrowRight } from 'lucide-react'
import { generateMemo, pollJobStatus } from '@/lib/api'
import AgentProgress from '@/components/AgentProgress'
import GradientButton from '@/components/GradientButton'
import type { AgentProgress as AgentProgressType, JobStatusResponse } from '@/types'

const EXAMPLES = [
  'We are building an AI-powered legal contract review tool for small businesses in India who cannot afford lawyers. We use Gemini to analyze contracts and flag risky clauses in plain English.',
  'We are creating a B2B SaaS platform that uses computer vision to automate quality control inspections in manufacturing facilities across Southeast Asia.',
  'Our startup is a marketplace that connects rural farmers in Africa directly with urban grocery chains, eliminating middlemen and increasing farmer income by 40%.',
]

const DEFAULT_PROGRESS: AgentProgressType = {
  intake: 'queued', market_research: 'queued', funding: 'queued', vc_memo: 'queued', quality_review: 'queued',
}

type Phase = 'idle' | 'generating' | 'done' | 'error'

export default function GeneratePage() {
  const router = useRouter()
  const [description, setDescription] = useState('')
  const [phase,       setPhase]       = useState<Phase>('idle')
  const [progress,    setProgress]    = useState<AgentProgressType>(DEFAULT_PROGRESS)
  const [jobId,       setJobId]       = useState('')
  const [errorMsg,    setErrorMsg]    = useState('')

  const MIN = 50; const MAX = 5000
  const charCount = description.length
  const tooShort  = charCount > 0 && charCount < MIN
  const tooLong   = charCount > MAX
  const canSubmit = charCount >= MIN && charCount <= MAX && phase === 'idle'

  const handleGenerate = useCallback(async () => {
    if (!canSubmit) return
    setPhase('generating'); setProgress(DEFAULT_PROGRESS); setErrorMsg('')

    try {
      const { job_id } = await generateMemo(description)
      setJobId(job_id)

      pollJobStatus(
        job_id,
        (status: JobStatusResponse) => setProgress(status.agent_progress),
        (_status: JobStatusResponse) => { setPhase('done'); setTimeout(() => router.push(`/results/${job_id}`), 800) },
        (err: string) => { setPhase('error'); setErrorMsg(err) },
      )
    } catch (err) {
      setPhase('error')
      setErrorMsg(err instanceof Error ? err.message : 'Failed to start generation')
    }
  }, [description, canSubmit, router])

  return (
    <div className="min-h-screen pt-24 pb-16 px-6 relative">
      <div className="absolute top-32 left-1/2 -translate-x-1/2 w-[600px] h-[400px] bg-pitch-purple/6 blur-3xl rounded-full pointer-events-none" />
      <div className="relative z-10 max-w-3xl mx-auto">

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-10">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full glass border border-pitch-purple/30 text-xs text-pitch-lavender mb-5">
            <Zap size={12} className="text-pitch-purple" /> Powered by Google ADK · Gemini 2.5 Flash · MCP
          </div>
          <h1 className="text-4xl md:text-5xl font-display font-bold text-pitch-cream mb-3 leading-tight">
            Generate Your<br /><span className="gradient-text">Investor Memo</span>
          </h1>
          <p className="text-pitch-cream-dim text-base max-w-xl mx-auto">
            Describe your startup in plain English. Our AI agents will research your market and produce a VC-ready memo in minutes.
          </p>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}
          className="glass rounded-2xl border border-pitch-border p-6 md:p-8">

          {phase === 'idle' && (
            <div className="mb-5">
              <p className="text-xs text-pitch-cream-dim flex items-center gap-1.5 mb-2.5">
                <Lightbulb size={12} className="text-pitch-gold" /> Example descriptions:
              </p>
              <div className="space-y-2">
                {EXAMPLES.map((ex, i) => (
                  <button key={i} onClick={() => setDescription(ex)}
                    className="w-full text-left text-xs text-pitch-cream-dim hover:text-pitch-cream bg-pitch-muted/30 hover:bg-pitch-muted/60 border border-pitch-border hover:border-pitch-purple/30 rounded-xl px-3 py-2.5 transition-all line-clamp-2">
                    {ex}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div className="mb-4">
            <label className="block text-sm font-medium text-pitch-cream mb-2">Startup Description</label>
            <textarea
              value={description} onChange={(e) => setDescription(e.target.value)}
              disabled={phase !== 'idle'} rows={7}
              placeholder="Describe your startup in plain English: what you do, who your customers are, where you operate, and what problem you solve..."
              className="w-full bg-pitch-card border border-pitch-border rounded-xl px-4 py-3 text-sm text-pitch-cream placeholder:text-pitch-cream-dim/50 focus:outline-none focus:border-pitch-purple/60 focus:ring-1 focus:ring-pitch-purple/30 resize-none transition-colors disabled:opacity-60 leading-relaxed"
            />
            <div className="flex justify-between items-center mt-2">
              <span className={`text-xs ${tooShort ? 'text-pitch-gold' : tooLong ? 'text-pitch-red' : 'text-pitch-cream-dim'}`}>
                {tooShort && `${MIN - charCount} more characters needed`}
                {tooLong  && `${charCount - MAX} characters over limit`}
                {!tooShort && !tooLong && charCount > 0 && 'Looking good!'}
              </span>
              <span className={`text-xs font-mono ${tooLong ? 'text-pitch-red' : 'text-pitch-cream-dim'}`}>{charCount}/{MAX}</span>
            </div>
          </div>

          <AnimatePresence>
            {phase === 'error' && (
              <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }}
                className="mb-4 flex items-start gap-2.5 p-3.5 rounded-xl bg-pitch-red/10 border border-pitch-red/30">
                <AlertCircle size={16} className="text-pitch-red flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-medium text-pitch-red">Generation Failed</p>
                  <p className="text-xs text-pitch-red/80 mt-0.5">{errorMsg}</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          <GradientButton onClick={handleGenerate} disabled={!canSubmit} loading={phase === 'generating'} size="lg" className="w-full">
            {phase === 'generating' ? 'Agents Running...' : <><Zap size={16} /> Generate Investor Memo <ArrowRight size={16} /></>}
          </GradientButton>

          {phase === 'done' && (
            <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center text-sm text-pitch-emerald mt-3">
              ✓ Complete! Redirecting to your memo...
            </motion.p>
          )}
        </motion.div>

        <AnimatePresence>
          {(phase === 'generating' || phase === 'done') && (
            <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
              className="mt-6 glass rounded-2xl border border-pitch-border p-6">
              <h2 className="text-sm font-semibold text-pitch-cream mb-4 flex items-center gap-2">
                <Zap size={14} className="text-pitch-purple" /> Agent Pipeline · Job {jobId.slice(0, 8)}
              </h2>
              <AgentProgress progress={progress} />
            </motion.div>
          )}
        </AnimatePresence>

        {phase === 'idle' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
            className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-3">
            {[
              { t: '5 Agents',     d: 'Intake → Research → Funding → Memo → Review', c: 'text-pitch-lavender' },
              { t: 'MCP Tools',    d: 'Live web search & funding data via MCP',       c: 'text-pitch-emerald' },
              { t: '~2-3 Minutes', d: 'Full pipeline including quality review',       c: 'text-pitch-gold' },
            ].map((b) => (
              <div key={b.t} className="glass rounded-xl border border-pitch-border p-3.5 text-center">
                <p className={`text-sm font-semibold ${b.c} mb-0.5`}>{b.t}</p>
                <p className="text-xs text-pitch-cream-dim">{b.d}</p>
              </div>
            ))}
          </motion.div>
        )}
      </div>
    </div>
  )
}