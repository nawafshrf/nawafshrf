import { notFound } from "next/navigation";
import type { Metadata } from "next";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  templates,
  getTemplateBySlug,
  categoryLabels,
  categoryColors,
} from "@/lib/templates-config";

export async function generateStaticParams() {
  return templates.map((t) => ({ slug: t.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const template = getTemplateBySlug(slug);
  if (!template) return {};

  return {
    title: `${template.name} - Notion Template | NotionBoost`,
    description: template.description,
    openGraph: {
      title: `${template.name} - Notion Template`,
      description: template.description,
      type: "website",
    },
  };
}

export default async function TemplatePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const template = getTemplateBySlug(slug);
  if (!template) notFound();

  const relatedTemplates = templates
    .filter((t) => t.category === template.category && t.slug !== template.slug)
    .slice(0, 3);

  return (
    <>
      {/* Breadcrumb + Header */}
      <section className="bg-gradient-to-b from-gray-50 to-white pt-10 pb-8">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-gray-900">
              Home
            </Link>
            <span>/</span>
            <Link href="/templates" className="hover:text-gray-900">
              Templates
            </Link>
            <span>/</span>
            <span className="text-gray-900">{template.name}</span>
          </div>

          <div className="flex items-start gap-4">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-3">
                <span
                  className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                    categoryColors[template.category]
                  }`}
                >
                  {categoryLabels[template.category]}
                </span>
                {template.isNew && <Badge variant="success">New</Badge>}
                {template.isFeatured && (
                  <Badge variant="secondary">Featured</Badge>
                )}
              </div>
              <h1 className="text-2xl sm:text-3xl font-bold text-gray-900 mb-2">
                {template.name}
              </h1>
              <p className="text-gray-600 max-w-2xl">
                {template.longDescription}
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Main Content */}
      <section className="py-10">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="grid gap-8 lg:grid-cols-3">
            {/* Left: Features & Details */}
            <div className="lg:col-span-2 space-y-8">
              {/* Features */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Key Features</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="grid sm:grid-cols-2 gap-3">
                    {template.features.map((feature) => (
                      <li key={feature} className="flex items-start gap-2">
                        <svg
                          className="h-5 w-5 text-green-500 shrink-0 mt-0.5"
                          fill="none"
                          viewBox="0 0 24 24"
                          strokeWidth="2"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M4.5 12.75l6 6 9-13.5"
                          />
                        </svg>
                        <span className="text-sm text-gray-700">{feature}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>

              {/* What's Included */}
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">
                    What&apos;s Included
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {template.includes.map((item) => (
                      <li
                        key={item}
                        className="flex items-center gap-2 text-sm text-gray-700"
                      >
                        <svg
                          className="h-4 w-4 text-orange-500 shrink-0"
                          fill="none"
                          viewBox="0 0 24 24"
                          strokeWidth="2"
                          stroke="currentColor"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                          />
                        </svg>
                        {item}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            </div>

            {/* Right: Purchase Card */}
            <div>
              <Card className="sticky top-24 border-gray-200 shadow-lg">
                <CardHeader className="text-center border-b border-gray-100 pb-6">
                  <div className="text-4xl font-bold text-gray-900 mb-1">
                    ${template.price}
                  </div>
                  <p className="text-sm text-gray-500">One-time purchase</p>
                </CardHeader>
                <CardContent className="space-y-4 pt-6">
                  <form action="/api/stripe/checkout" method="POST">
                    <input
                      type="hidden"
                      name="templateId"
                      value={template.id}
                    />
                    <Button type="submit" className="w-full" size="lg">
                      Buy Template
                    </Button>
                  </form>

                  <div className="text-center">
                    <p className="text-xs text-gray-400 mb-3">or</p>
                    <Link href="/pricing">
                      <Button variant="outline" className="w-full" size="sm">
                        Get All Templates with Pro
                      </Button>
                    </Link>
                    <p className="text-xs text-gray-400 mt-2">
                      All templates + AI tools for $19.99/mo
                    </p>
                  </div>

                  <div className="border-t border-gray-100 pt-4 space-y-2">
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <svg
                        className="h-4 w-4 shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth="2"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z"
                        />
                      </svg>
                      Secure checkout via Stripe
                    </div>
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <svg
                        className="h-4 w-4 shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth="2"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      Instant access after purchase
                    </div>
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <svg
                        className="h-4 w-4 shrink-0"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth="2"
                        stroke="currentColor"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182M2.985 19.644l3.181-3.183"
                        />
                      </svg>
                      Free updates included
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Related Templates */}
      {relatedTemplates.length > 0 && (
        <section className="py-12 bg-gray-50">
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              Related Templates
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {relatedTemplates.map((t) => (
                <Link
                  key={t.slug}
                  href={`/templates/${t.slug}`}
                  className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-4 hover:border-orange-200 hover:shadow-sm transition-all"
                >
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">
                      {t.name}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      {t.description}
                    </p>
                    <p className="text-sm font-bold text-gray-900 mt-2">
                      ${t.price}
                    </p>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}
    </>
  );
}
