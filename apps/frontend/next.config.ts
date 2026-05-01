import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@docuweave/shared-types"],
};

export default nextConfig;
