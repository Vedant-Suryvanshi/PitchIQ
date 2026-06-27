/** @type {import('next').NextConfig} */
const nextConfig = {
  // TypeScript settings
  typescript: {
    ignoreBuildErrors: true,  // This helps during Docker build
  },
  // ESLint settings
  eslint: {
    ignoreDuringBuilds: true, // This helps during Docker build
  },
  // Output standalone for smaller Docker images (optional)
  output: 'standalone',
  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000',
  },
}

module.exports = nextConfig