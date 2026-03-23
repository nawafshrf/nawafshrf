import { NextResponse } from "next/server";
import { createPortalSession } from "@/lib/stripe";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";

export async function POST() {
  try {
    const session = await getServerSession(authOptions);

    if (!session?.user?.email) {
      return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
    }

    const stripeCustomerId = (session.user as Record<string, unknown>)
      .stripeCustomerId as string;

    if (!stripeCustomerId) {
      return NextResponse.json(
        { error: "No active subscription" },
        { status: 400 }
      );
    }

    const portalSession = await createPortalSession(stripeCustomerId);

    if (portalSession.url) {
      return NextResponse.redirect(portalSession.url);
    }

    return NextResponse.json(
      { error: "Could not create portal session" },
      { status: 500 }
    );
  } catch (error) {
    console.error("Portal error:", error);
    return NextResponse.json(
      { error: "Something went wrong" },
      { status: 500 }
    );
  }
}
