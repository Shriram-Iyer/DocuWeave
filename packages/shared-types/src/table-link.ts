export interface LinkDef {
  field: string;
  ref_table: string;
  ref_field: string;
}

export interface TableConfig {
  name: string;
  primary_key: string;
  link?: LinkDef;
}

export interface LinkConfig {
  id: string;
  name: string;
  tables: TableConfig[];
}
