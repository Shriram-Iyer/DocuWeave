"use client";

import { useTemplate } from "@/hooks/useTemplates";
import { CanvasBoard } from "@/components/canvas/CanvasBoard";
import { SpreadsheetBoard } from "@/components/spreadsheet/SpreadsheetBoard";
import { ComponentPalette } from "@/components/components-palette/ComponentPalette";
import { PropertiesPanel } from "@/components/properties-panel/PropertiesPanel";
import { DndContext } from "@dnd-kit/core";
import { useCanvas } from "@/hooks/useCanvas";

interface Props {
  params: { id: string };
}

export default function EditorPage({ params }: Props) {
  const { id } = params;
  const { data: template, isLoading } = useTemplate(id);
  const { handleDrop } = useCanvas();

  if (isLoading || !template) {
    return <div className="p-8">Loading editor…</div>;
  }

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Left palette — Word mode only */}
      {template.output_format === "docx" && (
        <aside className="w-56 border-r bg-muted/40 flex-shrink-0 overflow-y-auto">
          <ComponentPalette />
        </aside>
      )}

      {/* Main editor area */}
      <main className="flex-1 overflow-auto bg-zinc-100 p-6">
        {template.output_format === "docx" ? (
          <DndContext onDragEnd={handleDrop}>
            <CanvasBoard templateId={id} />
          </DndContext>
        ) : (
          <SpreadsheetBoard templateId={id} />
        )}
      </main>

      {/* Right properties panel */}
      <aside className="w-72 border-l bg-background flex-shrink-0 overflow-y-auto">
        <PropertiesPanel templateId={id} />
      </aside>
    </div>
  );
}
