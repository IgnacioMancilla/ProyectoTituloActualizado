<script lang="ts">
  import { cart, count, total, loadCart, update, remove } from '$lib/cart.store';
  import { onMount } from 'svelte';
  import { fade, scale } from 'svelte/transition';

  onMount(loadCart);

  // UI state
  let open = false;
  const toggle = () => (open = !open);
  const closePanel = () => (open = false);

  // Cerrar con clic fuera
  function clickOutside(node: HTMLElement) {
    const handler = (e: MouseEvent) => {
      if (open && !node.contains(e.target as Node)) closePanel();
    };
    document.addEventListener('mousedown', handler);
    return { destroy: () => document.removeEventListener('mousedown', handler) };
  }

  // Cerrar con Escape
  function onKey(e: KeyboardEvent) {
    if (e.key === 'Escape') closePanel();
  }

  // Formateo de moneda (CLP)
  const money = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' });
  function fmt(n: unknown) {
    const num = typeof n === 'number' ? n : parseFloat(String(n ?? 0));
    return money.format(isNaN(num) ? 0 : num);
  }

  // Helper de imagen (evita errores TS si tu tipo no declara image/image_url)
  type AnyProduct = Record<string, any> | null | undefined;
  function imgUrl(p: AnyProduct) {
    return p?.image || p?.image_url || p?.thumbnail || p?.img || 'https://placehold.co/64x64?text=%20';
  }
</script>

<!-- Botón + Panel -->
<div class="relative inline-block" on:keydown={onKey}>
  <!-- Botón Carrito -->
  <button
    class="relative inline-flex items-center gap-2 rounded-xl bg-white px-3 py-2 text-sm font-medium ring-1 ring-slate-200 shadow-sm hover:shadow transition"
    aria-haspopup="dialog"
    aria-expanded={open}
    aria-controls="cart-panel"
    on:click={toggle}
  >
    <svg class="h-5 w-5 text-slate-700" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M3 3h2l.4 2M7 13h9a2 2 0 0 0 1.94-1.5l1.2-5A1 1 0 0 0 18.2 5H6.1L5.6 3.2A1 1 0 0 0 4.6 3H3"/>
      <circle cx="9" cy="19" r="1.75"></circle>
      <circle cx="17" cy="19" r="1.75"></circle>
    </svg>
    Carrito
    <span class="ml-1 inline-flex min-w-5 items-center justify-center rounded-full bg-amber-600 px-1.5 py-0.5 text-[11px] font-semibold text-white">
      {$count}
    </span>
  </button>

  {#if open}
    <!-- Overlay móvil -->
    <div class="fixed inset-0 z-40 lg:hidden" on:click={closePanel} out:fade={{ duration: 100 }}></div>

    <!-- Panel -->
    <div
      id="cart-panel"
      class="absolute right-0 z-50 mt-2 w-[26rem] max-w-[90vw]"
      use:clickOutside
      in:scale={{ start: 0.95, duration: 120 }}
      out:fade={{ duration: 120 }}
      role="dialog"
      aria-label="Carrito de compras"
    >
      <div class="rounded-2xl border border-slate-200 bg-white shadow-xl">
        <!-- Header -->
        <div class="flex items-center justify-between px-4 py-3 border-b border-slate-200">
          <h3 class="text-sm font-semibold text-slate-800">Tu carrito</h3>
          <button class="p-1.5 rounded hover:bg-slate-100" on:click={closePanel} aria-label="Cerrar carrito">
            <svg class="h-5 w-5 text-slate-500" viewBox="0 0 24 24" fill="none">
              <path stroke="currentColor" stroke-linecap="round" stroke-width="1.5" d="M6 6l12 12M18 6L6 18" />
            </svg>
          </button>
        </div>

        <!-- Contenido -->
        <div class="max-h-[60vh] overflow-y-auto px-2 py-2">
          {#if !$cart || $cart.items.length === 0}
            <!-- Vacío -->
            <div class="px-4 py-10 text-center">
              <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-slate-100">
                <svg class="h-6 w-6 text-slate-400" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M3 3h2l.4 2M7 13h9a2 2 0 0 0 1.94-1.5l1.2-5A1 1 0 0 0 18.2 5H6.1L5.6 3.2A1 1 0 0 0 4.6 3H3"/>
                </svg>
              </div>
              <p class="text-sm text-slate-600">Tu carrito está vacío.</p>
            </div>
          {:else}
            <ul class="divide-y divide-slate-200">
              {#each $cart.items as it (it.id)}
                <li class="flex items-start gap-3 py-3 px-2">
                  <!-- Imagen -->
                  <div class="h-16 w-16 flex-none overflow-hidden rounded-lg border border-slate-200 bg-slate-50">
                    <img
                      src={imgUrl(it.product as AnyProduct)}
                      alt={it.product?.name ?? 'Producto'}
                      class="h-full w-full object-cover"
                      loading="lazy"
                    />
                  </div>

                  <!-- Info -->
                  <div class="min-w-0 flex-1">
                    <div class="flex items-start justify-between gap-2">
                      <p class="truncate text-sm font-medium text-slate-800">{it.product?.name}</p>
                      <button
                        class="shrink-0 rounded p-1 text-slate-400 hover:text-rose-600 hover:bg-rose-50"
                        on:click={() => remove(it.id)}
                        aria-label="Eliminar"
                        title="Eliminar"
                      >
                        <svg class="h-4.5 w-4.5" viewBox="0 0 24 24" fill="none">
                          <path stroke="currentColor" stroke-linecap="round" stroke-width="1.5" d="M6 6l12 12M18 6L6 18" />
                        </svg>
                      </button>
                    </div>

                    <div class="mt-0.5 text-xs text-slate-500">
                      {fmt(it.unit_price)} x {it.qty}
                      <span class="mx-1">•</span>
                      Subtotal: <span class="font-semibold text-slate-700">{fmt(it.subtotal)}</span>
                    </div>

                    <!-- Stepper -->
                    <div class="mt-2 inline-flex items-center rounded-lg ring-1 ring-slate-300 overflow-hidden">
                      <button
                        class="px-2 py-1.5 text-slate-700 hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed"
                        on:click={() => update(it.id, Math.max(1, it.qty - 1))}
                        disabled={it.qty <= 1}
                        aria-label="Disminuir"
                      >
                        −
                      </button>
                      <span class="min-w-8 text-center text-sm">{it.qty}</span>
                      <button
                        class="px-2 py-1.5 text-slate-700 hover:bg-slate-100"
                        on:click={() => update(it.id, it.qty + 1)}
                        aria-label="Aumentar"
                      >
                        +
                      </button>
                    </div>
                  </div>
                </li>
              {/each}
            </ul>
          {/if}
        </div>

        <!-- Footer -->
        <div class="flex items-center justify-between gap-3 border-t border-slate-200 px-4 py-3">
          <div class="text-sm text-slate-600">
            Total: <span class="ml-1 text-base font-semibold text-slate-900">{fmt($total)}</span>
          </div>
          <a
            href="/checkout"
            class="inline-flex items-center justify-center rounded-xl bg-amber-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-amber-700 active:bg-amber-800 transition"
          >
            Ir a pagar
          </a>
        </div>
      </div>
    </div>
  {/if}
</div>


