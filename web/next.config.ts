import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // MVP: Cache Components는 searchParams·Date 제약으로 우선 비활성
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
