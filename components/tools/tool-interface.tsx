"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ToolConfig } from "@/lib/tools-config";

export default function ToolInterface({ tool }: { tool: ToolConfig }) {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [selectedOption, setSelectedOption] = useState(
    tool.options?.choices[0]?.value || ""
  );
  const [usageInfo, setUsageInfo] = useState<{
    remaining: number;
    limit: number;
  } | null>(null);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setError("");
    setOutput("");

    try {
      const body: Record<string, string> = { input: input.trim() };
      if (tool.options) {
        body[tool.options.name] = selectedOption;
      }

      const res = await fetch(`/api/tools/${tool.slug}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (!res.ok) {
        if (res.status === 429) {
          setError(
            "Daily free limit reached. Upgrade to Pro for unlimited access!"
          );
          setUsageInfo({ remaining: 0, limit: data.limit || 5 });
        } else {
          setError(data.error || "Something went wrong. Please try again.");
        }
        return;
      }

      setOutput(data.result);
      if (data.remaining !== undefined) {
        setUsageInfo({ remaining: data.remaining, limit: data.limit });
      }
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      {/* Input Panel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">{tool.inputLabel}</CardTitle>
            {usageInfo && (
              <Badge variant={usageInfo.remaining > 0 ? "secondary" : "destructive"}>
                {usageInfo.remaining}/{usageInfo.limit} uses left today
              </Badge>
            )}
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          {tool.options && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {tool.options.label}
              </label>
              <select
                value={selectedOption}
                onChange={(e) => setSelectedOption(e.target.value)}
                className="w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500"
              >
                {tool.options.choices.map((choice) => (
                  <option key={choice.value} value={choice.value}>
                    {choice.label}
                  </option>
                ))}
              </select>
            </div>
          )}

          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={tool.inputPlaceholder}
            rows={10}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm placeholder:text-gray-400 focus:border-orange-500 focus:outline-none focus:ring-1 focus:ring-orange-500 resize-none"
          />

          <Button
            onClick={handleSubmit}
            disabled={loading || !input.trim()}
            className="w-full"
            size="lg"
          >
            {loading ? (
              <span className="flex items-center gap-2">
                <svg
                  className="animate-spin h-4 w-4"
                  viewBox="0 0 24 24"
                  fill="none"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  />
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                Processing...
              </span>
            ) : (
              `Generate ${tool.outputLabel}`
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Output Panel */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">{tool.outputLabel}</CardTitle>
            {output && (
              <Button variant="outline" size="sm" onClick={handleCopy}>
                {copied ? "Copied!" : "Copy"}
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          {error ? (
            <div className="rounded-lg bg-red-50 border border-red-200 p-4">
              <p className="text-sm text-red-700">{error}</p>
              {error.includes("Upgrade") && (
                <a
                  href="/pricing"
                  className="mt-2 inline-block text-sm font-medium text-orange-600 hover:text-orange-700"
                >
                  View Pro plans &rarr;
                </a>
              )}
            </div>
          ) : output ? (
            <div className="rounded-lg bg-gray-50 border border-gray-200 p-4 min-h-[250px]">
              <pre className="whitespace-pre-wrap text-sm text-gray-800 font-sans leading-relaxed">
                {output}
              </pre>
            </div>
          ) : (
            <div className="flex items-center justify-center min-h-[250px] text-gray-400 text-sm">
              Your result will appear here...
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
