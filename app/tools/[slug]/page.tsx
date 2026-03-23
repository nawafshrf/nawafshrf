import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { tools, getToolBySlug } from "@/lib/tools-config";
import ToolInterface from "@/components/tools/tool-interface";
import Link from "next/link";
import {
  FileText,
  Database,
  PenTool,
  CheckSquare,
  Calendar,
  BookOpen,
  Zap,
} from "lucide-react";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  FileText,
  Database,
  PenTool,
  CheckSquare,
  Calendar,
  Sigma: FileText,
  BookOpen,
  Zap,
};

export async function generateStaticParams() {
  return tools.map((tool) => ({
    slug: tool.slug,
  }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) return {};

  return {
    title: tool.metaTitle,
    description: tool.metaDescription,
    openGraph: {
      title: tool.metaTitle,
      description: tool.metaDescription,
      type: "website",
    },
  };
}

export default async function ToolPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const tool = getToolBySlug(slug);
  if (!tool) notFound();

  const Icon = iconMap[tool.icon] || FileText;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    name: tool.name,
    description: tool.metaDescription,
    applicationCategory: "UtilitiesApplication",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <section className="bg-gradient-to-b from-gray-50 to-white pt-10 pb-8">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-gray-900">
              Home
            </Link>
            <span>/</span>
            <Link href="/#tools" className="hover:text-gray-900">
              AI Tools
            </Link>
            <span>/</span>
            <span className="text-gray-900">{tool.name}</span>
          </div>

          <div className="flex items-center gap-4 mb-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-orange-100 text-orange-600">
              <Icon className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
                {tool.name}
              </h1>
              <p className="text-gray-600 mt-1">{tool.longDescription}</p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-8">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <ToolInterface tool={tool} />
        </div>
      </section>

      {/* Other Tools */}
      <section className="py-12 bg-gray-50">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            Other Notion Tools
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {tools
              .filter((t) => t.slug !== tool.slug)
              .slice(0, 4)
              .map((t) => {
                const OtherIcon = iconMap[t.icon] || FileText;
                return (
                  <Link
                    key={t.slug}
                    href={`/tools/${t.slug}`}
                    className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-3 hover:border-orange-200 hover:shadow-sm transition-all"
                  >
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-orange-50 text-orange-600 shrink-0">
                      <OtherIcon className="h-4 w-4" />
                    </div>
                    <span className="text-sm font-medium text-gray-700 truncate">
                      {t.name}
                    </span>
                  </Link>
                );
              })}
          </div>
        </div>
      </section>
    </>
  );
}
