import path from "path";

/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  webpack(config) {
    config.resolve.alias["@"] = path.resolve(__dirname);
    return config;
  },
};

export default nextConfig;
