"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Props {
  rows: Record<string, unknown>[];
  displayFields: string[];
  selectedIds: string[];
  idField: string;
  multiSelect: boolean;
  onToggle: (id: string) => void;
}

export function SelectionTable({ rows, displayFields, selectedIds, idField, multiSelect, onToggle }: Props) {
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead className="w-8" />
          {displayFields.map((f) => (
            <TableHead key={f}>{f}</TableHead>
          ))}
        </TableRow>
      </TableHeader>
      <TableBody>
        {rows.map((row) => {
          const id = String(row[idField]);
          const selected = selectedIds.includes(id);
          return (
            <TableRow
              key={id}
              className="cursor-pointer"
              data-state={selected ? "selected" : undefined}
              onClick={() => onToggle(id)}
            >
              <TableCell>
                <input
                  type={multiSelect ? "checkbox" : "radio"}
                  readOnly
                  checked={selected}
                  className="pointer-events-none"
                />
              </TableCell>
              {displayFields.map((f) => (
                <TableCell key={f}>{String(row[f] ?? "")}</TableCell>
              ))}
            </TableRow>
          );
        })}
        {rows.length === 0 && (
          <TableRow>
            <TableCell colSpan={displayFields.length + 1} className="text-center text-muted-foreground">
              No data available.
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}
