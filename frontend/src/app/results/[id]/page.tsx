'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import { motion } from 'framer-motion'
import { ArrowLeft, AlertCircle, Loader2, Tag, Globe } from 'lucide-react'
import Link from 'next/link'
import { getMemo } from '@/lib/api'
import MemoViewer from '@/components/MemoViewer'
import ConfidenceGauge from '@/components/ConfidenceGauge'
import type { MemoResponse } from '@/types'

function SkeletonBlock({ className = '' }: { className?: string }) {
  return <div className={`skeleton rounded-lg ${className}`} />
}

export default function ResultsPage() {
  const params = useParams()
  const jobId  = params.id as string

  const [memo,    setMemo]    = useState<MemoResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error,   setError]   = useState('')

  useEffect(() => {
    if (!jobId) return
    getMemo(jobId)
      .then(setMemo)
      .catch((err) => setError(err instanceof Error ? err.message : 'Failed to load memo'))
      .finally(() => setLoading(false))
  }, [jobId])

  if (loading) {
    return (
      <div className="min-h-screen pt-24 pb-16 px-6">
        <div className="max-w-5xl mx-auto">
          <SkeletonBlock className="h-6 w-32 mb-8" />
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            <div className="lg:col-span-3 space-y-4">
              <SkeletonBlock className="h-10 w-64" />
              <SkeletonBlock className="h-[600px] w-full" />
            </div>
            <div className="space-y-4">
              <SkeletonBlock className="h-48 w-full" />
              <SkeletonBlock className="h-32 w-full" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen pt-24 pb-16 px-6 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="w-14 h-14 rounded-2xl bg-pitch-red/15 border border-pitch-red/30 flex items-center justify-center mx-auto mb-5">
            <AlertCircle size={24} className="text-pitch-red" />
          </div>
          <h2 className="text-xl font-bold text-pitch-cream mb-2">Failed to Load Memo</h2>
          <p className="text-pitch-cream-dim text-sm mb-6">{error}</p>
          <Link href="/generate" className="px-4 py-2 rounded-lg glass border border-pitch-border text-pitch-cream text-sm">
            New Memo
          </Link>
        </div>
      </div>
    )
  }

  if (!memo) return null

  const flags = memo.quality_flags || []

  return (
    <div className="min-h-screen pt-24 pb-16 px-6">
      <div className="fixed top-32 right-0 w-[500px] h-[500px] bg-pitch-emerald/4 blur-3xl rounded-full pointer-events-none" />
      <div className="relative z-10 max-w-6xl mx-auto">

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
          <Link href="/generate" className="inline-flex items-center gap-1.5 text-sm text-pitch-cream-dim hover:text-pitch-cream mb-8 transition-colors">
            <ArrowLeft size={15} /> Back to Generate
          </Link>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
          <h1 className="text-3xl md:text-4xl font-display font-bold text-pitch-cream mb-2">
            {memo.startup_name || 'Investor Memo'}
          </h1>
          <div className="flex flex-wrap items-center gap-2">
            {memo.industry && (
              <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-pitch-purple/15 border border-pitch-purple/25 text-xs font-medium text-pitch-lavender">
                <Tag size={11} /> {memo.industry}
              </span>
            )}
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-pitch-emerald/10 border border-pitch-emerald/20 text-xs font-medium text-pitch-emerald">
              <Globe size={11} /> Memo Ready
            </span>
            <span className="text-xs text-pitch-cream-dim font-mono">ID: {jobId.slice(0, 12)}</span>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="lg:col-span-3">
            <MemoViewer markdown={memo.memo_markdown} jobId={jobId} />
          </motion.div>

          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="space-y-4">
            {memo.confidence_score !== null && memo.confidence_score !== undefined && (
              <div className="glass rounded-2xl border border-pitch-border p-5 flex flex-col items-center">
                <p className="text-xs font-semibold text-pitch-cream uppercase tracking-wider mb-4">Quality Score</p>
                <ConfidenceGauge score={memo.confidence_score} />
              </div>
            )}

            {flags.length > 0 && (
              <div className="glass rounded-2xl border border-pitch-border p-5">
                <p className="text-xs font-semibold text-pitch-cream uppercase tracking-wider mb-3">Review Flags ({flags.length})</p>
                <ul className="space-y-2">
                  {flags.slice(0, 5).map((flag, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <AlertCircle size={12} className="text-pitch-gold flex-shrink-0 mt-0.5" />
                      <span className="text-xs text-pitch-cream-dim leading-relaxed">
                        {typeof flag === 'string' ? flag : (flag as { issue?: string }).issue || String(flag)}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <Link href="/generate"
              className="block w-full text-center px-4 py-3 rounded-xl bg-pitch-purple/20 hover:bg-pitch-purple/30 border border-pitch-purple/30 text-pitch-lavender text-sm font-semibold transition-all">
              Generate Another Memo
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  )
}