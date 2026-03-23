import Link from "next/link";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { NotionTemplate } from "@/lib/templates-config";
import { categoryLabels, categoryColors } from "@/lib/templates-config";

export default function TemplateCard({ template }: { template: NotionTemplate }) {
  return (
    <Link href={`/templates/${template.slug}`}>
      <Card className="group h-full transition-all hover:shadow-md hover:border-orange-200 hover:-translate-y-0.5">
        <CardHeader>
          <div className="flex items-start justify-between mb-2">
            <span
              className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                categoryColors[template.category]
              }`}
            >
              {categoryLabels[template.category]}
            </span>
            <div className="flex items-center gap-1.5">
              {template.isNew && <Badge variant="success">New</Badge>}
            </div>
          </div>
          <CardTitle className="text-lg">{template.name}</CardTitle>
          <CardDescription>{template.description}</CardDescription>
          <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-100">
            <span className="text-lg font-bold text-gray-900">
              ${template.price}
            </span>
            <span className="text-xs text-gray-500">
              {template.includes[0]}
            </span>
          </div>
        </CardHeader>
      </Card>
    </Link>
  );
}
