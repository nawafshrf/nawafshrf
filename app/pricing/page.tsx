import type { Metadata } from "next";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Pricing - NotionBoost",
  description:
    "Get unlimited access to all AI tools, every template, and Gumroad publishing for $19.99/month. Free tier available.",
};

const features = [
  { name: "AI Notion Tools", free: "5 uses/day", pro: "Unlimited" },
  { name: "Browse Templates", free: true, pro: true },
  { name: "Buy Individual Templates", free: true, pro: true },
  { name: "All Templates Included", free: false, pro: true },
  { name: "Template Description Writer", free: false, pro: true },
  { name: "Gumroad Publishing", free: false, pro: true },
  { name: "Sales Dashboard", free: false, pro: true },
  { name: "Priority AI Processing", free: false, pro: true },
];

export default function PricingPage() {
  return (
    <section className="py-16 sm:py-20">
      <div className="mx-auto max-w-4xl px-4 sm:px-6">
        <div className="text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-3">
            Simple, Transparent Pricing
          </h1>
          <p className="text-gray-600 max-w-xl mx-auto">
            Start free with AI tools. Go Pro for unlimited access, all
            templates, and Gumroad marketplace publishing.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-3xl mx-auto">
          {/* Free Plan */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Free</CardTitle>
              <div className="mt-2">
                <span className="text-4xl font-bold text-gray-900">$0</span>
                <span className="text-gray-500">/month</span>
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Try AI tools and browse templates
              </p>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {features.map((feature) => (
                  <li key={feature.name} className="flex items-center gap-3 text-sm">
                    {feature.free === true ? (
                      <svg className="h-4 w-4 text-green-500 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    ) : feature.free === false ? (
                      <svg className="h-4 w-4 text-gray-300 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    ) : (
                      <span className="h-4 w-4 shrink-0" />
                    )}
                    <span className="text-gray-700">
                      {feature.name}
                      {typeof feature.free === "string" && (
                        <span className="text-gray-400 ml-1">
                          ({feature.free})
                        </span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
              <Link href="/#tools" className="block mt-6">
                <Button variant="outline" className="w-full">
                  Get Started Free
                </Button>
              </Link>
            </CardContent>
          </Card>

          {/* Pro Plan */}
          <Card className="border-orange-200 shadow-lg relative">
            <div className="absolute -top-3 left-1/2 -translate-x-1/2">
              <Badge>Most Popular</Badge>
            </div>
            <CardHeader>
              <CardTitle className="text-lg">Pro</CardTitle>
              <div className="mt-2">
                <span className="text-4xl font-bold text-gray-900">
                  $19.99
                </span>
                <span className="text-gray-500">/month</span>
              </div>
              <p className="text-sm text-gray-500 mt-2">
                Everything you need to build and sell
              </p>
            </CardHeader>
            <CardContent>
              <ul className="space-y-3">
                {features.map((feature) => (
                  <li key={feature.name} className="flex items-center gap-3 text-sm">
                    {feature.pro === true ? (
                      <svg className="h-4 w-4 text-green-500 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 12.75l6 6 9-13.5" />
                      </svg>
                    ) : (
                      <span className="h-4 w-4 shrink-0" />
                    )}
                    <span className="text-gray-700">
                      {feature.name}
                      {typeof feature.pro === "string" && (
                        <span className="text-orange-600 font-medium ml-1">
                          ({feature.pro})
                        </span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
              <form action="/api/stripe/checkout" method="POST" className="mt-6">
                <Button type="submit" className="w-full" size="lg">
                  Go Pro
                </Button>
              </form>
              <p className="text-xs text-gray-400 text-center mt-3">
                Cancel anytime. No contracts.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
