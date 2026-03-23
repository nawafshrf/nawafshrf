import { NextResponse } from "next/server";
import { createCheckoutSession } from "@/lib/stripe";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";

export async function POST() {
  try {
    const session = await getServerSession(authOptions);

    if (!session?.user?.email) {
      // Redirect to sign-in if not authenticated
      return NextResponse.redirect(
        new URL("/api/auth/signin?callbackUrl=/pricing", process.env.NEXTAUTH_URL || "http://localhost:3000")
      );
    }

    const userId = (session.user as Record<string, unknown>).id as string;
    const checkoutSession = await createCheckoutSession(
      session.user.email,
      userId
    );

    if (checkoutSession.url) {
      return NextResponse.redirect(checkoutSession.url);
    }

    return NextResponse.json(
      { error: "Could not create checkout session" },
      { status: 500 }
    );
  } catch (error) {
    console.error("Checkout error:", error);
    return NextResponse.json(
      { error: "Something went wrong" },
      { status: 500 }
    );
  }
}
