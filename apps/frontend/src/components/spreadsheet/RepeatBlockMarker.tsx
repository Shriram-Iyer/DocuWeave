"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface RepeatBlock {
  tableName: string;
  startRow: number;
  endRow: number;
}

interface Props {
  onAddBlock: (block: RepeatBlock) => void;
}

export function RepeatBlockMarker({ onAddBlock }: Props) {
  const [tableName, setTableName] = useState("");
  const [startRow, setStartRow] = useState("");
  const [endRow, setEndRow] = useState("");

  function handleAdd() {
    if (!tableName || !startRow || !endRow) return;
    onAddBlock({
      tableName,
      startRow: Number(startRow),
      endRow: Number(endRow),
    });
    setTableName("");
    setStartRow("");
    setEndRow("");
  }

  return (
    <div className="bg-white border rounded p-3 text-sm space-y-3">
      <p className="font-semibold text-xs text-muted-foreground uppercase tracking-wide">
        Repeat Block
      </p>
      <p className="text-xs text-muted-foreground">
        Mark a row range to repeat for each row in a table.
      </p>

      <div className="space-y-2">
        <div className="space-y-1">
          <Label className="text-xs">Table name</Label>
          <Input
            value={tableName}
            onChange={(e) => setTableName(e.target.value)}
            placeholder="users"
            className="h-7 text-xs"
          />
        </div>
        <div className="flex gap-2">
          <div className="space-y-1 flex-1">
            <Label className="text-xs">Start row</Label>
            <Input
              type="number"
              value={startRow}
              onChange={(e) => setStartRow(e.target.value)}
              placeholder="2"
              className="h-7 text-xs"
            />
          </div>
          <div className="space-y-1 flex-1">
            <Label className="text-xs">End row</Label>
            <Input
              type="number"
              value={endRow}
              onChange={(e) => setEndRow(e.target.value)}
              placeholder="4"
              className="h-7 text-xs"
            />
          </div>
        </div>
        <Button size="sm" className="w-full h-7 text-xs" onClick={handleAdd}>
          Add Block
        </Button>
      </div>

      <div className="mt-2 space-y-1">
        <p className="text-xs text-muted-foreground">
          Generates{" "}
          <code className="bg-muted px-1 rounded">{"{{#repeat table_name}}"}</code> markers in the
          first and last cells of the selected rows.
        </p>
      </div>
    </div>
  );
}
