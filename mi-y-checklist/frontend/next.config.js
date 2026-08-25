/** @type {import('next').NextConfig} */
// Rewrite rule was: /api/local/* → NEXT_PUBLIC_API_BASE.  Replaced because Vercel
// rewrites can only point to relative / Vercel-internal hosts, not arbitrary HTTPS.
// The page now reads NEXT_PUBLIC_API_BASE directly and calls it client-side.
const nextConfig = {
  reactStrictMode: true,
};
module.exports = nextConfig;
