"use client";

import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gray-900 text-white font-bold text-sm">
            N
          </div>
          <span className="text-lg font-bold text-gray-900">
            Notion<span className="text-orange-500">Boost</span>
          </span>
        </Link>

        <nav className="hidden md:flex items-center gap-6">
          <Link
            href="/templates"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            Templates
          </Link>
          <Link
            href="/#tools"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            AI Tools
          </Link>
          <Link
            href="/publish"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            Sell Templates
          </Link>
          <Link
            href="/pricing"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            Pricing
          </Link>
        </nav>

        <div className="hidden md:flex items-center gap-3">
          <Link href="/pricing">
            <Button size="sm">Go Pro</Button>
          </Link>
        </div>

        <button
          className="md:hidden p-2"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          aria-label="Toggle menu"
        >
          <svg
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
          >
            {mobileMenuOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            )}
          </svg>
        </button>
      </div>

      {mobileMenuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white px-4 py-4 space-y-3">
          <Link
            href="/templates"
            className="block text-sm text-gray-600 hover:text-gray-900"
            onClick={() => setMobileMenuOpen(false)}
          >
            Templates
          </Link>
          <Link
            href="/#tools"
            className="block text-sm text-gray-600 hover:text-gray-900"
            onClick={() => setMobileMenuOpen(false)}
          >
            AI Tools
          </Link>
          <Link
            href="/publish"
            className="block text-sm text-gray-600 hover:text-gray-900"
            onClick={() => setMobileMenuOpen(false)}
          >
            Sell Templates
          </Link>
          <Link
            href="/pricing"
            className="block text-sm text-gray-600 hover:text-gray-900"
            onClick={() => setMobileMenuOpen(false)}
          >
            Pricing
          </Link>
          <Link href="/pricing" onClick={() => setMobileMenuOpen(false)}>
            <Button size="sm" className="w-full">
              Go Pro
            </Button>
          </Link>
        </div>
      )}
    </header>
  );
}
