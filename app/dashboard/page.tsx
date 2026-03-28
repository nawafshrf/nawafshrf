import type { Metadata } from "next";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { tools } from "@/lib/tools-config";
import { getFeaturedTemplates } from "@/lib/templates-config";

export const metadata: Metadata = {
  title: "Dashboard - NotionBoost",
};

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);

  if (!session?.user) {
    redirect("/api/auth/signin?callbackUrl=/dashboard");
  }

  const user = session.user as Record<string, unknown>;
  const isPro = user.subscriptionStatus === "pro";
  const featuredTemplates = getFeaturedTemplates();

  return (
    <section className="py-12">
      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500 text-sm mt-1">
              Welcome back, {session.user.name || session.user.email}
            </p>
          </div>
          <Badge variant={isPro ? "default" : "secondary"}>
            {isPro ? "Pro" : "Free"} Plan
          </Badge>
        </div>

        <div className="grid gap-6 md:grid-cols-2 mb-8">
          {/* Subscription Card */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Subscription</CardTitle>
            </CardHeader>
            <CardContent>
              {isPro ? (
                <div>
                  <p className="text-sm text-gray-600 mb-4">
                    You have unlimited AI tools, all templates, and Gumroad
                    publishing.
                  </p>
                  <form action="/api/stripe/portal" method="POST">
                    <Button variant="outline" type="submit" size="sm">
                      Manage Subscription
                    </Button>
                  </form>
                </div>
              ) : (
                <div>
                  <p className="text-sm text-gray-600 mb-4">
                    You&apos;re on the free plan with 5 AI tool uses per day.
                  </p>
                  <Link href="/pricing">
                    <Button size="sm">Go Pro — $19.99/mo</Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Quick Access Tools */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">AI Tools</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2">
                {tools.slice(0, 6).map((tool) => (
                  <Link
                    key={tool.slug}
                    href={`/tools/${tool.slug}`}
                    className="text-sm text-orange-600 hover:text-orange-700 hover:underline"
                  >
                    {tool.name}
                  </Link>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Templates Section */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">Your Templates</CardTitle>
              {isPro && (
                <Link href="/publish">
                  <Button size="sm" variant="outline">
                    Sell on Gumroad
                  </Button>
                </Link>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {isPro ? (
              <div>
                <p className="text-sm text-gray-600 mb-4">
                  You have access to all {featuredTemplates.length}+ premium
                  templates. Browse and duplicate them to your Notion workspace.
                </p>
                <Link href="/templates">
                  <Button size="sm">Browse Templates</Button>
                </Link>
              </div>
            ) : (
              <div>
                <p className="text-sm text-gray-600 mb-4">
                  Upgrade to Pro to get access to all premium templates and
                  Gumroad publishing.
                </p>
                <Link href="/templates">
                  <Button size="sm" variant="outline">
                    Browse Templates
                  </Button>
                </Link>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Gumroad Section (Pro only) */}
        {isPro && (
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Gumroad Marketplace</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600 mb-4">
                Connect your Gumroad account to start selling Notion templates.
                Use our AI tools to create templates and write marketplace
                listings.
              </p>
              <div className="flex gap-3">
                <Button size="sm">Connect Gumroad</Button>
                <Link href="/tools/template-description">
                  <Button size="sm" variant="outline">
                    Write Template Listing
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </section>
  );
}
