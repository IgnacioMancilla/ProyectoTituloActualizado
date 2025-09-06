import { writable } from 'svelte/store';

export type ToastType = 'success' | 'error' | 'info';
export type Toast = { id: number; text: string; type: ToastType; timeout?: number };

function createToasts() {
  const { subscribe, update } = writable<Toast[]>([]);
  let id = 0;

  function show(text: string, type: ToastType = 'info', timeout = 2500) {
    const t = { id: ++id, text, type, timeout };
    update((list) => [...list, t]);
    if (timeout > 0) {
      setTimeout(() => dismiss(t.id), timeout);
    }
  }
  function dismiss(id: number) {
    update((list) => list.filter((t) => t.id !== id));
  }
  return { subscribe, show, dismiss };
}

export const toasts = createToasts();

// helpers
export const toastSuccess = (msg: string, ms = 2500) => toasts.show(msg, 'success', ms);
export const toastError   = (msg: string, ms = 3000)  => toasts.show(msg, 'error', ms);
export const toastInfo    = (msg: string, ms = 2000)  => toasts.show(msg, 'info', ms);
