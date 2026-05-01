"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { dataSourcesApi } from "@/lib/api/dataSources";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import type { DataSource, DataSourceCreateRequest } from "@docuweave/shared-types";

const BLANK: DataSourceCreateRequest = { name: "", db_type: "postgres", connection_url: "" };

export default function DataSourcesPage() {
  const qc = useQueryClient();
  const { data: sources = [], isLoading } = useQuery({
    queryKey: ["data-sources"],
    queryFn: dataSourcesApi.list,
  });

  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<DataSourceCreateRequest>(BLANK);
  const [testResult, setTestResult] = useState<{ connected: boolean; error?: string } | null>(null);

  const createMutation = useMutation({
    mutationFn: dataSourcesApi.create,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["data-sources"] });
      setOpen(false);
      setForm(BLANK);
      setTestResult(null);
    },
  });

  const deleteMutation = useMutation({
    mutationFn: dataSourcesApi.delete,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["data-sources"] }),
  });

  const testMutation = useMutation({
    mutationFn: (id: string) => dataSourcesApi.test(id),
    onSuccess: (data) => setTestResult(data),
  });

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Data Sources</h1>
        <Button onClick={() => setOpen(true)}>Add Data Source</Button>
      </div>

      {isLoading && <p className="text-muted-foreground">Loading…</p>}

      <div className="space-y-3">
        {sources.map((src: DataSource) => (
          <div
            key={src.id}
            className="flex items-center justify-between border rounded-lg p-4 bg-white"
          >
            <div>
              <p className="font-medium">{src.name}</p>
              <Badge variant="secondary" className="mt-1">
                {src.db_type}
              </Badge>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm" onClick={() => testMutation.mutate(src.id)}>
                Test
              </Button>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => deleteMutation.mutate(src.id)}
              >
                Delete
              </Button>
            </div>
          </div>
        ))}
        {sources.length === 0 && !isLoading && (
          <p className="text-muted-foreground text-sm">No data sources yet.</p>
        )}
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Data Source</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-1">
              <Label>Name</Label>
              <Input
                value={form.name}
                onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                placeholder="My PostgreSQL DB"
              />
            </div>
            <div className="space-y-1">
              <Label>Type</Label>
              <Select
                value={form.db_type}
                onValueChange={(v) => setForm((f) => ({ ...f, db_type: v }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="postgres">PostgreSQL</SelectItem>
                  <SelectItem value="mysql">MySQL</SelectItem>
                  <SelectItem value="mongodb">MongoDB</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-1">
              <Label>Connection URL</Label>
              <Input
                value={form.connection_url}
                onChange={(e) => setForm((f) => ({ ...f, connection_url: e.target.value }))}
                placeholder="postgresql://user:pass@host:5432/db"
              />
            </div>
            {testResult && (
              <p
                className={`text-sm ${testResult.connected ? "text-green-600" : "text-destructive"}`}
              >
                {testResult.connected ? "Connection successful!" : `Error: ${testResult.error}`}
              </p>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button
              disabled={createMutation.isPending}
              onClick={() => createMutation.mutate(form)}
            >
              {createMutation.isPending ? "Saving…" : "Save"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
