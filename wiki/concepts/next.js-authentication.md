---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 nextauth (extracted)
  - 🔗 nextjs (extracted)
  - 🔗 authentication (inferred)
last_updated: 2026-04-11
tags:
  - nextjs
  - authentication
  - security
  - auth
---

# Next.js Authentication

> Authentication patterns and implementation for Next.js applications.

## Overview

Next.js supports multiple authentication patterns:
- **Server Components**: Auth in RSC, protect pages
- **Middleware**: Route-level auth checks
- **API Routes**: JWT/session verification
- **Client Components**: Client-side auth state

## NextAuth.js (Auth.js)

The recommended approach for Next.js:

### Setup
```bash
npm install next-auth
```

### Configuration (App Router)
```typescript
// auth.ts
import NextAuth from "next-auth"
import Google from "next-auth/providers/google"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [Google({
    clientId: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
  })],
  callbacks: {
    jwt({ token, user }) {
      if (user) token.id = user.id
      return token
    },
    session({ session, token }) {
      session.user.id = token.id as string
      return session
    }
  }
})
```

### Route Handler
```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth"
export const { GET, POST } = handlers
```

## Protecting Pages (Server Components)

```typescript
// app/dashboard/page.tsx
import { auth } from "@/auth"
import { redirect } from "next/navigation"

export default async function DashboardPage() {
  const session = await auth()
  
  if (!session) {
    redirect("/api/auth/signin")
  }
  
  return (
    <div>
      <h1>Welcome, {session.user.name}</h1>
      <p>Email: {session.user.email}</p>
    </div>
  )
}
```

## Middleware Protection

```typescript
// middleware.ts
export { auth as middleware } from "@/auth"

export const config = {
  matcher: ["/dashboard/:path*", "/settings/:path*", "/profile"]
}
```

## Custom Login Page

```typescript
// app/login/page.tsx
import { signIn } from "@/auth"

export default function LoginPage() {
  return (
    <form action={async () => {
      "use server"
      await signIn("google", { redirectTo: "/dashboard" })
    }}>
      <button type="submit">Sign in with Google</button>
    </form>
  )
}
```

## API Routes with Auth

```typescript
// app/api/user/route.ts
import { auth } from "@/auth"
import { NextResponse } from "next/server"

export async function GET() {
  const session = await auth()
  
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 })
  }
  
  return NextResponse.json({
    user: {
      name: session.user.name,
      email: session.user.email
    }
  })
}
```

## Client-Side Auth

```typescript
"use client"

import { useSession, signIn, signOut } from "next-auth/react"

export function AuthButton() {
  const { data: session, status } = useSession()
  
  if (status === "loading") return <p>Loading...</p>
  
  if (session) {
    return (
      <div>
        <p>{session.user.name}</p>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    )
  }
  
  return <button onClick={() => signIn()}>Sign in</button>
}
```

## Session vs JWT

| Aspect | Session (Database) | JWT |
|--------|-------------------|-----|
| Storage | Server database | Browser (client) |
| Revocation | Instant (DB delete) | Must use blocklist |
| Scale | Needs DB connection | Stateless |
| Use case | Server-rendered | API-heavy, SPA |

## Related Concepts

- [[nextauth]] — NextAuth details
- [[authentication]] — Auth fundamentals
- [[jwt]] — JWT tokens
- [[nextjs]] — Next.js framework

## External Resources

- [NextAuth.js](https://next-auth.js.org/)
- [Auth.js](https://authjs.dev/)
- [Next.js Auth Tutorial](https://nextjs.org/docs/app/building-your-application/authentication)