import { apiClient } from "./client";
import type { LinkConfig } from "@docuweave/shared-types";

export const linkConfigsApi = {
  list: () => apiClient.get<LinkConfig[]>("/api/v1/link-configs").then((r) => r.data),

  get: (id: string) => apiClient.get<LinkConfig>(`/api/v1/link-configs/${id}`).then((r) => r.data),

  create: (payload: Omit<LinkConfig, "id">) =>
    apiClient.post<LinkConfig>("/api/v1/link-configs", payload).then((r) => r.data),

  update: (id: string, payload: Partial<Omit<LinkConfig, "id">>) =>
    apiClient.put<LinkConfig>(`/api/v1/link-configs/${id}`, payload).then((r) => r.data),

  delete: (id: string) => apiClient.delete(`/api/v1/link-configs/${id}`),
};
