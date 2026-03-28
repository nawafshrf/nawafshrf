import { createClient, SupabaseClient } from "@supabase/supabase-js";

let _supabase: SupabaseClient | null = null;
let _supabaseAdmin: SupabaseClient | null = null;

export function getSupabase(): SupabaseClient {
  if (!_supabase) {
    _supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL || "",
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ""
    );
  }
  return _supabase;
}

function getSupabaseAdmin(): SupabaseClient {
  if (!_supabaseAdmin) {
    _supabaseAdmin = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL || "",
      process.env.SUPABASE_SERVICE_ROLE_KEY || ""
    );
  }
  return _supabaseAdmin;
}

export { getSupabaseAdmin as supabaseAdmin };

export async function recordUsage(
  toolSlug: string,
  sessionId: string,
  userId?: string
) {
  const admin = getSupabaseAdmin();
  const { error } = await admin.from("usage").insert({
    tool_slug: toolSlug,
    session_id: sessionId,
    user_id: userId || null,
  });
  if (error) console.error("Error recording usage:", error);
}

export async function getUsageCount(
  sessionId: string,
  userId?: string
): Promise<number> {
  const admin = getSupabaseAdmin();
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  let query = admin
    .from("usage")
    .select("id", { count: "exact" })
    .gte("created_at", today.toISOString());

  if (userId) {
    query = query.eq("user_id", userId);
  } else {
    query = query.eq("session_id", sessionId);
  }

  const { count, error } = await query;
  if (error) {
    console.error("Error getting usage count:", error);
    return 0;
  }
  return count || 0;
}
