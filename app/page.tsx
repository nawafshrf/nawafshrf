import Link from "next/link";
import { Button } from "@/components/ui/button";
import ToolCard from "@/components/tools/tool-card";
import TemplateCard from "@/components/templates/template-card";
import { tools } from "@/lib/tools-config";
import { getFeaturedTemplates } from "@/lib/templates-config";

export default function Home() {
  const featuredTemplates = getFeaturedTemplates();

  return (
    <>
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-50 to-white pt-16 pb-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center max-w-3xl mx-auto">
            <div className="inline-flex items-center rounded-full bg-orange-100 px-3 py-1 text-sm text-orange-700 mb-6">
              Notion Templates + AI Tools + Marketplace
            </div>
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-gray-900 mb-6">
              Supercharge Your{" "}
              <span className="text-orange-500">Notion</span> Workspace
            </h1>
            <p className="text-lg sm:text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Premium templates, AI-powered tools, and a marketplace to sell
              your own. Everything you need to build the perfect Notion setup.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/templates">
                <Button size="lg" className="text-base px-8">
                  Browse Templates
                </Button>
              </Link>
              <Link href="#tools">
                <Button variant="outline" size="lg" className="text-base px-8">
                  Try AI Tools Free
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Templates */}
      <section className="py-16 sm:py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-2">
                Featured Templates
              </h2>
              <p className="text-gray-600">
                Ready-to-use Notion templates for every workflow
              </p>
            </div>
            <Link href="/templates">
              <Button variant="outline" size="sm">
                View All
              </Button>
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredTemplates.slice(0, 6).map((template) => (
              <TemplateCard key={template.id} template={template} />
            ))}
          </div>
        </div>
      </section>

      {/* AI Tools Grid */}
      <section id="tools" className="py-16 sm:py-20 bg-gray-50">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              AI Tools for Notion Users
            </h2>
            <p className="text-gray-600 max-w-xl mx-auto">
              Powered by AI, built specifically for Notion. Generate databases,
              write formulas, plan content, and more.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {tools.map((tool) => (
              <ToolCard key={tool.slug} tool={tool} />
            ))}
          </div>
        </div>
      </section>

      {/* Why NotionBoost */}
      <section className="py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-3">
              Why NotionBoost?
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-orange-100 text-orange-600 mb-4">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                AI-Powered Tools
              </h3>
              <p className="text-gray-600 text-sm">
                Generate databases, formulas, SOPs, and content calendars with
                AI built specifically for Notion workflows.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600 mb-4">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25L5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Premium Templates
              </h3>
              <p className="text-gray-600 text-sm">
                Professionally designed Notion templates for freelancers,
                students, creators, and startups. Ready to duplicate.
              </p>
            </div>

            <div className="text-center">
              <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-purple-600 mb-4">
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5M9 11.25v1.5M12 9v3.75m3-6v6" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Sell on Gumroad
              </h3>
              <p className="text-gray-600 text-sm">
                Build templates with AI assistance and publish them directly to
                Gumroad. Turn your Notion skills into passive income.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="rounded-2xl bg-gray-900 px-6 py-12 sm:px-12 text-center">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-4">
              Ready to Build Your Perfect Notion Setup?
            </h2>
            <p className="text-gray-400 mb-6 max-w-xl mx-auto">
              Go Pro for unlimited AI tools, all templates, and Gumroad
              marketplace publishing. Start building your passive income today.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link href="/pricing">
                <Button
                  size="lg"
                  className="bg-orange-500 hover:bg-orange-600 text-white text-base px-8"
                >
                  Go Pro — $19.99/mo
                </Button>
              </Link>
              <Link href="/templates">
                <Button
                  variant="outline"
                  size="lg"
                  className="border-gray-600 text-gray-300 hover:bg-gray-800 text-base px-8"
                >
                  Browse Templates
                </Button>
              </Link>
            </div>
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
                q: "What is NotionBoost?",
                a: "NotionBoost is a platform for Notion users. We offer premium Notion templates, AI-powered tools built specifically for Notion workflows, and the ability to create and sell your own templates on Gumroad.",
              },
              {
                q: "Are the AI tools really free?",
                a: "Yes! You get 5 free AI tool uses per day with no sign-up required. Pro members get unlimited access to all tools plus our full template library.",
              },
              {
                q: "Can I sell my own Notion templates?",
                a: "Absolutely! Pro members can use our AI tools to create templates and publish them directly to Gumroad. We help you write descriptions, plan your template, and list it on the marketplace.",
              },
              {
                q: "How do the templates work?",
                a: "Each template is a Notion page you can duplicate to your own workspace. After purchase, you'll get a Notion link to duplicate. All databases, views, and formulas are included and ready to use.",
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
