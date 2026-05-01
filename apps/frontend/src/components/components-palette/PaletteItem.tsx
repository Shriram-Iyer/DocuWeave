"use client";

import { useDraggable } from "@dnd-kit/core";
import type { ComponentType } from "@docuweave/shared-types";

interface Props {
  type: ComponentType;
  label: string;
  icon: React.ReactNode;
}

export function PaletteItem({ type, label, icon }: Props) {
  const { attributes, listeners, setNodeRef, isDragging } = useDraggable({
    id: `palette-${type}`,
    data: { type },
  });

  return (
    <div
      ref={setNodeRef}
      {...listeners}
      {...attributes}
      className={`flex items-center gap-2 px-3 py-2 rounded border cursor-grab bg-white hover:border-primary transition-colors text-sm ${
        isDragging ? "opacity-50" : ""
      }`}
    >
      {icon}
      <span>{label}</span>
    </div>
  );
}
