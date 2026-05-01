"use client";

import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { useTemplate, useUpdateTemplate } from "@/hooks/useTemplates";
import { CellTokenHelper } from "./CellTokenHelper";

// Fortune Sheet has no SSR support — load client-only
const Workbook = dynamic(
  () => import("@fortune-sheet/react").then((m) => m.Workbook),
  { ssr: false, loading: () => <div className="p-8">Loading spreadsheet editor…</div> }
);

interface Props {
  templateId: string;
}

export function SpreadsheetBoard({ templateId }: Props) {
  const { data: template } = useTemplate(templateId);
  const updateTemplate = useUpdateTemplate(templateId);

  const [sheets, setSheets] = useState<object[]>([
    { name: "Sheet1", celldata: [], order: 0 },
  ]);

  useEffect(() => {
    if (template?.excel_config?.sheets) {
      setSheets(template.excel_config.sheets as object[]);
    }
  }, [template?.excel_config]);

  function handleChange(updatedSheets: object[]) {
    setSheets(updatedSheets);
    // Auto-save debounced in production; for simplicity save on each change
    updateTemplate.mutate({
      excel_config: { sheets: updatedSheets },
    });
  }

  return (
    <div className="flex h-full gap-4">
      <div className="flex-1 bg-white rounded border overflow-hidden" style={{ height: "80vh" }}>
        <Workbook
          data={sheets as never}
          onChange={handleChange}
          showFormulaBar
          showSheetTabs
        />
      </div>
      <aside className="w-56 flex-shrink-0">
        <CellTokenHelper templateId={templateId} />
      </aside>
    </div>
  );
}
