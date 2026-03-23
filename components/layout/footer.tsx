import Link from "next/link";
import { tools } from "@/lib/tools-config";

export default function Footer() {
  return (
    <footer className="border-t border-gray-200 bg-gray-50">
      <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white font-bold text-sm">
                ST
              </div>
              <span className="text-lg font-bold text-gray-900">
                SmartTools<span className="text-blue-600">AI</span>
              </span>
            </div>
            <p className="text-sm text-gray-500">
              Free AI-powered tools for writers, developers, and marketers. No
              sign-up required.
            </p>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-900 mb-3">Tools</h3>
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
              More Tools
            </h3>
            <ul className="space-y-2">
              {tools.slice(4).map((tool) => (
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
            </ul>
          </div>
        </div>

        <div className="mt-8 border-t border-gray-200 pt-8 text-center">
          <p className="text-sm text-gray-400">
            &copy; {new Date().getFullYear()} SmartTools AI. All rights
            reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
