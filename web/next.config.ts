import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure proper handling of dynamic pages on Vercel
  experimental: {
    serverComponentsExternalPackages: [],
  },
  // Optimize for Vercel deployment
  trailingSlash: false,
  // Ensure proper CSP for media content
  async headers() {
    return [
      {
        source: '/player',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
