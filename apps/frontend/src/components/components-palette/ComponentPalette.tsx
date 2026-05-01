"use client";

import { PaletteItem } from "./PaletteItem";
import { FileTextIcon, TableIcon, ImageIcon, ZapIcon, RepeatIcon } from "lucide-react";
import type { ComponentType } from "@docuweave/shared-types";

const ITEMS: Array<{ type: ComponentType; label: string; icon: React.ReactNode }> = [
  { type: "text", label: "Text Block", icon: <FileTextIcon className="w-4 h-4" /> },
  { type: "table", label: "Table", icon: <TableIcon className="w-4 h-4" /> },
  { type: "image", label: "Image", icon: <ImageIcon className="w-4 h-4" /> },
  { type: "dynamic_field", label: "Dynamic Field", icon: <ZapIcon className="w-4 h-4" /> },
  { type: "repeat_block", label: "Repeat Block", icon: <RepeatIcon className="w-4 h-4" /> },
];

export function ComponentPalette() {
  return (
    <div className="p-3">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3">
        Components
      </p>
      <div className="flex flex-col gap-2">
        {ITEMS.map((item) => (
          <PaletteItem key={item.type} type={item.type} label={item.label} icon={item.icon} />
        ))}
      </div>
    </div>
  );
}
