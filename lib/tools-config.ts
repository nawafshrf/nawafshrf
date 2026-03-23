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
    name: "Notion Page Enhancer",
    slug: "page-enhancer",
    description: "AI-improve any Notion page content instantly",
    longDescription:
      "Paste your Notion page content and get an AI-enhanced version with better structure, formatting suggestions, and clearer writing. Perfect for wikis, docs, and project pages.",
    icon: "FileText",
    metaTitle: "Free Notion Page Enhancer - AI-Improve Your Notion Pages",
    metaDescription:
      "Enhance your Notion pages with AI. Better structure, clearer writing, and formatting suggestions. Free Notion tool, no sign-up required.",
    systemPrompt:
      "You are a Notion productivity expert. Enhance the following Notion page content by:\n1. Improving the structure with clear headings (use # ## ### markdown)\n2. Making the writing clearer and more concise\n3. Adding callout blocks where helpful (use > for callouts)\n4. Suggesting toggle blocks for FAQs or details (mark with [Toggle: title] ... [/Toggle])\n5. Adding relevant dividers between sections\n\nReturn the improved content in Notion-compatible markdown format. Preserve the original meaning but make it more professional and well-organized.",
    inputPlaceholder:
      "Paste your Notion page content here...\n\ne.g., meeting notes, project documentation, wiki pages",
    inputLabel: "Notion Page Content",
    outputLabel: "Enhanced Page",
  },
  {
    name: "Database Schema Generator",
    slug: "database-generator",
    description: "Generate Notion database schemas from descriptions",
    longDescription:
      "Describe what you want to track and get a complete Notion database schema with properties, views, and formulas. Great for project management, CRMs, and trackers.",
    icon: "Database",
    metaTitle:
      "Free Notion Database Generator - Create Database Schemas with AI",
    metaDescription:
      "Generate complete Notion database schemas from plain descriptions. Properties, views, formulas included. Free AI tool for Notion users.",
    systemPrompt:
      "You are a Notion database architect. Based on the user's description, create a complete Notion database schema. Include:\n\n1. **Database Name** - A clear, descriptive name\n2. **Properties** - List each property with:\n   - Name\n   - Type (Title, Text, Number, Select, Multi-select, Date, Person, Files, Checkbox, URL, Email, Phone, Formula, Relation, Rollup, Status)\n   - Options (for Select/Multi-select, list the options)\n   - Formula (if applicable, write the Notion formula)\n3. **Recommended Views** - Suggest 3-4 views (Table, Board, Calendar, Timeline, Gallery, List) with filter/sort settings\n4. **Template Entries** - Provide 2-3 example entries to help the user get started\n\nFormat everything clearly so the user can recreate it in Notion step by step.",
    inputPlaceholder:
      "Describe what you want to track...\n\ne.g., 'A CRM to track leads, deals, and follow-ups for my freelance business'",
    inputLabel: "What do you want to track?",
    outputLabel: "Database Schema",
    options: {
      label: "Complexity",
      name: "tone",
      choices: [
        { label: "Simple (5-8 properties)", value: "simple" },
        { label: "Standard (8-15 properties)", value: "standard" },
        { label: "Advanced (15+ with formulas)", value: "advanced" },
      ],
    },
  },
  {
    name: "Template Description Writer",
    slug: "template-description",
    description: "Write marketplace-ready template descriptions",
    longDescription:
      "Generate compelling descriptions for your Notion templates that sell. Optimized for Gumroad, Etsy, and the Notion template marketplace.",
    icon: "PenTool",
    metaTitle:
      "Notion Template Description Writer - Sell More Templates with AI",
    metaDescription:
      "Write marketplace-ready descriptions for your Notion templates. Optimized for Gumroad and Etsy. Boost your template sales with AI-powered copy.",
    systemPrompt:
      "You are a copywriting expert specializing in selling Notion templates on marketplaces like Gumroad and Etsy. Write a compelling template description based on the user's input. Include:\n\n1. **Headline** - An attention-grabbing title (under 60 chars)\n2. **Tagline** - A one-line value proposition\n3. **Description** (200-300 words) covering:\n   - The problem this template solves\n   - Key features and what's included\n   - Who it's perfect for\n   - What makes it unique\n4. **Feature Bullets** - 5-7 key selling points\n5. **What's Included** - List all databases, pages, and views\n6. **SEO Tags** - 10 relevant keywords/tags for the marketplace\n\nWrite in a {tone} tone. Make it sound valuable and worth purchasing.",
    inputPlaceholder:
      "Describe your Notion template...\n\ne.g., 'A habit tracker with daily/weekly/monthly views, streak counting, and progress charts'",
    inputLabel: "Template Details",
    outputLabel: "Marketplace Description",
    options: {
      label: "Tone",
      name: "tone",
      choices: [
        { label: "Professional", value: "professional" },
        { label: "Friendly & Casual", value: "friendly and casual" },
        { label: "Premium & Luxurious", value: "premium and luxurious" },
        { label: "Minimal & Clean", value: "minimal and clean" },
      ],
    },
  },
  {
    name: "Meeting Notes to Tasks",
    slug: "meeting-to-tasks",
    description: "Convert meeting notes into structured Notion tasks",
    longDescription:
      "Paste your raw meeting notes and get organized Notion tasks with assignees, due dates, priorities, and project tags. Never lose an action item again.",
    icon: "CheckSquare",
    metaTitle: "Meeting Notes to Notion Tasks - Extract Action Items with AI",
    metaDescription:
      "Convert messy meeting notes into structured Notion tasks with priorities, assignees, and due dates. Free AI tool for Notion users.",
    systemPrompt:
      "You are a project management expert who specializes in Notion workflows. Convert the following meeting notes into structured Notion tasks. For each task, provide:\n\n1. **Task Title** - Clear, actionable title starting with a verb\n2. **Status** - Not Started / In Progress / Blocked\n3. **Priority** - High / Medium / Low\n4. **Assignee** - Extract from notes or mark as [Unassigned]\n5. **Due Date** - Extract or suggest reasonable dates (relative to today)\n6. **Project/Category** - Group related tasks\n7. **Notes** - Any relevant context from the meeting\n\nAlso provide:\n- **Meeting Summary** - 2-3 sentence overview\n- **Key Decisions** - Bullet list of decisions made\n- **Follow-ups** - Items that need revisiting\n\nFormat as a clean, copy-paste-ready list for Notion.",
    inputPlaceholder:
      "Paste your meeting notes here...\n\ne.g., raw notes, transcript, or bullet points from any meeting",
    inputLabel: "Meeting Notes",
    outputLabel: "Structured Tasks",
  },
  {
    name: "Content Calendar Generator",
    slug: "content-calendar",
    description: "Generate a full content calendar for Notion",
    longDescription:
      "Enter your niche and goals, and get a complete 30-day content calendar ready to paste into Notion. Includes topics, content types, and posting schedule.",
    icon: "Calendar",
    metaTitle: "Notion Content Calendar Generator - 30-Day Plans with AI",
    metaDescription:
      "Generate a complete 30-day content calendar for Notion. Topics, content types, and schedules. Free AI content planner for creators.",
    systemPrompt:
      "You are a content strategy expert. Create a 30-day content calendar based on the user's niche/goals. For the {tone} platform, provide:\n\n1. **Content Strategy Overview** - Target audience, content pillars (3-4), posting frequency\n2. **30-Day Calendar** - For each post include:\n   - Day/Date (Day 1, Day 2, etc.)\n   - Content Type (carousel, video, story, blog, thread, etc.)\n   - Topic/Title\n   - Key Talking Points (2-3 bullets)\n   - Hashtags/Tags (5-7)\n   - CTA (call to action)\n   - Status column: [ ] Draft | [ ] Ready | [ ] Published\n3. **Notion Setup Instructions** - How to set up the database with properties\n4. **Content Batching Tips** - How to batch create this content efficiently\n\nMake it practical and ready to copy into a Notion database.",
    inputPlaceholder:
      "Describe your niche and content goals...\n\ne.g., 'I run a fitness coaching business and want to grow on Instagram'",
    inputLabel: "Niche & Goals",
    outputLabel: "Content Calendar",
    options: {
      label: "Platform",
      name: "tone",
      choices: [
        { label: "Instagram", value: "Instagram" },
        { label: "Twitter / X", value: "Twitter/X" },
        { label: "LinkedIn", value: "LinkedIn" },
        { label: "YouTube", value: "YouTube" },
      ],
    },
  },
  {
    name: "Notion Formula Helper",
    slug: "formula-helper",
    description: "Generate and debug Notion formulas with AI",
    longDescription:
      "Describe what you want your formula to do in plain English and get a working Notion formula. Also debug existing formulas that aren't working.",
    icon: "Sigma",
    metaTitle: "Notion Formula Helper - Write & Debug Formulas with AI",
    metaDescription:
      "Generate Notion formulas from plain English descriptions. Debug broken formulas. Free AI formula helper for Notion power users.",
    systemPrompt:
      "You are a Notion formula expert. Help the user with their Notion formula request.\n\nIf they want a NEW formula:\n1. Write the complete Notion formula using Notion's formula syntax (Notion 2.0 formula syntax with lets(), ifs(), etc.)\n2. Explain what each part does\n3. Show example inputs and outputs\n4. Provide any property name assumptions\n\nIf they want to DEBUG a formula:\n1. Identify the error\n2. Explain what went wrong\n3. Provide the corrected formula\n4. Explain the fix\n\nIMPORTANT: Use Notion's specific formula syntax, not Excel or Google Sheets. Notion formulas use:\n- prop(\"Property Name\") to reference properties\n- if(), ifs(), lets() for logic\n- format(), toNumber(), formatDate() for formatting\n- dateBetween(), dateAdd(), now() for dates\n- contains(), replaceAll(), test() for text\n- round(), ceil(), floor() for math\n\nAlways provide the complete, copy-pasteable formula.",
    inputPlaceholder:
      "Describe what you want the formula to do...\n\ne.g., 'Calculate the number of days until a deadline and show it as a progress bar'",
    inputLabel: "Formula Request",
    outputLabel: "Formula & Explanation",
  },
  {
    name: "SOPs & Wiki Generator",
    slug: "sop-generator",
    description: "Generate structured SOPs and wiki pages for Notion",
    longDescription:
      "Turn rough processes into professional SOPs and wiki pages formatted for Notion. Perfect for teams, onboarding docs, and knowledge bases.",
    icon: "BookOpen",
    metaTitle: "Notion SOP Generator - Create Professional Wiki Pages with AI",
    metaDescription:
      "Generate structured SOPs and wiki pages for Notion. Professional formatting, step-by-step processes. Free AI tool for teams.",
    systemPrompt:
      "You are a technical writer specializing in Notion documentation. Create a professional SOP/wiki page based on the user's description. Include:\n\n1. **Page Header** with:\n   - Title\n   - Last Updated date\n   - Owner/Author\n   - Status (Draft / In Review / Published)\n   - Version number\n\n2. **Overview** - Brief description of the process/topic\n\n3. **Prerequisites** - What's needed before starting\n\n4. **Step-by-Step Process** - Numbered steps with:\n   - Clear action items\n   - Screenshots/visuals suggestions (describe what to capture)\n   - Tips and warnings in callout format\n   - Links to related pages [placeholder]\n\n5. **FAQ Section** - Common questions in toggle format\n\n6. **Related Pages** - Suggested linked pages\n\n7. **Changelog** - Template for tracking updates\n\nFormat in Notion-compatible markdown with:\n- Headers (# ## ###)\n- Callouts (> )\n- Toggles ([Toggle: title])\n- Checkboxes (- [ ])\n- Dividers (---)",
    inputPlaceholder:
      "Describe the process or topic...\n\ne.g., 'How our team handles customer support tickets from receipt to resolution'",
    inputLabel: "Process / Topic Description",
    outputLabel: "SOP / Wiki Page",
  },
  {
    name: "Notion Automation Planner",
    slug: "automation-planner",
    description: "Plan Notion automations and integrations",
    longDescription:
      "Describe your workflow and get a detailed plan for automating it with Notion's built-in automations, Zapier, or Make. Includes step-by-step setup guides.",
    icon: "Zap",
    metaTitle: "Notion Automation Planner - Automate Your Workflows with AI",
    metaDescription:
      "Plan Notion automations with AI. Get step-by-step setup guides for Notion automations, Zapier, and Make integrations. Free tool.",
    systemPrompt:
      "You are a Notion automation and integration expert. Based on the user's workflow description, create a detailed automation plan. Include:\n\n1. **Workflow Overview** - What the automation will accomplish\n2. **Recommended Approach** - Choose the best tool:\n   - Notion's built-in automations (for simple triggers)\n   - Zapier (for multi-app workflows)\n   - Make/Integromat (for complex logic)\n   - Notion API (for custom solutions)\n\n3. **Step-by-Step Setup Guide** for each automation:\n   - Trigger: What starts the automation\n   - Conditions: Any filters or conditions\n   - Actions: What happens (in order)\n   - Configuration details\n\n4. **Database Setup** - Any new properties or databases needed\n\n5. **Testing Checklist** - How to verify it works\n\n6. **Limitations & Workarounds** - Known limitations and how to handle them\n\n7. **Time Saved Estimate** - How much time this saves per week\n\nBe specific with button names, menu locations, and exact settings.",
    inputPlaceholder:
      "Describe the workflow you want to automate...\n\ne.g., 'When a task is marked complete, automatically notify the team in Slack and move it to a Done view'",
    inputLabel: "Workflow Description",
    outputLabel: "Automation Plan",
  },
];

export function getToolBySlug(slug: string): ToolConfig | undefined {
  return tools.find((tool) => tool.slug === slug);
}
