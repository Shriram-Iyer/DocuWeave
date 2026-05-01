export interface GenerateDocumentRequest {
  template_id: string;
  data_source_id: string;
  link_config_id: string;
  selected_ids?: string[];
}

export interface DataSource {
  id: string;
  name: string;
  db_type: "postgres" | "mysql" | "mongodb";
  created_at: string;
}

export interface DataSourceCreateRequest {
  name: string;
  db_type: "postgres" | "mysql" | "mongodb";
  db_url: string;
}

export interface ConnectionTestResponse {
  connected: boolean;
  error?: string;
}
