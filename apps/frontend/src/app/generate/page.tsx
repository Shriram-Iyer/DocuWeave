"use client";

import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { templatesApi } from "@/lib/api/templates";
import { dataSourcesApi } from "@/lib/api/dataSources";
import { linkConfigsApi } from "@/lib/api/linkConfigs";
import { documentsApi } from "@/lib/api/documents";
import { downloadBlob } from "@/utils/download";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function GeneratePage() {
  const [templateId, setTemplateId] = useState("");
  const [dataSourceId, setDataSourceId] = useState("");
  const [linkConfigId, setLinkConfigId] = useState("");

  const { data: templates = [] } = useQuery({
    queryKey: ["templates"],
    queryFn: templatesApi.list,
  });

  const { data: dataSources = [] } = useQuery({
    queryKey: ["data-sources"],
    queryFn: dataSourcesApi.list,
  });

  const { data: linkConfigs = [] } = useQuery({
    queryKey: ["link-configs"],
    queryFn: linkConfigsApi.list,
  });

  const selectedTemplate = templates.find((t) => t.id === templateId);

  const generateMutation = useMutation({
    mutationFn: () =>
      documentsApi.generate({
        template_id: templateId,
        data_source_id: dataSourceId,
        link_config_id: linkConfigId,
      }),
    onSuccess: (blob) => {
      const ext = selectedTemplate?.output_format === "xlsx" ? "xlsx" : "docx";
      downloadBlob(blob, `${selectedTemplate?.name ?? "document"}.${ext}`);
    },
  });

  const canGenerate = templateId && dataSourceId && linkConfigId && !generateMutation.isPending;

  return (
    <div className="p-8 max-w-lg mx-auto">
      <h1 className="text-2xl font-bold mb-6">Generate Document</h1>

      <div className="space-y-5">
        <div className="space-y-1">
          <Label>Template</Label>
          <Select value={templateId} onValueChange={setTemplateId}>
            <SelectTrigger>
              <SelectValue placeholder="Select a template…" />
            </SelectTrigger>
            <SelectContent>
              {templates.map((t) => (
                <SelectItem key={t.id} value={t.id}>
                  {t.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <Label>Data Source</Label>
          <Select value={dataSourceId} onValueChange={setDataSourceId}>
            <SelectTrigger>
              <SelectValue placeholder="Select a data source…" />
            </SelectTrigger>
            <SelectContent>
              {dataSources.map((ds) => (
                <SelectItem key={ds.id} value={ds.id}>
                  {ds.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <Label>Link Config</Label>
          <Select value={linkConfigId} onValueChange={setLinkConfigId}>
            <SelectTrigger>
              <SelectValue placeholder="Select a link config…" />
            </SelectTrigger>
            <SelectContent>
              {linkConfigs.map((lc) => (
                <SelectItem key={lc.id} value={lc.id}>
                  {lc.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {generateMutation.isError && (
          <p className="text-sm text-destructive">Generation failed. Check your configuration.</p>
        )}

        <Button
          className="w-full"
          disabled={!canGenerate}
          onClick={() => generateMutation.mutate()}
        >
          {generateMutation.isPending ? "Generating…" : "Generate & Download"}
        </Button>
      </div>
    </div>
  );
}
