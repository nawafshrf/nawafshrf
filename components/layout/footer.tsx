import Link from "next/link";
import { tools } from "@/lib/tools-config";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-gray-50">
      <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gray-900 text-white font-bold text-sm">
                N
              </div>
              <span className="text-lg font-bold text-gray-900">
                Notion<span className="text-orange-500">Boost</span>
              </span>
            </div>
            <p className="text-sm text-gray-500">
              AI-powered Notion templates and tools. Build, buy, and sell
              Notion templates.
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Templates
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/templates"
                  className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
                >
                  All Templates
                </Link>
              </li>
              <li>
                <Link
                  href="/publish"
                  className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
                >
                  Sell on Gumroad
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              AI Tools
            </h3>
            <ul className="space-y-2">
              {tools.slice(0, 4).map((tool) => (
                <li key={tool.slug}>
                  <Link
                    href={`/tools/${tool.slug}`}
                    className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
                  >
                    {tool.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Company
            </h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/pricing"
                  className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
                >
                  Pricing
                </Link>
              </li>
              <li>
                <Link
                  href="/dashboard"
                  className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
                >
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-200 pt-8 text-center">
          <p className="text-sm text-gray-400">
            &copy; {new Date().getFullYear()} NotionBoost. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
