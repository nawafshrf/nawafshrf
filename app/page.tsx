import Link from "next/link";
import { Button } from "@/components/ui/button";
import ToolCard from "@/components/tools/tool-card";
import { tools } from "@/lib/tools-config";

export default function Home() {
  return (
    <>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white pt-16 pb-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-700 mb-6">
              No sign-up required &middot; 100% free to start
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-gray-900 mb-6">
              Free AI Tools for{" "}
              <span className="text-blue-600">Everyone</span>
            </h1>
            <p className="text-lg sm:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Summarize text, rewrite content, check grammar, explain code, and
              more. Powered by AI, built for speed. Just paste and click.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="#tools">
                <Button size="lg" className="text-base px-8">
                  Try Free Tools
                </Button>
              </Link>
              <Link href="/pricing">
                <Button variant="outline" size="lg" className="text-base px-8">
                  View Pricing
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Tools Grid */}
      <section id="tools" className="py-16 sm:py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              8 AI-Powered Tools
            </h2>
            <p className="text-gray-600 max-w-xl mx-auto">
              Each tool is designed for a specific task. No prompts to write, no
              accounts to create. Just paste your content and get instant
              results.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {tools.map((tool) => (
              <ToolCard key={tool.slug} tool={tool} />
            ))}
          </div>
        </div>
      </section>

      {/* Why SmartTools */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              Why SmartTools AI?
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-blue-100 text-blue-600 mb-4">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Instant Results
              </h3>
              <p className="text-gray-600 text-sm">
                No prompts to craft. Just paste your text, click a button, and
                get results in seconds.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600 mb-4">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                No Sign-Up Needed
              </h3>
              <p className="text-gray-600 text-sm">
                Start using all tools immediately. No account, no credit card,
                no hassle.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-purple-600 mb-4">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Private & Secure
              </h3>
              <p className="text-gray-600 text-sm">
                Your data is never stored or used for training. Process and
                forget.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="rounded-2xl bg-blue-600 px-6 py-12 sm:px-12 text-center">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-4">
              Need Unlimited Access?
            </h2>
            <p className="text-blue-100 mb-6 max-w-xl mx-auto">
              Upgrade to Pro for unlimited uses across all tools. Just $9.99/month.
              Cancel anytime.
            </p>
            <Link href="/pricing">
              <Button
                size="lg"
                className="bg-white text-blue-600 hover:bg-blue-50 text-base px-8"
              >
                Get Pro Access
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-gray-50">
        <div className="mx-auto max-w-3xl px-4 sm:px-6">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Frequently Asked Questions
          </h2>

          <div className="space-y-6">
            {[
              {
                q: "Is SmartTools AI really free?",
                a: "Yes! You get 5 free uses per day across all tools. No sign-up, no credit card required. If you need more, Pro is just $9.99/month for unlimited access.",
              },
              {
                q: "How is this different from ChatGPT?",
                a: "SmartTools AI gives you purpose-built tools optimized for specific tasks. No prompt crafting needed — just paste and click. It's faster and simpler for common tasks like summarizing, paraphrasing, and grammar checking.",
              },
              {
                q: "Is my data safe?",
                a: "Absolutely. We don't store your text or use it for training. Your content is processed and immediately discarded.",
              },
              {
                q: "Can I cancel Pro anytime?",
                a: "Yes, cancel anytime with one click. No contracts, no hidden fees. You'll keep Pro access until the end of your billing period.",
              },
            ].map((faq) => (
              <div
                key={faq.q}
                className="rounded-lg bg-white border border-gray-200 p-6"
              >
                <h3 className="text-base font-semibold text-gray-900 mb-2">
                  {faq.q}
                </h3>
                <p className="text-sm text-gray-600">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
