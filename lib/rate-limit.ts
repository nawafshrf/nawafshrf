import { cookies } from "next/headers";
import { getUsageCount } from "./supabase";

const FREE_DAILY_LIMIT = 5;
const REGISTERED_DAILY_LIMIT = 10;

export async function getSessionId(): Promise<string> {
  const cookieStore = await cookies();
  let sessionId = cookieStore.get("smarttools_session")?.value;

  if (!sessionId) {
    sessionId = crypto.randomUUID();
  }

  return sessionId;
}

export async function checkRateLimit(
  sessionId: string,
  userId?: string,
  subscriptionStatus?: string
): Promise<{
  allowed: boolean;
  remaining: number;
  limit: number;
}> {
  if (subscriptionStatus === "pro") {
    return { allowed: true, remaining: Infinity, limit: Infinity };
  }

  const limit = userId ? REGISTERED_DAILY_LIMIT : FREE_DAILY_LIMIT;
  const usageCount = await getUsageCount(sessionId, userId);
  const remaining = Math.max(0, limit - usageCount);

  return {
    allowed: remaining > 0,
    remaining,
    limit,
  };
}
