import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { getToolBySlug } from "@/lib/tools-config";
import { generateAIResponse } from "@/lib/openai";
import { getSessionId, checkRateLimit } from "@/lib/rate-limit";
import { recordUsage } from "@/lib/supabase";

const inputSchema = z.object({
  input: z.string().min(1).max(10000),
  tone: z.string().optional(),
});

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ tool: string }> }
) {
  try {
    const { tool: toolSlug } = await params;
    const tool = getToolBySlug(toolSlug);

    if (!tool) {
      return NextResponse.json({ error: "Tool not found" }, { status: 404 });
    }

    const body = await request.json();
    const parsed = inputSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json(
        { error: "Invalid input. Please provide text to process." },
        { status: 400 }
      );
    }

    const sessionId = await getSessionId();
    const rateLimit = await checkRateLimit(sessionId);

    if (!rateLimit.allowed) {
      return NextResponse.json(
        {
          error: "Daily free limit reached. Upgrade to Pro for unlimited access.",
          limit: rateLimit.limit,
          remaining: 0,
        },
        { status: 429 }
      );
    }

    const options: Record<string, string> = {};
    if (tool.options && body[tool.options.name]) {
      options[tool.options.name] = body[tool.options.name];
    }

    const result = await generateAIResponse(
      tool.systemPrompt,
      parsed.data.input,
      Object.keys(options).length > 0 ? options : undefined
    );

    await recordUsage(toolSlug, sessionId);

    const newRemaining = rateLimit.remaining - 1;

    const response = NextResponse.json({
      result,
      remaining: newRemaining,
      limit: rateLimit.limit,
    });

    // Set session cookie if not present
    response.cookies.set("smarttools_session", sessionId, {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 365, // 1 year
      path: "/",
    });

    return response;
  } catch (error) {
    console.error("Tool API error:", error);
    return NextResponse.json(
      { error: "Something went wrong. Please try again." },
      { status: 500 }
    );
  }
}
