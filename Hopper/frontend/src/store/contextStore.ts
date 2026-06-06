import { create } from "zustand";
import { persist } from "zustand/middleware";

interface ContextState {
    selectedNamespace: string;
    setSelectedNamespace: (namespace: string) => void;
}

export const useContextStore = create<ContextState>()(persist((set) => ({
    selectedNamespace: "__default__",
    setSelectedNamespace: (namespace: string) => set({ selectedNamespace: namespace }),
}), {
    name: "context-store",
}));        