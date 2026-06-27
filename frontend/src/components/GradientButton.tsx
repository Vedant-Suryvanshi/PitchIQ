'use client'

import { motion } from 'framer-motion'
import { cn } from '@/lib/utils'

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?:    'sm' | 'md' | 'lg'
  loading?: boolean
  children: React.ReactNode
}

export default function GradientButton({
  variant = 'primary',
  size    = 'md',
  loading = false,
  children,
  className,
  disabled,
  ...rest
}: Props) {
  const base = 'relative inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 focus-visible:outline-none disabled:opacity-50 disabled:cursor-not-allowed overflow-hidden'

  const sizes = {
    sm: 'px-4 py-2 text-sm gap-1.5',
    md: 'px-6 py-3 text-sm gap-2',
    lg: 'px-8 py-4 text-base gap-2.5',
  }

  const variants = {
    primary:   'bg-gradient-to-r from-pitch-purple to-violet-600 text-white hover:from-violet-600 hover:to-pitch-purple shadow-lg shadow-pitch-purple/25',
    secondary: 'bg-pitch-card border border-pitch-border text-pitch-cream hover:border-pitch-purple/50',
    ghost:     'text-pitch-cream-dim hover:text-pitch-cream hover:bg-pitch-muted/40',
  }

  return (
    <motion.button
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      whileTap={{   scale: disabled || loading ? 1 : 0.98 }}
      className={cn(base, sizes[size], variants[variant], className)}
      disabled={disabled || loading}
      {...(rest as React.ButtonHTMLAttributes<HTMLButtonElement>)}
    >
      {loading && (
        <svg className="animate-spin w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      )}
      {children}
    </motion.button>
  )
}