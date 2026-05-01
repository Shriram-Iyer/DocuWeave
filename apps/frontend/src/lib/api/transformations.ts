import type {
  ValidatePipelineRequest,
  ValidatePipelineResponse,
  PreviewPipelineRequest,
  PreviewPipelineResponse,
} from "@docuweave/shared-types";
import { apiClient } from "./client";

export const transformationsApi = {
  validate: (data: ValidatePipelineRequest) =>
    apiClient
      .post<ValidatePipelineResponse>("/api/v1/transformations/validate", data)
      .then((r) => r.data),
  preview: (data: PreviewPipelineRequest) =>
    apiClient
      .post<PreviewPipelineResponse>("/api/v1/transformations/preview", data)
      .then((r) => r.data),
};
