"use client";

import { useDroppable } from "@dnd-kit/core";
import { Stage, Layer } from "react-konva";
import { useCanvasStore } from "@/store/canvasStore";
import { CanvasNode } from "./CanvasNode";

const CANVAS_WIDTH = 794;  // A4 width in px at 96dpi
const CANVAS_HEIGHT = 1123; // A4 height in px

interface Props {
  templateId: string;
}

export function CanvasBoard({ templateId: _ }: Props) {
  const components = useCanvasStore((s) => s.components);
  const selectComponent = useCanvasStore((s) => s.selectComponent);

  const { setNodeRef } = useDroppable({ id: "canvas-drop-zone" });

  return (
    <div
      ref={setNodeRef}
      className="bg-white shadow-lg mx-auto"
      style={{ width: CANVAS_WIDTH, minHeight: CANVAS_HEIGHT, position: "relative" }}
    >
      <Stage
        width={CANVAS_WIDTH}
        height={CANVAS_HEIGHT}
        onClick={(e) => {
          if (e.target === e.target.getStage()) selectComponent(null);
        }}
      >
        <Layer>
          {components.map((component) => (
            <CanvasNode key={component.id} component={component} />
          ))}
        </Layer>
      </Stage>
    </div>
  );
}
