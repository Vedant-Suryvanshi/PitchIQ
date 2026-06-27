'use client'

import { motion } from 'framer-motion'

interface Props { score: number }

function getColor(score: number) {
  if (score >= 0.8) return '#10B981'
  if (score >= 0.6) return '#F59E0B'
  return '#EF4444'
}

function getLabel(score: number) {
  if (score >= 0.9) return 'Excellent'
  if (score >= 0.8) return 'Very Good'
  if (score >= 0.7) return 'Good'
  if (score >= 0.6) return 'Fair'
  return 'Needs Work'
}

export default function ConfidenceGauge({ score }: Props) {
  const pct   = Math.round(score * 100)
  const color = getColor(score)
  const label = getLabel(score)
  const circumference = 2 * Math.PI * 40

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative w-28 h-28">
        <svg viewBox="0 0 100 100" className="w-full h-full -rotate-90">
          <circle cx="50" cy="50" r="40" fill="none" stroke="#1E1E2E" strokeWidth="8" />
          <motion.circle
            cx="50" cy="50" r="40"
            fill="none"
            stroke={color}
            strokeWidth="8"
            strokeLinecap="round"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: circumference * (1 - score) }}
            transition={{ duration: 1.2, ease: 'easeOut', delay: 0.3 }}
            style={{ filter: `drop-shadow(0 0 6px ${color}88)` }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            className="text-2xl font-bold font-mono"
            style={{ color }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {pct}%
          </motion.span>
        </div>
      </div>
      <div className="text-center">
        <p className="text-sm font-semibold" style={{ color }}>{label}</p>
        <p className="text-xs text-pitch-cream-dim mt-0.5">AI Quality Score</p>
      </div>
    </div>
  )
}