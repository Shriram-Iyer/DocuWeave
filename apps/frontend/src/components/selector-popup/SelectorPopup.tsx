"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { selectorsApi } from "@/lib/api/selectors";
import { SelectionTable } from "./SelectionTable";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import type { SelectorConfig } from "@docuweave/shared-types";

interface Props {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  dataSourceId: string;
  selectorConfig: SelectorConfig;
  onConfirm: (selectedIds: string[]) => void;
}

export function SelectorPopup({ open, onOpenChange, dataSourceId, selectorConfig, onConfirm }: Props) {
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const { data: rows = [], isLoading } = useQuery({
    queryKey: ["selector-options", dataSourceId, selectorConfig],
    queryFn: () =>
      selectorsApi.getOptions({
        data_source_id: dataSourceId,
        selector_config: selectorConfig,
      }),
    enabled: open,
  });

  const idField = selectorConfig.display_fields[0] ?? "id";

  function toggle(id: string) {
    if (selectorConfig.multi_select) {
      setSelectedIds((prev) =>
        prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
      );
    } else {
      setSelectedIds([id]);
    }
  }

  function handleConfirm() {
    onConfirm(selectedIds);
    onOpenChange(false);
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            Select {selectorConfig.multi_select ? "records" : "a record"} from{" "}
            <code className="text-sm bg-muted px-1 rounded">{selectorConfig.table}</code>
          </DialogTitle>
        </DialogHeader>

        <div className="max-h-[400px] overflow-auto border rounded">
          {isLoading ? (
            <p className="p-4 text-sm text-muted-foreground">Loading…</p>
          ) : (
            <SelectionTable
              rows={rows as Record<string, unknown>[]}
              displayFields={selectorConfig.display_fields}
              idField={idField}
              selectedIds={selectedIds}
              multiSelect={selectorConfig.multi_select}
              onToggle={toggle}
            />
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            Cancel
          </Button>
          <Button disabled={selectedIds.length === 0} onClick={handleConfirm}>
            Confirm ({selectedIds.length})
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
