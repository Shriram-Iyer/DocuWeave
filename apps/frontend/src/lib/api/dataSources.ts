import { apiClient } from "./client";
import type { DataSource, DataSourceCreateRequest, ConnectionTestResponse } from "@docuweave/shared-types";

export const dataSourcesApi = {
  list: () => apiClient.get<DataSource[]>("/api/v1/data-sources").then((r) => r.data),

  get: (id: string) => apiClient.get<DataSource>(`/api/v1/data-sources/${id}`).then((r) => r.data),

  create: (payload: DataSourceCreateRequest) =>
    apiClient.post<DataSource>("/api/v1/data-sources", payload).then((r) => r.data),

  update: (id: string, payload: Partial<DataSourceCreateRequest>) =>
    apiClient.put<DataSource>(`/api/v1/data-sources/${id}`, payload).then((r) => r.data),

  delete: (id: string) => apiClient.delete(`/api/v1/data-sources/${id}`),

  test: (id: string) =>
    apiClient.post<ConnectionTestResponse>(`/api/v1/data-sources/${id}/test`).then((r) => r.data),

  listTables: (id: string) =>
    apiClient.get<string[]>(`/api/v1/data-sources/${id}/tables`).then((r) => r.data),

  sampleTable: (id: string, table: string) =>
    apiClient.get<Record<string, unknown>[]>(`/api/v1/data-sources/${id}/tables/${table}/sample`).then((r) => r.data),
};
