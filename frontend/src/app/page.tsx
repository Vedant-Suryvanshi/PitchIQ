'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Zap, TrendingUp, DollarSign, FileText, Shield, ArrowRight, CheckCircle2, Brain, Network } from 'lucide-react'

const fadeUp = (delay = 0) => ({
  initial: { opacity: 0, y: 24 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, ease: 'easeOut', delay },
})

const features = [
  { icon: <TrendingUp size={20} />, color: 'from-violet-500/20 to-purple-600/20', border: 'border-violet-500/20', ic: 'text-violet-400', title: 'Market Research Agent', desc: 'Performs live web research on your industry, identifies competitors, and produces a full market intelligence report with TAM/SAM/SOM.' },
  { icon: <DollarSign size={20} />, color: 'from-emerald-500/20 to-teal-600/20', border: 'border-emerald-500/20', ic: 'text-emerald-400', title: 'Funding Intelligence Agent', desc: 'Finds comparable funding rounds, valuations, and active investors in your space so you know exactly what raise to target.' },
  { icon: <FileText size={20} />,   color: 'from-blue-500/20 to-indigo-600/20',  border: 'border-blue-500/20',   ic: 'text-blue-400',   title: 'VC Memo Agent', desc: 'Synthesises all research into a polished investor memo with executive summary, risks, moat analysis, and an investment thesis.' },
  { icon: <Shield size={20} />,     color: 'from-amber-500/20 to-orange-600/20', border: 'border-amber-500/20', ic: 'text-amber-400',   title: 'Quality Review Agent', desc: 'Acts as a skeptical VC partner — fact-checks claims, detects hallucinations, and assigns a confidence score.' },
  { icon: <Brain size={20} />,      color: 'from-pink-500/20 to-rose-600/20',    border: 'border-pink-500/20',   ic: 'text-pink-400',   title: 'Google ADK Orchestrator', desc: 'Coordinates agents using Google Agent Development Kit with sequential and parallel execution patterns.' },
  { icon: <Network size={20} />,    color: 'from-cyan-500/20 to-sky-600/20',     border: 'border-cyan-500/20',   ic: 'text-cyan-400',   title: 'MCP Server', desc: 'Model Context Protocol server exposes web_search, startup_research, and funding_lookup tools agents call in real time.' },
]

const steps = [
  { n: '01', title: 'Describe Your Startup', desc: 'Write a plain-English description of your startup idea — what you do, who you serve, and where you operate.' },
  { n: '02', title: 'Agents Run in Parallel', desc: 'The Orchestrator launches all 5 agents. Market Research and Funding agents run simultaneously via ADK parallel execution.' },
  { n: '03', title: 'Memo Gets Generated',    desc: 'The VC Memo Agent synthesises all research into a complete investor memo with every section a VC expects to see.' },
  { n: '04', title: 'Quality Reviewed',       desc: 'A Quality Review Agent scores the memo for accuracy and completeness, then returns a confidence score.' },
  { n: '05', title: 'Download Your Memo',     desc: 'View the polished memo in your browser and download it as Markdown or plain text for immediate use.' },
]

export default function HomePage() {
  return (
    <div className="relative">
      {/* HERO */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
        <div className="absolute inset-0 grid-bg opacity-60" />
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[600px] rounded-full bg-pitch-purple/8 blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-5xl mx-auto px-6 text-center">
          <motion.div {...fadeUp(0)} className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-pitch-purple/30 text-sm text-pitch-lavender mb-8">
            <Zap size={14} className="text-pitch-purple" />
            Kaggle AI Agents Capstone · Google ADK + Gemini 2.5 Flash
          </motion.div>

          <motion.h1 {...fadeUp(0.1)} className="text-5xl md:text-7xl font-display font-bold text-pitch-cream mb-6 leading-tight">
            Your startup deserves<br />
            <span className="gradient-text">an investor-grade memo.</span>
          </motion.h1>

          <motion.p {...fadeUp(0.2)} className="text-lg md:text-xl text-pitch-cream-dim max-w-2xl mx-auto mb-10 leading-relaxed">
            Describe your idea in plain English. PitchIQ&apos;s multi-agent AI system researches your market,
            finds comparable funding rounds, and generates a VC-ready investor memo in under 5 minutes.
          </motion.p>

          <motion.div {...fadeUp(0.3)} className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/generate"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-pitch-purple to-violet-600 text-white font-semibold text-base hover:scale-105 transition-all shadow-lg shadow-pitch-purple/30">
              Generate My Memo <ArrowRight size={18} />
            </Link>
            <Link href="/architecture"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl glass border border-pitch-border text-pitch-cream font-semibold text-base hover:border-pitch-purple/40 transition-all">
              View Architecture
            </Link>
          </motion.div>

          <motion.div {...fadeUp(0.4)} className="mt-16 grid grid-cols-3 gap-6 max-w-lg mx-auto">
            {[
              { v: '5',  u: 'Agents',    l: 'Specialised AI agents' },
              { v: '3',  u: 'MCP Tools', l: 'Live data tools' },
              { v: '<5', u: 'Minutes',   l: 'To investor memo' },
            ].map((s) => (
              <div key={s.u} className="text-center">
                <div className="text-3xl font-display font-bold gradient-text">{s.v}</div>
                <div className="text-sm font-semibold text-pitch-cream mt-0.5">{s.u}</div>
                <div className="text-xs text-pitch-cream-dim mt-0.5">{s.l}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* FEATURES */}
      <section className="py-24 px-6">
        <div className="max-w-7xl mx-auto">
          <motion.div {...fadeUp(0)} className="text-center mb-16">
            <p className="text-sm text-pitch-purple font-semibold uppercase tracking-wider mb-3">Multi-Agent Architecture</p>
            <h2 className="text-3xl md:text-5xl font-display font-bold text-pitch-cream mb-4">Six agents working as one</h2>
            <p className="text-pitch-cream-dim max-w-xl mx-auto">Each agent is specialised, independently testable, and orchestrated by Google ADK.</p>
          </motion.div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {features.map((f, i) => (
              <motion.div key={f.title}
                initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.08 }}
                className={`glass rounded-2xl p-6 border ${f.border} hover:scale-[1.02] transition-transform group`}>
                <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${f.color} flex items-center justify-center ${f.ic} mb-4 group-hover:scale-110 transition-transform`}>{f.icon}</div>
                <h3 className="text-base font-semibold text-pitch-cream mb-2">{f.title}</h3>
                <p className="text-sm text-pitch-cream-dim leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-24 px-6 bg-pitch-surface/40">
        <div className="max-w-4xl mx-auto">
          <motion.div {...fadeUp(0)} className="text-center mb-16">
            <p className="text-sm text-pitch-emerald font-semibold uppercase tracking-wider mb-3">How It Works</p>
            <h2 className="text-3xl md:text-4xl font-display font-bold text-pitch-cream">From idea to memo in 5 steps</h2>
          </motion.div>
          <div className="space-y-4">
            {steps.map((s, i) => (
              <motion.div key={s.n}
                initial={{ opacity: 0, x: -24 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.1 }}
                className="flex gap-5 items-start glass rounded-2xl p-5 border border-pitch-border hover:border-pitch-purple/30 transition-colors">
                <div className="flex-shrink-0 w-10 h-10 rounded-xl bg-pitch-purple/15 border border-pitch-purple/30 flex items-center justify-center">
                  <span className="text-xs font-mono font-bold text-pitch-lavender">{s.n}</span>
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-pitch-cream mb-1">{s.title}</h3>
                  <p className="text-sm text-pitch-cream-dim leading-relaxed">{s.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6">
        <motion.div initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
          className="max-w-3xl mx-auto text-center glass rounded-3xl border border-pitch-purple/20 p-12 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-pitch-purple/8 to-pitch-emerald/5 pointer-events-none" />
          <div className="relative z-10">
            <Zap size={32} className="text-pitch-purple mx-auto mb-6" />
            <h2 className="text-3xl md:text-4xl font-display font-bold text-pitch-cream mb-4">Ready to generate your memo?</h2>
            <p className="text-pitch-cream-dim mb-8 leading-relaxed">Join founders who use PitchIQ to create professional investor materials in minutes, not days.</p>
            <Link href="/generate"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-gradient-to-r from-pitch-purple to-violet-600 text-white font-semibold hover:scale-105 transition-all shadow-lg shadow-pitch-purple/30">
              Get Started Free <ArrowRight size={18} />
            </Link>
            <div className="mt-6 flex items-center justify-center gap-6 text-xs text-pitch-cream-dim">
              {['No signup required', 'Powered by Gemini 2.5', 'VC-grade output'].map((t) => (
                <span key={t} className="flex items-center gap-1.5">
                  <CheckCircle2 size={12} className="text-pitch-emerald" /> {t}
                </span>
              ))}
            </div>
          </div>
        </motion.div>
      </section>
    </div>
  )
}