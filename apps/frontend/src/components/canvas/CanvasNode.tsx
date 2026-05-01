"use client";

import { useRef } from "react";
import { Group, Rect, Text } from "react-konva";
import type Konva from "konva";
import type { TemplateComponent } from "@docuweave/shared-types";
import { useCanvasStore } from "@/store/canvasStore";

interface Props {
  component: TemplateComponent;
}

export function CanvasNode({ component }: Props) {
  const groupRef = useRef<Konva.Group>(null);
  const selectedId = useCanvasStore((s) => s.selectedId);
  const selectComponent = useCanvasStore((s) => s.selectComponent);
  const moveComponent = useCanvasStore((s) => s.moveComponent);

  const isSelected = selectedId === component.id;
  const pos = component.position;
  const width = typeof pos.width === "number" ? pos.width : 300;
  const height = typeof pos.height === "number" ? pos.height : 60;

  function handleClick() {
    selectComponent(component.id);
  }

  function handleDragEnd(e: Konva.KonvaEventObject<DragEvent>) {
    moveComponent(component.id, { x: e.target.x(), y: e.target.y() });
  }

  const label = component.type === "text"
    ? (component.content || "Text")
    : component.type === "dynamic_field"
    ? `{{${component.source_field || "field"}}}`
    : component.type === "table"
    ? "[ Table ]"
    : component.type === "repeat_block"
    ? `[↻ ${component.repeat_over || "repeat"}]`
    : component.type;

  return (
    <Group
      ref={groupRef}
      x={pos.x}
      y={pos.y}
      draggable
      onClick={handleClick}
      onDragEnd={handleDragEnd}
    >
      <Rect
        width={width}
        height={height}
        fill="white"
        stroke={isSelected ? "#6366f1" : "#d1d5db"}
        strokeWidth={isSelected ? 2 : 1}
        cornerRadius={4}
        shadowColor="rgba(0,0,0,0.08)"
        shadowBlur={4}
      />
      <Text
        text={label}
        x={8}
        y={8}
        width={width - 16}
        height={height - 16}
        fontSize={13}
        fill="#111827"
        wrap="word"
        ellipsis
      />
    </Group>
  );
}
