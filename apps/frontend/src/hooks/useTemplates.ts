import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { Template, TemplateCreateRequest } from "@docuweave/shared-types";
import { templatesApi } from "@/lib/api/templates";

export function useTemplates() {
  return useQuery({ queryKey: ["templates"], queryFn: templatesApi.list });
}

export function useTemplate(id: string) {
  return useQuery({
    queryKey: ["templates", id],
    queryFn: () => templatesApi.get(id),
    enabled: !!id,
  });
}

export function useCreateTemplate() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: TemplateCreateRequest) => templatesApi.create(data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["templates"] }),
  });
}

export function useUpdateTemplate(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (data: Partial<TemplateCreateRequest>) => templatesApi.update(id, data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["templates"] });
      qc.invalidateQueries({ queryKey: ["templates", id] });
    },
  });
}

export function useDeleteTemplate() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => templatesApi.delete(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["templates"] }),
  });
}
