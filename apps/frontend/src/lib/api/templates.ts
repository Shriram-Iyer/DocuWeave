import type { Template, TemplateCreateRequest, TemplateComponent } from "@docuweave/shared-types";
import { apiClient } from "./client";

export const templatesApi = {
  list: () => apiClient.get<Template[]>("/api/v1/templates").then((r) => r.data),
  get: (id: string) => apiClient.get<Template>(`/api/v1/templates/${id}`).then((r) => r.data),
  create: (data: TemplateCreateRequest) =>
    apiClient.post<Template>("/api/v1/templates", data).then((r) => r.data),
  update: (id: string, data: Partial<TemplateCreateRequest>) =>
    apiClient.put<Template>(`/api/v1/templates/${id}`, data).then((r) => r.data),
  delete: (id: string) => apiClient.delete(`/api/v1/templates/${id}`),
  createComponent: (templateId: string, data: Omit<TemplateComponent, "id" | "template_id">) =>
    apiClient
      .post<TemplateComponent>(`/api/v1/templates/${templateId}/components`, data)
      .then((r) => r.data),
  updateComponent: (templateId: string, componentId: string, data: Partial<TemplateComponent>) =>
    apiClient
      .put<TemplateComponent>(`/api/v1/templates/${templateId}/components/${componentId}`, data)
      .then((r) => r.data),
  deleteComponent: (templateId: string, componentId: string) =>
    apiClient.delete(`/api/v1/templates/${templateId}/components/${componentId}`),
};
