import type { Metadata } from "next";
import "./globals.css";
import Header from "@/components/layout/header";
import Footer from "@/components/layout/footer";

export const metadata: Metadata = {
  title: "NotionBoost - AI-Powered Notion Templates & Tools",
  description:
    "Premium Notion templates and AI tools for productivity. Template shop, AI page enhancer, database generator, formula helper, and more. Publish to Gumroad marketplace.",
  keywords: [
    "Notion templates",
    "Notion tools",
    "AI Notion",
    "Notion database generator",
    "Notion formula helper",
    "Gumroad templates",
    "Notion marketplace",
    "productivity templates",
  ],
  openGraph: {
    title: "NotionBoost - AI-Powered Notion Templates & Tools",
    description:
      "Premium Notion templates and AI tools. Build, buy, and sell Notion templates with AI assistance.",
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
