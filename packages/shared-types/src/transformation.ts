export type FieldType =
  | "string"
  | "number"
  | "boolean"
  | "date"
  | "array"
  | "object";

export type Operation =
  | "uppercase"
  | "lowercase"
  | "concat"
  | "add"
  | "subtract"
  | "multiply"
  | "divide"
  | "sum_by_group"
  | "count_by_group"
  | "avg_by_group"
  | "min_by_group"
  | "max_by_group"
  | "map"
  | "filter"
  | "reduce";

export interface FieldRef {
  field?: string;
  literal?: string;
  field_type?: FieldType;
  transformations?: TransformationStep[];
}

export interface TransformationStep {
  op: Operation;
  source_field?: string;
  operand?: number;
  fields?: FieldRef[];       // for concat
  group_field?: string;      // for aggregation
  value_field?: string;      // for aggregation
  expression?: string;       // for array ops
}

export interface FieldTransformation {
  output_field: string;
  field_type: FieldType;
  pipeline: TransformationStep[];
}

export interface ValidatePipelineRequest {
  field_type: FieldType;
  pipeline: TransformationStep[];
}

export interface ValidatePipelineResponse {
  is_valid: boolean;
  errors: string[];
}

export interface PreviewPipelineRequest {
  field_type: FieldType;
  pipeline: TransformationStep[];
  sample_data: Record<string, unknown>;
}

export interface PreviewPipelineResponse {
  result: unknown;
  errors: string[];
}
