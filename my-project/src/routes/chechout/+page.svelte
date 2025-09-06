<script lang="ts">
  import { onMount } from 'svelte';
  import { getCart } from '$lib/api';
  import { checkoutSummary, checkoutConfirm } from '$lib/api';
  import { loadCart, cart } from '$lib/cart.store';
  import { toastError, toastSuccess } from '$lib/ui/toast';
  import { goto } from '$app/navigation';

  let form = { email:'', full_name:'', phone:'', address:'', city:'', region:'', notes:'' };
  let summary:any = null;
  let loading = false;

  onMount(async () => {
    await loadCart();
    summary = await checkoutSummary();
  });

  async function submit() {
    loading = true;
    try {
      const r = await checkoutConfirm(form);
      toastSuccess('Orden creada');
      // carrito queda vacío en el backend; actualiza store
      await loadCart();
      goto(`/gracias?o=${encodeURIComponent(r.order.number)}`);
    } catch (e: any) {
      let msg = String(e);
      try { const j = JSON.parse(msg); msg = j.detail || msg; } catch {}
      if (msg === 'no_stock') msg = 'No hay stock suficiente de un producto';
      if (msg === 'empty_cart') msg = 'Tu carrito está vacío';
      toastError(msg);
    } finally {
      loading = false;
    }
  }
</script>

<h1 class="text-2xl font-semibold mb-4">Checkout</h1>

{#if summary}
  <div class="grid md:grid-cols-3 gap-6">
    <div class="md:col-span-2 space-y-3">
      <input class="w-full border rounded px-3 py-2" placeholder="Nombre completo" bind:value={form.full_name} />
      <input class="w-full border rounded px-3 py-2" type="email" placeholder="Email" bind:value={form.email} />
      <input class="w-full border rounded px-3 py-2" placeholder="Teléfono" bind:value={form.phone} />
      <input class="w-full border rounded px-3 py-2" placeholder="Dirección" bind:value={form.address} />
      <div class="grid grid-cols-2 gap-3">
        <input class="w-full border rounded px-3 py-2" placeholder="Ciudad" bind:value={form.city} />
        <input class="w-full border rounded px-3 py-2" placeholder="Región" bind:value={form.region} />
      </div>
      <textarea class="w-full border rounded px-3 py-2" rows="3" placeholder="Notas (opcional)" bind:value={form.notes}></textarea>

      <button class="rounded bg-amber-600 text-white px-4 py-2 disabled:opacity-60 disabled:cursor-not-allowed"
              on:click={submit} disabled={loading}>
        {#if loading}Procesando…{:else}Confirmar orden{/if}
      </button>
    </div>

    <aside class="space-y-3">
      <div class="rounded border bg-white p-4">
        <h2 class="font-semibold mb-2">Resumen</h2>
        {#if $cart}
          {#each $cart.items as it}
            <div class="flex justify-between text-sm py-1 border-b last:border-0">
              <span>{it.product.name} × {it.qty}</span>
              <span>${it.subtotal}</span>
            </div>
          {/each}
          <div class="flex justify-between mt-2 text-sm">
            <span>Envío</span>
            <span>${summary.cart.shipping}</span>
          </div>
          <div class="flex justify-between mt-2 font-semibold">
            <span>Total</span>
            <span>${summary.cart.total}</span>
          </div>
        {/if}
      </div>
    </aside>
  </div>
{:else}
  <p>Cargando…</p>
{/if}
