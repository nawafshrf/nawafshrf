export interface NotionTemplate {
  id: string;
  name: string;
  slug: string;
  description: string;
  longDescription: string;
  category: TemplateCategory;
  price: number;
  icon: string;
  features: string[];
  includes: string[];
  previewImages: string[];
  notionUrl?: string;
  isFeatured: boolean;
  isNew: boolean;
}

export type TemplateCategory =
  | "productivity"
  | "business"
  | "personal"
  | "content"
  | "finance"
  | "education";

export const categoryLabels: Record<TemplateCategory, string> = {
  productivity: "Productivity",
  business: "Business",
  personal: "Personal",
  content: "Content Creation",
  finance: "Finance",
  education: "Education",
};

export const categoryColors: Record<TemplateCategory, string> = {
  productivity: "bg-blue-100 text-blue-700",
  business: "bg-purple-100 text-purple-700",
  personal: "bg-green-100 text-green-700",
  content: "bg-orange-100 text-orange-700",
  finance: "bg-emerald-100 text-emerald-700",
  education: "bg-pink-100 text-pink-700",
};

export const templates: NotionTemplate[] = [
  {
    id: "1",
    name: "Ultimate Freelancer Hub",
    slug: "freelancer-hub",
    description:
      "All-in-one Notion workspace for freelancers: clients, projects, invoices, and finances.",
    longDescription:
      "Stop juggling multiple tools. The Ultimate Freelancer Hub brings your entire freelance business into one Notion workspace. Track clients, manage projects, send invoices, and monitor your finances — all from a single dashboard. Includes automated formulas for revenue tracking, project timelines, and client health scores.",
    category: "business",
    price: 29,
    icon: "Briefcase",
    features: [
      "Client CRM with health scores",
      "Project tracker with Kanban & timeline views",
      "Invoice generator with auto-calculations",
      "Revenue dashboard with monthly/yearly views",
      "Time tracking log",
      "Contract & proposal templates",
    ],
    includes: [
      "5 linked databases",
      "12 custom views",
      "3 dashboard pages",
      "Notion formulas included",
      "Setup guide page",
    ],
    previewImages: [],
    isFeatured: true,
    isNew: false,
  },
  {
    id: "2",
    name: "Content Creator OS",
    slug: "content-creator-os",
    description:
      "Plan, create, and schedule content across all platforms from one Notion workspace.",
    longDescription:
      "The Content Creator OS is your all-in-one content management system built in Notion. Plan your content calendar, track ideas, manage your pipeline from draft to published, and analyze performance — all in one beautiful workspace. Works for YouTube, Instagram, TikTok, Twitter, LinkedIn, and blogs.",
    category: "content",
    price: 24,
    icon: "Video",
    features: [
      "Multi-platform content calendar",
      "Idea bank with scoring system",
      "Content pipeline (Idea → Draft → Review → Published)",
      "Analytics tracker per platform",
      "Hashtag & caption library",
      "Collaboration workspace for teams",
    ],
    includes: [
      "4 linked databases",
      "8 custom views",
      "2 dashboard pages",
      "Content templates for each platform",
      "Video script template",
    ],
    previewImages: [],
    isFeatured: true,
    isNew: true,
  },
  {
    id: "3",
    name: "Student Life Planner",
    slug: "student-life-planner",
    description:
      "Academic planner with assignment tracker, study scheduler, and GPA calculator.",
    longDescription:
      "Designed by students, for students. The Student Life Planner keeps your academics, assignments, study sessions, and goals all in one place. Automatic GPA calculation, assignment deadlines with reminders, and a Pomodoro-style study tracker to keep you focused.",
    category: "education",
    price: 14,
    icon: "GraduationCap",
    features: [
      "Semester & course manager",
      "Assignment tracker with deadlines",
      "GPA calculator with auto-formulas",
      "Study session logger",
      "Exam preparation planner",
      "Weekly & daily schedule views",
    ],
    includes: [
      "3 linked databases",
      "6 custom views",
      "GPA formula included",
      "Weekly planner template",
      "Exam prep checklist",
    ],
    previewImages: [],
    isFeatured: false,
    isNew: true,
  },
  {
    id: "4",
    name: "Personal Finance Tracker",
    slug: "finance-tracker",
    description:
      "Track income, expenses, budgets, and savings goals with automated calculations.",
    longDescription:
      "Take control of your money with this comprehensive Notion finance tracker. Log every transaction, set budgets by category, track savings goals with progress bars, and get monthly financial reports — all powered by Notion formulas. No spreadsheets needed.",
    category: "finance",
    price: 19,
    icon: "DollarSign",
    features: [
      "Transaction log with categories",
      "Monthly budget tracker",
      "Savings goals with progress bars",
      "Expense breakdown by category",
      "Net worth tracker",
      "Subscription manager",
    ],
    includes: [
      "4 linked databases",
      "10 custom views",
      "Budget dashboard",
      "All formulas included",
      "Monthly report template",
    ],
    previewImages: [],
    isFeatured: true,
    isNew: false,
  },
  {
    id: "5",
    name: "Habit Tracker Pro",
    slug: "habit-tracker",
    description:
      "Build and track habits with streaks, analytics, and daily/weekly/monthly views.",
    longDescription:
      "Build lasting habits with the most comprehensive habit tracker for Notion. Track daily habits with visual streaks, analyze your consistency over weeks and months, and celebrate milestones. Includes pre-built habit templates for health, productivity, learning, and mindfulness.",
    category: "personal",
    price: 12,
    icon: "Target",
    features: [
      "Daily habit check-in",
      "Streak counter with formulas",
      "Weekly & monthly consistency views",
      "Habit categories and tagging",
      "Progress analytics",
      "Pre-built habit templates",
    ],
    includes: [
      "2 linked databases",
      "5 custom views",
      "Streak formulas",
      "30 pre-built habits",
      "Daily journal template",
    ],
    previewImages: [],
    isFeatured: false,
    isNew: false,
  },
  {
    id: "6",
    name: "Startup Launch Pad",
    slug: "startup-launchpad",
    description:
      "Everything to launch your startup: roadmap, OKRs, investor tracker, and team wiki.",
    longDescription:
      "From idea to launch, the Startup Launch Pad gives you every tool you need to build your startup in Notion. Product roadmap, OKR tracking, investor CRM, team wiki, meeting notes, and launch checklists — all connected and ready to go from day one.",
    category: "business",
    price: 34,
    icon: "Rocket",
    features: [
      "Product roadmap with timeline view",
      "OKR tracker (company & team level)",
      "Investor CRM with pipeline",
      "Team wiki & onboarding docs",
      "Sprint planning board",
      "Launch checklist with milestones",
    ],
    includes: [
      "8 linked databases",
      "15 custom views",
      "4 dashboard pages",
      "Pitch deck outline",
      "Team onboarding template",
    ],
    previewImages: [],
    isFeatured: true,
    isNew: true,
  },
  {
    id: "7",
    name: "Job Hunt Command Center",
    slug: "job-hunt-tracker",
    description:
      "Track applications, prep for interviews, and manage your entire job search.",
    longDescription:
      "Land your dream job with the most organized job search system in Notion. Track every application, prepare for interviews with question banks, manage networking contacts, and never miss a follow-up. Includes salary comparison tools and offer evaluation frameworks.",
    category: "productivity",
    price: 16,
    icon: "Compass",
    features: [
      "Application tracker with Kanban view",
      "Interview prep question bank",
      "Networking contact manager",
      "Follow-up reminder system",
      "Salary comparison tool",
      "Offer evaluation framework",
    ],
    includes: [
      "3 linked databases",
      "7 custom views",
      "50+ interview questions",
      "Follow-up email templates",
      "Salary negotiation guide",
    ],
    previewImages: [],
    isFeatured: false,
    isNew: false,
  },
  {
    id: "8",
    name: "Second Brain System",
    slug: "second-brain",
    description:
      "PARA method knowledge management system for capturing, organizing, and retrieving information.",
    longDescription:
      "Build your second brain in Notion using the proven PARA method (Projects, Areas, Resources, Archives). Capture ideas, organize knowledge, and retrieve information instantly. Includes web clipper integration, reading list, and a connected note-taking system inspired by Zettelkasten.",
    category: "productivity",
    price: 22,
    icon: "Brain",
    features: [
      "PARA method organization",
      "Quick capture inbox",
      "Connected notes (backlinks)",
      "Reading list with highlights",
      "Weekly review template",
      "Knowledge base with search",
    ],
    includes: [
      "5 linked databases",
      "8 custom views",
      "PARA folder structure",
      "Weekly review template",
      "Web clipper setup guide",
    ],
    previewImages: [],
    isFeatured: true,
    isNew: false,
  },
];

export function getTemplateBySlug(
  slug: string
): NotionTemplate | undefined {
  return templates.find((t) => t.slug === slug);
}

export function getTemplatesByCategory(
  category: TemplateCategory
): NotionTemplate[] {
  return templates.filter((t) => t.category === category);
}

export function getFeaturedTemplates(): NotionTemplate[] {
  return templates.filter((t) => t.isFeatured);
}
