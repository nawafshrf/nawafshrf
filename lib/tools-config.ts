export interface ToolOption {
  label: string;
  value: string;
}

export interface ToolConfig {
  name: string;
  slug: string;
  description: string;
  longDescription: string;
  icon: string;
  metaTitle: string;
  metaDescription: string;
  systemPrompt: string;
  inputPlaceholder: string;
  inputLabel: string;
  outputLabel: string;
  options?: {
    label: string;
    name: string;
    choices: ToolOption[];
  };
}

export const tools: ToolConfig[] = [
  {
    name: "Text Summarizer",
    slug: "summarizer",
    description: "Summarize long text into concise key points",
    longDescription: "Paste any article, essay, or document and get a clear, concise summary in seconds. Perfect for students, researchers, and busy professionals.",
    icon: "FileText",
    metaTitle: "Free AI Text Summarizer - Summarize Any Text Instantly",
    metaDescription: "Summarize articles, essays, and documents instantly with our free AI text summarizer. No sign-up required. Get concise summaries in one click.",
    systemPrompt: "You are a text summarization expert. Summarize the following text concisely while preserving all key points and main ideas. Use clear, simple language. Format with bullet points for key takeaways.",
    inputPlaceholder: "Paste your text here to summarize...",
    inputLabel: "Text to Summarize",
    outputLabel: "Summary",
  },
  {
    name: "Paraphraser",
    slug: "paraphraser",
    description: "Rewrite text in different tones and styles",
    longDescription: "Rewrite any text in your preferred tone — formal, casual, academic, or simple. Great for essays, emails, and content creation.",
    icon: "RefreshCw",
    metaTitle: "Free AI Paraphrasing Tool - Rewrite Text in Any Tone",
    metaDescription: "Paraphrase and rewrite text instantly in formal, casual, academic, or simple tones. Free AI paraphraser with no sign-up required.",
    systemPrompt: "You are a paraphrasing expert. Rewrite the following text in a {tone} tone. Keep the same meaning but use different words and sentence structures. The output should feel natural and well-written.",
    inputPlaceholder: "Paste your text here to paraphrase...",
    inputLabel: "Text to Paraphrase",
    outputLabel: "Paraphrased Text",
    options: {
      label: "Tone",
      name: "tone",
      choices: [
        { label: "Formal", value: "formal" },
        { label: "Casual", value: "casual" },
        { label: "Academic", value: "academic" },
        { label: "Simple", value: "simple" },
      ],
    },
  },
  {
    name: "Grammar Checker",
    slug: "grammar-checker",
    description: "Fix grammar, spelling, and punctuation errors",
    longDescription: "Instantly fix grammar, spelling, and punctuation mistakes. Get clear explanations for each correction to improve your writing.",
    icon: "CheckCircle",
    metaTitle: "Free AI Grammar Checker - Fix Writing Errors Instantly",
    metaDescription: "Check and fix grammar, spelling, and punctuation errors instantly. Free AI grammar checker with explanations. No sign-up needed.",
    systemPrompt: "You are a grammar and writing expert. Check the following text for grammar, spelling, and punctuation errors. Return the corrected text first, then list each correction you made with a brief explanation. Format corrections as a numbered list.",
    inputPlaceholder: "Paste your text here to check grammar...",
    inputLabel: "Text to Check",
    outputLabel: "Corrected Text",
  },
  {
    name: "Code Explainer",
    slug: "code-explainer",
    description: "Get plain English explanations of any code",
    longDescription: "Paste any code snippet and get a clear, beginner-friendly explanation of what it does. Supports all major programming languages.",
    icon: "Code",
    metaTitle: "Free AI Code Explainer - Understand Any Code Instantly",
    metaDescription: "Get plain English explanations of any code snippet. Supports Python, JavaScript, Java, and more. Free AI code explainer, no sign-up required.",
    systemPrompt: "You are a programming teacher. Explain the following code in plain English that a beginner could understand. Break down what each part does, the overall purpose, and any important concepts used. Be thorough but clear.",
    inputPlaceholder: "Paste your code here...",
    inputLabel: "Code to Explain",
    outputLabel: "Explanation",
  },
  {
    name: "Email Writer",
    slug: "email-writer",
    description: "Generate professional emails from bullet points",
    longDescription: "Turn bullet points or rough notes into polished, professional emails. Choose your tone and get a ready-to-send email in seconds.",
    icon: "Mail",
    metaTitle: "Free AI Email Writer - Generate Professional Emails Instantly",
    metaDescription: "Turn bullet points into professional emails instantly. Choose formal, friendly, or persuasive tone. Free AI email writer, no sign-up needed.",
    systemPrompt: "You are a professional email writing expert. Based on the following bullet points/notes, write a polished, professional email in a {tone} tone. Include an appropriate subject line, greeting, body, and sign-off. The email should be clear, concise, and ready to send.",
    inputPlaceholder: "Enter your bullet points or notes...\n\n- Meeting rescheduled to Friday\n- Need budget approval\n- Deadline is next week",
    inputLabel: "Your Notes / Bullet Points",
    outputLabel: "Generated Email",
    options: {
      label: "Tone",
      name: "tone",
      choices: [
        { label: "Formal", value: "formal" },
        { label: "Friendly", value: "friendly" },
        { label: "Persuasive", value: "persuasive" },
        { label: "Concise", value: "concise" },
      ],
    },
  },
  {
    name: "Blog Outline Generator",
    slug: "blog-outline",
    description: "Generate structured blog post outlines",
    longDescription: "Enter a topic and get a structured blog post outline with headings, subheadings, and key points. Perfect for content creators and marketers.",
    icon: "List",
    metaTitle: "Free AI Blog Outline Generator - Create Blog Structure Instantly",
    metaDescription: "Generate structured blog post outlines with headings and key points instantly. Free AI blog outline generator, no sign-up required.",
    systemPrompt: "You are a content strategist and SEO expert. Create a detailed blog post outline for the following topic. Include: a compelling title, introduction hook, 4-6 main sections with H2 headings, 2-3 sub-points under each section, a conclusion section, and a suggested call-to-action. Make it SEO-friendly and engaging.",
    inputPlaceholder: "Enter your blog topic...\n\ne.g., 'How to start a freelance business in 2024'",
    inputLabel: "Blog Topic",
    outputLabel: "Blog Outline",
  },
  {
    name: "Meta Description Generator",
    slug: "meta-description",
    description: "Create SEO-optimized meta descriptions",
    longDescription: "Generate compelling, SEO-optimized meta descriptions for your web pages. Boost click-through rates from search results.",
    icon: "Search",
    metaTitle: "Free AI Meta Description Generator - SEO Meta Tags Instantly",
    metaDescription: "Generate SEO-optimized meta descriptions for your web pages. Boost CTR from search results. Free AI tool, no sign-up needed.",
    systemPrompt: "You are an SEO expert. Generate 3 compelling meta descriptions for a web page about the following content. Each description should be: 150-160 characters, include relevant keywords naturally, have a clear call-to-action, and be engaging enough to improve click-through rates. Number each option.",
    inputPlaceholder: "Describe your page content or paste your page text...",
    inputLabel: "Page Content / Description",
    outputLabel: "Meta Descriptions",
  },
  {
    name: "Hashtag Generator",
    slug: "hashtag-generator",
    description: "Generate relevant hashtags for social media",
    longDescription: "Generate trending, relevant hashtags for your social media posts. Boost reach and engagement on Instagram, Twitter, LinkedIn, and TikTok.",
    icon: "Hash",
    metaTitle: "Free AI Hashtag Generator - Social Media Hashtags Instantly",
    metaDescription: "Generate relevant hashtags for Instagram, Twitter, LinkedIn, and TikTok. Boost your social media reach. Free AI hashtag generator.",
    systemPrompt: "You are a social media marketing expert. Generate a set of 20-30 relevant hashtags for the following content/topic. Organize them into 3 categories: 1) High-volume (popular, broad hashtags), 2) Medium-volume (niche-specific), 3) Low-competition (very specific, long-tail). Format each category clearly.",
    inputPlaceholder: "Describe your post or enter your topic...\n\ne.g., 'Healthy meal prep ideas for busy professionals'",
    inputLabel: "Post Content / Topic",
    outputLabel: "Generated Hashtags",
  },
];

export function getToolBySlug(slug: string): ToolConfig | undefined {
  return tools.find((tool) => tool.slug === slug);
}
