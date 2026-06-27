import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

export const metadata: Metadata = {
  title:       'PitchIQ — AI Investor Memo Generator',
  description: 'Generate VC-grade investor memos in minutes using Google ADK multi-agent AI powered by Gemini 2.5 Flash.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-pitch-black text-pitch-cream antialiased">
        <Navbar />
        <main className="min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  )
}