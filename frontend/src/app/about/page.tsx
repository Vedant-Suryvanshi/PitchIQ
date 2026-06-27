'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Brain, Network, Zap, Shield, ArrowRight, BookOpen, Trophy } from 'lucide-react'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 20 }, animate: { opacity: 1, y: 0 }, transition: { duration: 0.5, delay },
})

const sections = [
  { icon: <Brain size={22} className="text-pitch-lavender" />,  color: 'from-pitch-purple/20 to-violet-600/10', border: 'border-pitch-purple/25', title: 'Google ADK',         sub: 'Agent Development Kit',     body: "Google ADK is the framework used to define, orchestrate, and run agents. PitchIQ uses ADK's sequential and parallel execution patterns — the Orchestrator runs Intake first, then fires Market Research and Funding simultaneously before synthesising the final memo." },
  { icon: <Zap size={22} className="text-pitch-gold" />,        color: 'from-amber-500/20 to-yellow-600/10',   border: 'border-amber-500/25',    title: 'Gemini 2.5 Flash',  sub: 'Google AI Studio',          body: 'Every agent uses Gemini 2.5 Flash as its language model via the GOOGLE_API_KEY from Google AI Studio. Gemini provides the reasoning, synthesis, and generation capabilities that power market research, funding analysis, memo writing, and quality review.' },
  { icon: <Network size={22} className="text-cyan-400" />,      color: 'from-cyan-500/20 to-sky-600/10',       border: 'border-cyan-500/25',     title: 'Model Context Protocol', sub: 'MCP Server',             body: "MCP standardises how agents call external tools. PitchIQ's MCP server exposes three tools — web_search, startup_research, and funding_lookup — through a single interface. Agents call tools by name; the server handles routing, validation, and error handling." },
  { icon: <Shield size={22} className="text-pitch-red" />,      color: 'from-red-500/20 to-rose-600/10',       border: 'border-red-500/25',      title: 'Security Layer',    sub: '8 Security Features',       body: 'PitchIQ includes a dedicated security module with: prompt injection detection, input validation, API rate limiting, secret management via SecretStr, environment isolation, output sanitization, secrets-free structured logging, and MCP tool whitelisting.' },
  { icon: <Trophy size={22} className="text-pitch-emerald" />,  color: 'from-emerald-500/20 to-teal-600/10',   border: 'border-emerald-500/25',  title: 'Kaggle Capstone',   sub: '5 Days AI Agents Intensive', body: 'PitchIQ was built for the Google & Kaggle "5 Days AI Agents Intensive" Capstone competition. It demonstrates multi-agent architecture, ADK orchestration, MCP integration, Gemini API usage, security features, and production deployment.' },
  { icon: <BookOpen size={22} className="text-blue-400" />,     color: 'from-blue-500/20 to-indigo-600/10',    border: 'border-blue-500/25',     title: 'Antigravity Principle', sub: 'Defying manual effort', body: 'The "antigravity" concept refers to AI lifting tasks that previously required heavy human effort. PitchIQ demonstrates this: a task that takes analysts 2-3 days (market research, competitor analysis, memo writing, fact-checking) is completed in under 5 minutes.' },
]

export default function AboutPage() {
  return (
    <div className="min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div {...fadeUp(0)} className="text-center mb-14">
          <p className="text-sm text-pitch-purple font-semibold uppercase tracking-wider mb-3">About PitchIQ</p>
          <h1 className="text-4xl md:text-5xl font-display font-bold text-pitch-cream mb-4">
            Built for the future of<br /><span className="gradient-text">AI-powered work</span>
          </h1>
          <p className="text-pitch-cream-dim max-w-xl mx-auto leading-relaxed">
            PitchIQ is a Kaggle Capstone project demonstrating production-grade multi-agent AI architecture using Google ADK, Gemini, and MCP.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {sections.map((s, i) => (
            <motion.div key={s.title} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: i * 0.08 }}
              className={`glass rounded-2xl border ${s.border} p-6`}>
              <div className={`inline-flex items-center gap-2.5 px-3 py-2 rounded-xl bg-gradient-to-br ${s.color} border ${s.border} mb-4`}>
                {s.icon}
                <div>
                  <p className="text-sm font-bold text-pitch-cream leading-tight">{s.title}</p>
                  <p className="text-xs text-pitch-cream-dim">{s.sub}</p>
                </div>
              </div>
              <p className="text-sm text-pitch-cream-dim leading-relaxed">{s.body}</p>
            </motion.div>
          ))}
        </div>

        <motion.div {...fadeUp(0.6)} className="mt-10 glass rounded-2xl border border-pitch-border p-6">
          <h2 className="text-sm font-semibold text-pitch-cream uppercase tracking-wider mb-5">Full Tech Stack</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { cat: 'Backend',  items: ['Python 3.12', 'FastAPI', 'SQLAlchemy', 'PostgreSQL'] },
              { cat: 'AI / ML',  items: ['Google ADK', 'Gemini 2.5 Flash', 'MCP SDK', 'google-generativeai'] },
              { cat: 'Frontend', items: ['Next.js 15', 'TypeScript', 'Tailwind CSS', 'Framer Motion'] },
              { cat: 'DevOps',   items: ['Docker', 'docker-compose', 'GitHub', 'Cloud Run ready'] },
            ].map((g) => (
              <div key={g.cat}>
                <p className="text-xs font-semibold text-pitch-lavender uppercase tracking-wider mb-2">{g.cat}</p>
                <ul className="space-y-1">
                  {g.items.map((item) => (
                    <li key={item} className="text-xs text-pitch-cream-dim flex items-center gap-1.5">
                      <span className="w-1 h-1 rounded-full bg-pitch-purple flex-shrink-0" /> {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div {...fadeUp(0.7)} className="mt-8 text-center">
          <Link href="/generate"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-pitch-purple to-violet-600 text-white font-semibold text-sm hover:scale-105 transition-all shadow-lg shadow-pitch-purple/30">
            Try PitchIQ Now <ArrowRight size={16} />
          </Link>
        </motion.div>
      </div>
    </div>
  )
}