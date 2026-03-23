import type { Metadata } from "next";
import TemplateCard from "@/components/templates/template-card";
import {
  templates,
  categoryLabels,
  type TemplateCategory,
} from "@/lib/templates-config";

export const metadata: Metadata = {
  title: "Notion Templates - NotionBoost",
  description:
    "Premium Notion templates for freelancers, students, creators, and startups. Ready to duplicate and customize.",
};

export default function TemplatesPage() {
  const categories = Object.keys(categoryLabels) as TemplateCategory[];

  return (
    <section className="py-12 sm:py-16">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">
            Notion Template Shop
          </h1>
          <p className="text-gray-600 max-w-xl mx-auto">
            Professionally designed templates ready to duplicate into your
            Notion workspace. All databases, views, and formulas included.
          </p>
        </div>

        {/* Category Filters */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-10">
          <span className="inline-flex items-center rounded-full bg-gray-900 px-4 py-1.5 text-sm text-white font-medium cursor-pointer">
            All Templates
          </span>
          {categories.map((cat) => (
            <span
              key={cat}
              className="inline-flex items-center rounded-full bg-gray-100 px-4 py-1.5 text-sm text-gray-600 font-medium hover:bg-gray-200 cursor-pointer transition-colors"
            >
              {categoryLabels[cat]}
            </span>
          ))}
        </div>

        {/* Templates Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {templates.map((template) => (
            <TemplateCard key={template.id} template={template} />
          ))}
        </div>

        {/* Pro CTA */}
        <div className="mt-16 text-center rounded-2xl bg-gray-50 border border-gray-200 px-6 py-10">
          <h2 className="text-xl font-bold text-gray-900 mb-2">
            Get All Templates with Pro
          </h2>
          <p className="text-gray-600 text-sm mb-4 max-w-md mx-auto">
            Pro members get access to every template in the shop plus unlimited
            AI tools and Gumroad publishing.
          </p>
          <a
            href="/pricing"
            className="inline-flex items-center justify-center rounded-lg bg-gray-900 px-6 py-2.5 text-sm font-medium text-white hover:bg-gray-800 transition-colors"
          >
            Go Pro — $19.99/mo
          </a>
        </div>
      </div>
    </section>
  );
}
