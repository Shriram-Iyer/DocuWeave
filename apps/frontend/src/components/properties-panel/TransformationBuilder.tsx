"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useCanvasStore } from "@/store/canvasStore";
import { transformationsApi } from "@/lib/api/transformations";
import type { FieldType, TransformationStep } from "@docuweave/shared-types";
import { Button } from "@/components/ui/button";
import { CheckCircleIcon, XCircleIcon } from "lucide-react";

interface Props {
  componentId: string;
}

export function TransformationBuilder({ componentId }: Props) {
  const components = useCanvasStore((s) => s.components);
  const updateComponent = useCanvasStore((s) => s.updateComponent);
  const component = components.find((c) => c.id === componentId);

  const [fieldType, setFieldType] = useState<FieldType>("string");
  const [pipelineJson, setPipelineJson] = useState(
    JSON.stringify(component?.transformations ?? [], null, 2)
  );
  const [validationResult, setValidationResult] = useState<{ is_valid: boolean; errors: string[] } | null>(null);

  const validate = useMutation({
    mutationFn: () => {
      const pipeline = JSON.parse(pipelineJson) as TransformationStep[];
      return transformationsApi.validate({ field_type: fieldType, pipeline });
    },
    onSuccess: (data) => setValidationResult(data),
    onError: () => setValidationResult({ is_valid: false, errors: ["Invalid JSON"] }),
  });

  function handleSave() {
    try {
      const pipeline = JSON.parse(pipelineJson) as TransformationStep[];
      updateComponent(componentId, { transformations: pipeline });
    } catch {
      alert("Invalid JSON in pipeline");
    }
  }

  return (
    <div className="space-y-2">
      <label className="text-xs font-semibold text-muted-foreground uppercase tracking-wide">
        Transformation Pipeline
      </label>

      <select
        className="w-full border rounded p-1 text-xs"
        value={fieldType}
        onChange={(e) => setFieldType(e.target.value as FieldType)}
      >
        {(["string", "number", "boolean", "date", "array", "object"] as FieldType[]).map((ft) => (
          <option key={ft} value={ft}>{ft}</option>
        ))}
      </select>

      <textarea
        className="w-full border rounded p-2 text-xs font-mono resize-y"
        rows={6}
        value={pipelineJson}
        onChange={(e) => {
          setPipelineJson(e.target.value);
          setValidationResult(null);
        }}
      />

      <div className="flex gap-2">
        <Button size="sm" variant="outline" onClick={() => validate.mutate()} className="flex-1">
          Validate
        </Button>
        <Button size="sm" onClick={handleSave} className="flex-1">
          Save
        </Button>
      </div>

      {validationResult && (
        <div className={`flex items-start gap-1 text-xs p-2 rounded ${validationResult.is_valid ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
          {validationResult.is_valid ? (
            <CheckCircleIcon className="w-3 h-3 mt-0.5 flex-shrink-0" />
          ) : (
            <XCircleIcon className="w-3 h-3 mt-0.5 flex-shrink-0" />
          )}
          <div>
            {validationResult.is_valid
              ? "Pipeline is valid"
              : validationResult.errors.join("; ")}
          </div>
        </div>
      )}
    </div>
  );
}
