// frontend/src/app/architecture/page.tsx
'use client'

import { motion } from 'framer-motion'
import { User, Brain, TrendingUp, DollarSign, FileText, Shield, Network, Database, Zap, ArrowDown } from 'lucide-react'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.5, delay },
})

interface NodeProps { icon: React.ReactNode; label: string; sub?: string; color: string; border: string; delay?: number }

function Node({ icon, label, sub, color, border, delay = 0 }: NodeProps) {
  return (
    <motion.div {...fadeUp(delay)} className={`glass rounded-2xl border ${border} p-4 flex flex-col items-center gap-2 text-center hover:scale-105 transition-transform`}>
      <div className={`w-10 h-10 rounded-xl ${color} flex items-center justify-center`}>{icon}</div>
      <p className="text-sm font-semibold text-pitch-cream">{label}</p>
      {sub && <p className="text-xs text-pitch-cream-dim">{sub}</p>}
    </motion.div>
  )
}

export default function ArchitecturePage() {
  return (
    <div className="min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-5xl mx-auto">
        <motion.div {...fadeUp(0)} className="text-center mb-14">
          <p className="text-sm text-pitch-purple font-semibold uppercase tracking-wider mb-3">System Design</p>
          <h1 className="text-4xl md:text-5xl font-display font-bold text-pitch-cream mb-4">PitchIQ Architecture</h1>
          <p className="text-pitch-cream-dim max-w-xl mx-auto">A production-grade multi-agent system built with Google ADK, Model Context Protocol, and Gemini 2.5 Flash.</p>
        </motion.div>

        <div className="space-y-4">
          <div className="flex justify-center">
            <div className="w-48">
              <Node icon={<User size={18} className="text-white" />} label="Founder" sub="Startup description" color="bg-slate-600" border="border-slate-500/30" delay={0} />
            </div>
          </div>
          <div className="flex justify-center"><ArrowDown size={20} className="text-pitch-purple" /></div>

          <motion.div {...fadeUp(0.1)} className="glass rounded-2xl border border-pitch-red/25 bg-pitch-red/5 p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-1">
              <Shield size={16} className="text-pitch-red" />
              <p className="text-sm font-semibold text-pitch-cream">Security Layer</p>
            </div>
            <p className="text-xs text-pitch-cream-dim">Prompt injection · Input validation · Rate limiting · Output sanitization</p>
          </motion.div>
          <div className="flex justify-center"><ArrowDown size={20} className="text-pitch-purple" /></div>

          <motion.div {...fadeUp(0.15)} className="glass rounded-2xl border border-blue-500/25 bg-blue-500/5 p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-1">
              <Zap size={16} className="text-blue-400" />
              <p className="text-sm font-semibold text-pitch-cream">FastAPI Backend</p>
            </div>
            <p className="text-xs text-pitch-cream-dim">POST /api/generate · GET /api/status · GET /api/memo · GET /api/mcp/tools</p>
          </motion.div>
          <div className="flex justify-center"><ArrowDown size={20} className="text-pitch-purple" /></div>

          <div className="flex justify-center">
            <div className="w-72">
              <Node icon={<Brain size={18} className="text-white" />} label="Orchestrator Agent" sub="Google ADK · Sequential + Parallel" color="bg-gradient-to-br from-pitch-purple to-violet-700" border="border-pitch-purple/40" delay={0.2} />
            </div>
          </div>

          <motion.div {...fadeUp(0.3)} className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Node icon={<FileText size={16} className="text-amber-300" />}    label="Intake Agent"    sub="Profile extraction"   color="bg-amber-500/20"   border="border-amber-500/25"   delay={0.3} />
            <Node icon={<TrendingUp size={16} className="text-violet-300" />} label="Market Research" sub="Trends · competitors"  color="bg-violet-500/20"  border="border-violet-500/25"  delay={0.35} />
            <Node icon={<DollarSign size={16} className="text-emerald-300" />}label="Funding Intel"   sub="Rounds · valuations"  color="bg-emerald-500/20" border="border-emerald-500/25" delay={0.4} />
            <Node icon={<FileText size={16} className="text-blue-300" />}     label="VC Memo Agent"  sub="Memo synthesis"       color="bg-blue-500/20"    border="border-blue-500/25"    delay={0.45} />
          </motion.div>

          <div className="flex justify-center gap-32">
            <ArrowDown size={18} className="text-pitch-purple/60" />
            <ArrowDown size={18} className="text-pitch-purple/60" />
          </div>

          <motion.div {...fadeUp(0.5)} className="glass rounded-2xl border border-cyan-500/25 bg-cyan-500/5 p-4 text-center">
            <div className="flex items-center justify-center gap-2 mb-1">
              <Network size={16} className="text-cyan-400" />
              <p className="text-sm font-semibold text-pitch-cream">MCP Server</p>
            </div>
            <div className="flex flex-wrap justify-center gap-3 mt-2">
              {['web_search', 'startup_research', 'funding_lookup'].map((t) => (
                <span key={t} className="text-xs bg-cyan-500/15 border border-cyan-500/25 text-cyan-300 px-2.5 py-1 rounded-lg font-mono">{t}</span>
              ))}
            </div>
          </motion.div>
          <div className="flex justify-center"><ArrowDown size={20} className="text-pitch-purple" /></div>

          <div className="flex justify-center">
            <div className="w-72">
              <Node icon={<Shield size={18} className="text-white" />} label="Quality Review Agent" sub="Fact-check · confidence score" color="bg-gradient-to-br from-pitch-emerald to-teal-600" border="border-pitch-emerald/40" delay={0.6} />
            </div>
          </div>
          <div className="flex justify-center"><ArrowDown size={20} className="text-pitch-purple" /></div>

          {/* Updated: PostgreSQL instead of SQLite */}
          <div className="grid grid-cols-2 gap-4">
            <Node icon={<Database size={18} className="text-indigo-300" />} label="PostgreSQL"  sub="Jobs · memos · results" color="bg-indigo-500/20" border="border-indigo-500/25" delay={0.65} />
            <Node icon={<Zap size={18} className="text-pitch-gold" />}      label="Gemini 2.5 Flash" sub="All agent LLM calls"    color="bg-amber-500/20"  border="border-amber-500/25"  delay={0.7} />
          </div>
        </div>

        <motion.div {...fadeUp(0.8)} className="mt-12 glass rounded-2xl border border-pitch-border p-6">
          <h2 className="text-sm font-semibold text-pitch-cream uppercase tracking-wider mb-4">Key Design Principles</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { t: 'ADK Parallel Execution', d: 'Market Research and Funding agents run simultaneously using asyncio.gather(), cutting pipeline time in half.', c: 'text-pitch-lavender' },
              { t: 'MCP Tool Protocol',      d: 'Agents call tools via a standard MCP interface — swappable, testable, and auditable in one place.',            c: 'text-cyan-400' },
              { t: 'Security First',         d: 'Every input is scanned for prompt injection before reaching an agent. Every output is sanitized before delivery.', c: 'text-pitch-red' },
            ].map((p) => (
              <div key={p.t} className="space-y-1.5">
                <h3 className={`text-sm font-semibold ${p.c}`}>{p.t}</h3>
                <p className="text-xs text-pitch-cream-dim leading-relaxed">{p.d}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}