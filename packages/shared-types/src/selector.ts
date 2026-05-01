export interface SelectorConfig {
  type: "table_selector";
  table: string;
  display_fields: string[];
  multi_select: boolean;
}

export interface SelectorOptionsRequest {
  data_source_id: string;
  selector_config: SelectorConfig;
}

export interface SelectorEvaluateRequest {
  data_source_id: string;
  selector_config: SelectorConfig;
  selected_ids: string[];
}
