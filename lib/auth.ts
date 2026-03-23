import { type NextAuthOptions } from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { supabaseAdmin } from "./supabase";

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
    }),
    CredentialsProvider({
      name: "Email",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;
        const db = supabaseAdmin();

        const { data: user } = await db
          .from("users")
          .select("*")
          .eq("email", credentials.email)
          .single();

        if (user) {
          return {
            id: user.id,
            email: user.email,
            name: user.name,
            subscriptionStatus: user.subscription_status,
          };
        }

        const { data: newUser, error } = await db
          .from("users")
          .insert({
            email: credentials.email,
            name: credentials.email.split("@")[0],
          })
          .select()
          .single();

        if (error || !newUser) return null;

        return {
          id: newUser.id,
          email: newUser.email,
          name: newUser.name,
          subscriptionStatus: "free",
        };
      },
    }),
  ],
  callbacks: {
    async signIn({ user, account }) {
      if (account?.provider === "google" && user.email) {
        const db = supabaseAdmin();
        const { data: existingUser } = await db
          .from("users")
          .select("*")
          .eq("email", user.email)
          .single();

        if (!existingUser) {
          await db.from("users").insert({
            email: user.email,
            name: user.name,
            image: user.image,
          });
        }
      }
      return true;
    },
    async session({ session }) {
      if (session.user?.email) {
        const db = supabaseAdmin();
        const { data: dbUser } = await db
          .from("users")
          .select("id, subscription_status, stripe_customer_id")
          .eq("email", session.user.email)
          .single();

        if (dbUser) {
          (session.user as Record<string, unknown>).id = dbUser.id;
          (session.user as Record<string, unknown>).subscriptionStatus =
            dbUser.subscription_status;
          (session.user as Record<string, unknown>).stripeCustomerId =
            dbUser.stripe_customer_id;
        }
      }
      return session;
    },
  },
  pages: {
    signIn: "/auth/signin",
  },
  secret: process.env.NEXTAUTH_SECRET,
};
