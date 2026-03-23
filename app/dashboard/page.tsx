import type { Metadata } from "next";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { tools } from "@/lib/tools-config";

export const metadata: Metadata = {
  title: "Dashboard - SmartTools AI",
};

export default async function DashboardPage() {
  const session = await getServerSession(authOptions);

  if (!session?.user) {
    redirect("/api/auth/signin?callbackUrl=/dashboard");
  }

  const user = session.user as Record<string, unknown>;
  const isPro = user.subscriptionStatus === "pro";

  return (
    <section className="py-12">
      <div className="mx-auto max-w-4xl px-4 sm:px-6">
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
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Subscription</CardTitle>
            </CardHeader>
            <CardContent>
              {isPro ? (
                <div>
                  <p className="text-sm text-gray-600 mb-4">
                    You have unlimited access to all tools.
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
                    You&apos;re on the free plan with limited daily uses.
                  </p>
                  <Link href="/pricing">
                    <Button size="sm">Upgrade to Pro</Button>
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Access</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 gap-2">
                {tools.slice(0, 4).map((tool) => (
                  <Link
                    key={tool.slug}
                    href={`/tools/${tool.slug}`}
                    className="text-sm text-blue-600 hover:text-blue-700 hover:underline"
                  >
                    {tool.name}
                  </Link>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
}
