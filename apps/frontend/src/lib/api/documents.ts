import type { GenerateDocumentRequest } from "@docuweave/shared-types";
import { apiClient } from "./client";

export const documentsApi = {
  generate: async (data: GenerateDocumentRequest): Promise<Blob> => {
    const response = await apiClient.post("/api/v1/documents/generate", data, {
      responseType: "blob",
    });
    return response.data as Blob;
  },
};
