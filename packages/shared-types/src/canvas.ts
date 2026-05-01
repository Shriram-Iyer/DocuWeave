export interface CanvasPosition {
  x: number;
  y: number;
  width: number;
  height: number | "auto";
}

export type ComponentType =
  | "text"
  | "table"
  | "image"
  | "dynamic_field"
  | "repeat_block";
