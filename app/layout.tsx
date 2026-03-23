import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";

export const metadata: Metadata = {
  title: "SmartTools AI - Free AI-Powered Tools for Everyone",
  description:
    "Free AI tools for writers, developers, and marketers. Summarize text, paraphrase, check grammar, explain code, and more. No sign-up required.",
  keywords: [
    "AI tools",
    "text summarizer",
    "paraphraser",
    "grammar checker",
    "code explainer",
    "free AI tools",
  ],
  openGraph: {
    title: "SmartTools AI - Free AI-Powered Tools",
    description:
      "Free AI tools for writers, developers, and marketers. No sign-up required.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased font-sans">
        <div className="flex min-h-screen flex-col">
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
        </div>
      </body>
    </html>
  );
}
