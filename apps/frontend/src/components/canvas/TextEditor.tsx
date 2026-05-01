"use client";

import { useEffect } from "react";
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import { useCanvasStore } from "@/store/canvasStore";

interface Props {
  componentId: string;
  initialContent: string;
  onClose: () => void;
  style?: React.CSSProperties;
}

export function TextEditor({ componentId, initialContent, onClose, style }: Props) {
  const updateComponent = useCanvasStore((s) => s.updateComponent);

  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({ placeholder: "Type here…" }),
    ],
    content: initialContent,
    autofocus: true,
    onBlur: ({ editor }) => {
      updateComponent(componentId, { content: editor.getText() });
      onClose();
    },
  });

  return (
    <div
      style={style}
      className="absolute bg-white border border-indigo-400 rounded shadow-lg p-2 z-50 min-w-[200px]"
    >
      <EditorContent editor={editor} className="text-sm outline-none" />
    </div>
  );
}
