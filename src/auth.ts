import NextAuth from "next-auth"
import Google from "next-auth/providers/google"
import type { NextAuthConfig } from "next-auth"

export const authConfig: NextAuthConfig = {
    providers: [
        Google({
            clientId: process.env.GOOGLE_CLIENT_ID!,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
        }),
    ],
    callbacks: {
        authorized({ auth, request: { nextUrl } }) {
            const isLoggedIn = !!auth?.user
            const isOnApp = nextUrl.pathname === '/'

            // Allow access to the app without login, but API routes require auth
            if (nextUrl.pathname.startsWith('/api/runs')) {
                return isLoggedIn
            }

            return true
        },
        async session({ session, token }) {
            if (session.user && token.sub) {
                session.user.id = token.sub
            }
            return session
        },
    },
    pages: {
        signIn: '/', // Redirect to home page for sign in
    },
}

export const { handlers, auth, signIn, signOut } = NextAuth(authConfig)
