import type { Metadata } from "next";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Sell Notion Templates on Gumroad - NotionBoost",
  description:
    "Create Notion templates with AI and publish them directly to Gumroad. Turn your Notion skills into passive income.",
};

const steps = [
  {
    step: "1",
    title: "Design with AI",
    description:
      "Use our AI tools to generate database schemas, write SOPs, create content calendars, and build complete Notion templates faster.",
    tools: ["Database Generator", "SOP Generator", "Formula Helper"],
  },
  {
    step: "2",
    title: "Write Your Listing",
    description:
      "Our Template Description Writer creates marketplace-ready copy that sells. Optimized headlines, feature bullets, and SEO tags.",
    tools: ["Template Description Writer"],
  },
  {
    step: "3",
    title: "Publish to Gumroad",
    description:
      "Connect your Gumroad account and publish your template with one click. We handle the listing, you keep the revenue.",
    tools: ["Gumroad Integration"],
  },
  {
    step: "4",
    title: "Earn Passive Income",
    description:
      "Your template is live on Gumroad's marketplace reaching millions of buyers. Track sales from your NotionBoost dashboard.",
    tools: ["Sales Dashboard"],
  },
];

const tips = [
  {
    title: "Solve a Specific Problem",
    description:
      "The best-selling templates solve one clear problem. 'Freelancer CRM' beats 'All-in-one workspace'.",
  },
  {
    title: "Include Clear Documentation",
    description:
      "Add a setup guide page inside your template. Use our SOP Generator to create professional docs.",
  },
  {
    title: "Use Real Example Data",
    description:
      "Pre-fill your template with realistic example entries. Buyers want to see how it looks in action.",
  },
  {
    title: "Price for Value",
    description:
      "Templates priced $15-35 sell best. Think about the hours your template saves the buyer.",
  },
  {
    title: "Write Great Screenshots",
    description:
      "Show different views (table, board, calendar). Buyers need to visualize the template in their workflow.",
  },
  {
    title: "Update Regularly",
    description:
      "Templates that get updates rank higher. Add new views or features based on buyer feedback.",
  },
];

export default function PublishPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-gradient-to-b from-gray-50 to-white pt-16 pb-12">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 text-center">
          <div className="inline-flex items-center rounded-full bg-green-100 px-3 py-1 text-sm text-green-700 mb-6">
            Passive Income from Notion Templates
          </div>
          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-gray-900 mb-4 max-w-3xl mx-auto">
            Build Templates with AI.{" "}
            <span className="text-orange-500">Sell on Gumroad.</span>
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
            Use our AI tools to design Notion templates, generate marketplace
            listings, and publish directly to Gumroad. Keep 100% of your
            revenue.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link href="/pricing">
              <Button size="lg" className="text-base px-8">
                Start Selling — Go Pro
              </Button>
            </Link>
            <Link href="/#tools">
              <Button variant="outline" size="lg" className="text-base px-8">
                Try AI Tools Free
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-12">
            How It Works
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {steps.map((s) => (
              <Card key={s.step} className="relative">
                <CardHeader>
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-orange-100 text-orange-600 font-bold text-lg mb-3">
                    {s.step}
                  </div>
                  <CardTitle className="text-lg">{s.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-3">{s.description}</p>
                  <div className="flex flex-wrap gap-1.5">
                    {s.tools.map((tool) => (
                      <span
                        key={tool}
                        className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
                      >
                        {tool}
                      </span>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Gumroad Integration */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-4xl px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-2xl font-bold text-gray-900 mb-3">
              Direct Gumroad Integration
            </h2>
            <p className="text-gray-600 max-w-xl mx-auto">
              Connect your Gumroad account and publish templates with
              AI-generated listings. No copy-pasting needed.
            </p>
          </div>

          <Card>
            <CardContent className="p-8">
              <div className="grid sm:grid-cols-2 gap-8">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    What We Handle
                  </h3>
                  <ul className="space-y-2">
                    {[
                      "AI-written product descriptions",
                      "SEO-optimized tags and categories",
                      "Pricing suggestions based on market data",
                      "Automatic listing creation via Gumroad API",
                      "Sales tracking in your dashboard",
                    ].map((item) => (
                      <li
                        key={item}
                        className="flex items-center gap-2 text-sm text-gray-700"
                      >
                        <svg
                          className="h-4 w-4 text-green-500 shrink-0"
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
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 mb-3">
                    What You Keep
                  </h3>
                  <ul className="space-y-2">
                    {[
                      "100% of your template revenue",
                      "Full ownership of your templates",
                      "Direct customer relationships",
                      "Your own Gumroad store brand",
                      "All customer emails and data",
                    ].map((item) => (
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
                            d="M4.5 12.75l6 6 9-13.5"
                          />
                        </svg>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Tips */}
      <section className="py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-3">
            Tips for Selling Templates
          </h2>
          <p className="text-gray-600 text-center mb-10 max-w-xl mx-auto">
            Advice from top Notion template creators earning $5K+/month
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {tips.map((tip) => (
              <div
                key={tip.title}
                className="rounded-lg border border-gray-200 bg-white p-5"
              >
                <h3 className="text-sm font-semibold text-gray-900 mb-1">
                  {tip.title}
                </h3>
                <p className="text-sm text-gray-600">{tip.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-3">
            Ready to Start Earning?
          </h2>
          <p className="text-gray-600 mb-6">
            Pro members get full access to all AI tools for template creation
            plus direct Gumroad publishing.
          </p>
          <Link href="/pricing">
            <Button size="lg" className="text-base px-8">
              Go Pro — $19.99/mo
            </Button>
          </Link>
        </div>
      </section>
    </>
  );
}
