<script lang="ts">
  import { toasts, type Toast } from './toast';
  import { fly, fade } from 'svelte/transition';
  let list: Toast[] = [];
  const typeStyles: Record<string, string> = {
    success: 'bg-emerald-600',
    error: 'bg-rose-600',
    info: 'bg-slate-700'
  };
  $: toasts.subscribe((v) => (list = v));
</script>

<div class="pointer-events-none fixed bottom-4 right-4 z-[100] space-y-2">
  {#each list as t (t.id)}
    <div
      in:fly={{ x: 24, duration: 150 }}
      out:fade={{ duration: 120 }}
      class="pointer-events-auto min-w-[240px] max-w-[320px] rounded-lg px-4 py-3 text-white shadow-lg ring-1 ring-black/5"
      class:bg-emerald-600={t.type === 'success'}
      class:bg-rose-600={t.type === 'error'}
      class:bg-slate-700={t.type === 'info'}
      role="status" aria-live="polite">
      <div class="text-sm">{t.text}</div>
    </div>
  {/each}
</div>
