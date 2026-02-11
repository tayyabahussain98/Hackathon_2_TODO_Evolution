import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Ensure proper CSS handling in production
  output: 'standalone',
  experimental: {
    // Ensure CSS is properly bundled
    optimizePackageImports: ['lucide-react'],
  },
};

export default nextConfig;
