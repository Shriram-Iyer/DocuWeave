import { create } from "zustand";
import type { TemplateComponent, CanvasPosition } from "@docuweave/shared-types";

interface CanvasState {
  components: TemplateComponent[];
  selectedId: string | null;

  setComponents: (components: TemplateComponent[]) => void;
  addComponent: (component: TemplateComponent) => void;
  updateComponent: (id: string, updates: Partial<TemplateComponent>) => void;
  removeComponent: (id: string) => void;
  selectComponent: (id: string | null) => void;
  moveComponent: (id: string, position: Partial<CanvasPosition>) => void;
}

export const useCanvasStore = create<CanvasState>((set) => ({
  components: [],
  selectedId: null,

  setComponents: (components) => set({ components }),

  addComponent: (component) =>
    set((state) => ({ components: [...state.components, component] })),

  updateComponent: (id, updates) =>
    set((state) => ({
      components: state.components.map((c) =>
        c.id === id ? { ...c, ...updates } : c
      ),
    })),

  removeComponent: (id) =>
    set((state) => ({
      components: state.components.filter((c) => c.id !== id),
      selectedId: state.selectedId === id ? null : state.selectedId,
    })),

  selectComponent: (id) => set({ selectedId: id }),

  moveComponent: (id, position) =>
    set((state) => ({
      components: state.components.map((c) =>
        c.id === id ? { ...c, position: { ...c.position, ...position } } : c
      ),
    })),
}));
