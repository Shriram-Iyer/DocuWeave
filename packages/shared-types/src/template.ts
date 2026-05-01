import type { CanvasPosition, ComponentType } from "./canvas";
import type { TransformationStep } from "./transformation";

export interface TemplateComponent {
  id: string;
  template_id: string;
  type: ComponentType;
  position: CanvasPosition;
  content?: string;
  source_table?: string;
  source_field?: string;
  columns?: Array<{ header: string; field: string }>;
  repeat_over?: string;
  transformations?: TransformationStep[];
  sub_components?: TemplateComponent[];
  sort_order?: number;
}

export interface Template {
  id: string;
  name: string;
  output_format: "docx" | "xlsx";
  components: TemplateComponent[];
  excel_config?: Record<string, unknown> | null;
}

export interface TemplateCreateRequest {
  name: string;
  output_format: "docx" | "xlsx";
  excel_config?: Record<string, unknown> | null;
}
