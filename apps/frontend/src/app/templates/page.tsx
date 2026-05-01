"use client";

import { useState } from "react";
import Link from "next/link";
import { useTemplates, useCreateTemplate } from "@/hooks/useTemplates";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PlusIcon, FileTextIcon, TableIcon } from "lucide-react";

export default function TemplatesPage() {
  const { data: templates = [], isLoading } = useTemplates();
  const createTemplate = useCreateTemplate();
  const [creating, setCreating] = useState(false);

  async function handleCreate(format: "docx" | "xlsx") {
    setCreating(true);
    await createTemplate.mutateAsync({
      name: `Untitled ${format.toUpperCase()} Template`,
      output_format: format,
    });
    setCreating(false);
  }

  if (isLoading) return <div className="p-8">Loading templates…</div>;

  return (
    <div className="p-8 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Templates</h1>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => handleCreate("docx")} disabled={creating}>
            <FileTextIcon className="w-4 h-4 mr-2" />
            New Word
          </Button>
          <Button onClick={() => handleCreate("xlsx")} disabled={creating}>
            <TableIcon className="w-4 h-4 mr-2" />
            New Excel
          </Button>
        </div>
      </div>

      {templates.length === 0 ? (
        <div className="text-center py-16 text-muted-foreground">
          No templates yet. Create your first one above.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((t) => (
            <Link key={t.id} href={`/templates/${t.id}`}>
              <div className="border rounded-lg p-4 hover:border-primary transition-colors cursor-pointer">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-medium truncate">{t.name}</span>
                  <Badge variant={t.output_format === "docx" ? "secondary" : "default"}>
                    {t.output_format.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground">
                  {t.components?.length ?? 0} component{(t.components?.length ?? 0) !== 1 ? "s" : ""}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
