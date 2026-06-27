'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Copy, Check, Download, FileText } from 'lucide-react'

interface Props { markdown: string; jobId: string }

export default function MemoViewer({ markdown, jobId }: Props) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(markdown)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownloadMd = () => {
    const blob = new Blob([markdown], { type: 'text/markdown' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href = url; a.download = `pitchiq-memo-${jobId.slice(0, 8)}.md`; a.click()
    URL.revokeObjectURL(url)
  }

  const handleDownloadTxt = () => {
    const text = markdown.replace(/#{1,6}\s/g, '').replace(/\*\*(.*?)\*\*/g, '$1').replace(/\*(.*?)\*/g, '$1')
    const blob = new Blob([text], { type: 'text/plain' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href = url; a.download = `pitchiq-memo-${jobId.slice(0, 8)}.txt`; a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="glass rounded-2xl border border-pitch-border overflow-hidden">
      <div className="flex items-center justify-between px-5 py-3 border-b border-pitch-border bg-pitch-card/60">
        <div className="flex items-center gap-2">
          <FileText size={15} className="text-pitch-purple" />
          <span className="text-sm font-medium text-pitch-cream">Investor Memo</span>
          <span className="text-xs text-pitch-cream-dim font-mono bg-pitch-muted/50 px-2 py-0.5 rounded">
            {jobId.slice(0, 8)}
          </span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleCopy}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-pitch-muted/50 hover:bg-pitch-muted text-pitch-cream-dim hover:text-pitch-cream transition-all">
            {copied ? <Check size={13} className="text-pitch-emerald" /> : <Copy size={13} />}
            {copied ? 'Copied!' : 'Copy'}
          </button>
          <button onClick={handleDownloadMd}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-pitch-purple/20 hover:bg-pitch-purple/30 text-pitch-lavender transition-all">
            <Download size={13} /> .md
          </button>
          <button onClick={handleDownloadTxt}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-pitch-emerald/15 hover:bg-pitch-emerald/25 text-pitch-emerald transition-all">
            <Download size={13} /> .txt
          </button>
        </div>
      </div>
      <div className="p-6 md:p-8 max-h-[70vh] overflow-y-auto">
        <div className="memo-prose max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}