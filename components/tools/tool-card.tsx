import Link from "next/link";
import {
  FileText,
  Database,
  PenTool,
  CheckSquare,
  Calendar,
  BookOpen,
  Zap,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { ToolConfig } from "@/lib/tools-config";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  FileText,
  Database,
  PenTool,
  CheckSquare,
  Calendar,
  Sigma: FileText,
  BookOpen,
  Zap,
};

export default function ToolCard({ tool }: { tool: ToolConfig }) {
  const Icon = iconMap[tool.icon] || FileText;

  return (
    <Link href={`/tools/${tool.slug}`}>
      <Card className="group h-full transition-all hover:shadow-md hover:border-orange-200 hover:-translate-y-0.5">
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-50 text-orange-600 group-hover:bg-orange-100 transition-colors">
              <Icon className="h-5 w-5" />
            </div>
            <Badge variant="success">Free</Badge>
          </div>
          <CardTitle className="mt-3 text-lg">{tool.name}</CardTitle>
          <CardDescription>{tool.description}</CardDescription>
        </CardHeader>
      </Card>
    </Link>
  );
}
