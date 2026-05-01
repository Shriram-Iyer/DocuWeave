import { apiClient } from "./client";
import type { DataSource, DataSourceCreateRequest, ConnectionTestResponse } from "@docuweave/shared-types";

export const dataSourcesApi = {
  list: () => apiClient.get<DataSource[]>("/data-sources").then((r) => r.data),

  get: (id: string) => apiClient.get<DataSource>(`/data-sources/${id}`).then((r) => r.data),

  create: (payload: DataSourceCreateRequest) =>
    apiClient.post<DataSource>("/data-sources", payload).then((r) => r.data),

  update: (id: string, payload: Partial<DataSourceCreateRequest>) =>
    apiClient.put<DataSource>(`/data-sources/${id}`, payload).then((r) => r.data),

  delete: (id: string) => apiClient.delete(`/data-sources/${id}`),

  test: (id: string) =>
    apiClient.post<ConnectionTestResponse>(`/data-sources/${id}/test`).then((r) => r.data),

  listTables: (id: string) =>
    apiClient.get<string[]>(`/data-sources/${id}/tables`).then((r) => r.data),

  sampleTable: (id: string, table: string) =>
    apiClient.get<Record<string, unknown>[]>(`/data-sources/${id}/tables/${table}/sample`).then((r) => r.data),
};
