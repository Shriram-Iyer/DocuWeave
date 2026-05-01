"use client";

import { useTemplate } from "@/hooks/useTemplates";

interface Props {
  templateId: string;
}

export function CellTokenHelper({ templateId }: Props) {
  const { data: template } = useTemplate(templateId);
  const excelConfig = template?.excel_config as Record<string, unknown> | null | undefined;
  const tokens: string[] = (excelConfig?.available_fields as string[] | undefined) ?? [];

  return (
    <div className="bg-white border rounded p-3 text-sm">
      <p className="font-semibold mb-2 text-xs text-muted-foreground uppercase tracking-wide">
        Token Reference
      </p>
      <p className="text-xs text-muted-foreground mb-3">
        Use <code className="bg-muted px-1 rounded">{"{{field_name}}"}</code> in cells to insert dynamic values.
      </p>

      {tokens.length > 0 ? (
        <div className="flex flex-col gap-1">
          {tokens.map((token) => (
            <code
              key={token}
              className="text-xs bg-indigo-50 text-indigo-700 px-2 py-1 rounded cursor-pointer hover:bg-indigo-100"
              title="Click to copy"
              onClick={() => navigator.clipboard.writeText(`{{${token}}}`)}
            >
              {`{{${token}}}`}
            </code>
          ))}
        </div>
      ) : (
        <p className="text-xs text-muted-foreground">
          Configure a data source and link config to see available field tokens.
        </p>
      )}

      <div className="mt-4 space-y-1">
        <p className="text-xs font-semibold text-muted-foreground">Repeat blocks:</p>
        <code className="text-xs bg-muted px-2 py-1 rounded block">
          {"{{#repeat table_name}}"}
        </code>
        <code className="text-xs bg-muted px-2 py-1 rounded block">
          {"{{/repeat}}"}
        </code>
      </div>
    </div>
  );
}
