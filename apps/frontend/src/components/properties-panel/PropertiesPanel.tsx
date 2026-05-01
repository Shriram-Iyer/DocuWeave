"use client";

import { useCanvasStore } from "@/store/canvasStore";
import { TransformationBuilder } from "./TransformationBuilder";
import { TrashIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

interface Props {
  templateId: string;
}

export function PropertiesPanel({ templateId: _ }: Props) {
  const selectedId = useCanvasStore((s) => s.selectedId);
  const components = useCanvasStore((s) => s.components);
  const removeComponent = useCanvasStore((s) => s.removeComponent);
  const updateComponent = useCanvasStore((s) => s.updateComponent);

  const selected = components.find((c) => c.id === selectedId);

  if (!selected) {
    return (
      <div className="p-4 text-sm text-muted-foreground">
        Select a component to edit its properties.
      </div>
    );
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <span className="font-semibold capitalize text-sm">{selected.type.replace("_", " ")}</span>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => removeComponent(selected.id)}
          className="text-destructive hover:text-destructive"
        >
          <TrashIcon className="w-4 h-4" />
        </Button>
      </div>

      {/* Content edit for text/repeat_block */}
      {(selected.type === "text" || selected.type === "repeat_block") && (
        <div>
          <label className="text-xs text-muted-foreground">Content</label>
          <textarea
            className="w-full mt-1 border rounded p-2 text-sm resize-none"
            rows={3}
            value={selected.content}
            onChange={(e) => updateComponent(selected.id, { content: e.target.value })}
          />
        </div>
      )}

      {/* Source table + field for dynamic fields */}
      {(selected.type === "dynamic_field" || selected.type === "table") && (
        <div className="space-y-2">
          <div>
            <label className="text-xs text-muted-foreground">Source Table</label>
            <input
              className="w-full mt-1 border rounded p-2 text-sm"
              value={selected.source_table}
              onChange={(e) => updateComponent(selected.id, { source_table: e.target.value })}
            />
          </div>
          {selected.type === "dynamic_field" && (
            <div>
              <label className="text-xs text-muted-foreground">Source Field</label>
              <input
                className="w-full mt-1 border rounded p-2 text-sm"
                value={selected.source_field}
                onChange={(e) => updateComponent(selected.id, { source_field: e.target.value })}
              />
            </div>
          )}
        </div>
      )}

      {/* Position */}
      <div>
        <label className="text-xs text-muted-foreground">Position (x, y, w)</label>
        <div className="flex gap-1 mt-1">
          {(["x", "y", "width"] as const).map((key) => (
            <input
              key={key}
              type="number"
              className="w-full border rounded p-1 text-xs"
              value={selected.position[key] as number}
              onChange={(e) =>
                updateComponent(selected.id, {
                  position: { ...selected.position, [key]: Number(e.target.value) },
                })
              }
            />
          ))}
        </div>
      </div>

      {/* Transformation builder */}
      <TransformationBuilder componentId={selected.id} />
    </div>
  );
}
