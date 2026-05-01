import type { CanvasPosition } from "@docuweave/shared-types";

export function snapToGrid(value: number, gridSize = 8): number {
  return Math.round(value / gridSize) * gridSize;
}

export function clampPosition(pos: CanvasPosition, stageWidth: number, stageHeight: number): CanvasPosition {
  return {
    ...pos,
    x: Math.max(0, Math.min(pos.x, stageWidth - (pos.width as number))),
    y: Math.max(0, Math.min(pos.y, stageHeight - (pos.height === "auto" ? 40 : (pos.height as number)))),
  };
}
