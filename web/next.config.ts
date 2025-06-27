import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Optimize for Vercel deployment
  trailingSlash: false,
  // Force all pages to be dynamic to avoid SSG issues
  output: 'standalone',
};

export default nextConfig;
