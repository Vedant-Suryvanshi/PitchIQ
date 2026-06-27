'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Zap, Menu, X } from 'lucide-react'

const links = [
  { href: '/',             label: 'Home' },
  { href: '/generate',     label: 'Generate' },
  { href: '/architecture', label: 'Architecture' },
  { href: '/about',        label: 'About' },
]

export default function Navbar() {
  const pathname = usePathname()
  const [scrolled, setScrolled] = useState(false)
  const [open,     setOpen]     = useState(false)

  useEffect(() => {
    const fn = () => setScrolled(window.scrollY > 20)
    window.addEventListener('scroll', fn)
    return () => window.removeEventListener('scroll', fn)
  }, [])

  return (
    <motion.header
      initial={{ y: -80, opacity: 0 }}
      animate={{ y: 0,   opacity: 1 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'glass-strong border-b border-pitch-border' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-pitch-purple to-pitch-emerald flex items-center justify-center group-hover:scale-110 transition-transform">
            <Zap size={16} className="text-white" />
          </div>
          <span className="font-display text-lg font-bold text-pitch-cream tracking-tight">
            Pitch<span className="text-pitch-purple">IQ</span>
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-1">
          {links.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                pathname === l.href
                  ? 'bg-pitch-purple/20 text-pitch-lavender'
                  : 'text-pitch-cream-dim hover:text-pitch-cream hover:bg-pitch-muted/50'
              }`}
            >
              {l.label}
            </Link>
          ))}
        </nav>

        <div className="hidden md:flex">
          <Link
            href="/generate"
            className="px-4 py-2 rounded-lg bg-pitch-purple hover:bg-pitch-purple/80 text-white text-sm font-semibold transition-all hover:shadow-lg hover:shadow-pitch-purple/25"
          >
            Generate Memo →
          </Link>
        </div>

        <button
          className="md:hidden text-pitch-cream-dim hover:text-pitch-cream"
          onClick={() => setOpen(!open)}
        >
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{   opacity: 0, height: 0 }}
            className="md:hidden glass-strong border-t border-pitch-border"
          >
            <nav className="flex flex-col p-4 gap-1">
              {links.map((l) => (
                <Link
                  key={l.href}
                  href={l.href}
                  onClick={() => setOpen(false)}
                  className={`px-4 py-3 rounded-lg text-sm font-medium transition-all ${
                    pathname === l.href
                      ? 'bg-pitch-purple/20 text-pitch-lavender'
                      : 'text-pitch-cream-dim hover:text-pitch-cream'
                  }`}
                >
                  {l.label}
                </Link>
              ))}
              <Link
                href="/generate"
                onClick={() => setOpen(false)}
                className="mt-2 px-4 py-3 rounded-lg bg-pitch-purple text-white text-sm font-semibold text-center"
              >
                Generate Memo →
              </Link>
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.header>
  )
}