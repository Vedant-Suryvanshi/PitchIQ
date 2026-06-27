import Link from 'next/link'
import { Zap, Github, ExternalLink } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="border-t border-pitch-border bg-pitch-surface/50 mt-24">
      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          <div>
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-pitch-purple to-pitch-emerald flex items-center justify-center">
                <Zap size={14} className="text-white" />
              </div>
              <span className="font-display font-bold text-pitch-cream">
                Pitch<span className="text-pitch-purple">IQ</span>
              </span>
            </Link>
            <p className="text-sm text-pitch-cream-dim leading-relaxed">
              AI-powered investor memo generator built for the Google &amp; Kaggle AI Agents Intensive Capstone.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-pitch-cream mb-4 uppercase tracking-wider">Navigation</h4>
            <ul className="space-y-2">
              {[
                { href: '/',             label: 'Home' },
                { href: '/generate',     label: 'Generate Memo' },
                { href: '/architecture', label: 'Architecture' },
                { href: '/about',        label: 'About' },
              ].map((l) => (
                <li key={l.href}>
                  <Link href={l.href} className="text-sm text-pitch-cream-dim hover:text-pitch-lavender transition-colors">
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-pitch-cream mb-4 uppercase tracking-wider">Powered By</h4>
            <ul className="space-y-2">
              {['Google ADK', 'Gemini 2.5 Flash', 'Model Context Protocol', 'FastAPI + Python', 'Next.js 15'].map((t) => (
                <li key={t} className="text-sm text-pitch-cream-dim flex items-center gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-pitch-purple inline-block" />
                  {t}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-pitch-border flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-xs text-pitch-cream-dim">
            © 2026 PitchIQ · Built for Kaggle AI Agents Capstone
          </p>
          <div className="flex items-center gap-4">
            <a href="https://www.kaggle.com" target="_blank" rel="noopener noreferrer"
              className="text-xs text-pitch-cream-dim hover:text-pitch-lavender flex items-center gap-1 transition-colors">
              Kaggle <ExternalLink size={11} />
            </a>
            <a href="https://github.com" target="_blank" rel="noopener noreferrer"
              className="text-xs text-pitch-cream-dim hover:text-pitch-lavender flex items-center gap-1 transition-colors">
              GitHub <Github size={11} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}