import type { DragEndEvent } from "@dnd-kit/core";
import type { ComponentType, CanvasPosition } from "@docuweave/shared-types";
import { useCanvasStore } from "@/store/canvasStore";

function makeId() {
  return crypto.randomUUID();
}

export function useCanvas() {
  const { addComponent, moveComponent, removeComponent, selectComponent } = useCanvasStore();

  function handleDrop(event: DragEndEvent) {
    const { active, delta } = event;
    const componentType = active.data.current?.type as ComponentType | undefined;
    if (!componentType) return;

    const dropX = (active.rect.current.initial?.left ?? 0) + delta.x;
    const dropY = (active.rect.current.initial?.top ?? 0) + delta.y;

    const position: CanvasPosition = { x: Math.max(0, dropX), y: Math.max(0, dropY), width: 300, height: "auto" };

    addComponent({
      id: makeId(),
      type: componentType,
      position,
      content: componentType === "text" ? "Double-click to edit…" : "",
      source_table: "",
      source_field: "",
      columns: [],
      repeat_over: "",
      transformations: [],
      sub_components: [],
    });
  }

  return { handleDrop, moveComponent, removeComponent, selectComponent };
}
