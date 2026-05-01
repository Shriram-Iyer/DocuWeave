import { apiClient } from "./client";
import type { SelectorOptionsRequest, SelectorEvaluateRequest } from "@docuweave/shared-types";

export const selectorsApi = {
  getOptions: (payload: SelectorOptionsRequest) =>
    apiClient
      .post<Record<string, unknown>[]>("/api/v1/selectors/options", payload)
      .then((r) => r.data),

  evaluate: (payload: SelectorEvaluateRequest) =>
    apiClient
      .post<Record<string, unknown>[]>("/api/v1/selectors/evaluate", payload)
      .then((r) => r.data),
};
