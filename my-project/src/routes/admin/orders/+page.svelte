<script lang="ts">
  import { onMount } from 'svelte';
  import { adminListOrders, adminUpdateOrderStatus } from '$lib/api.admin';
  import { toastSuccess, toastError } from '$lib/ui/toast';

  let orders:any[] = [];
  onMount(load);
  async function load(){ orders = await adminListOrders(); }

  async function setStatus(o:any, s:'pending'|'paid'|'cancelled'){
    try { await adminUpdateOrderStatus(o.id, s); toastSuccess('Estado actualizado'); await load(); }
    catch(e:any){ toastError(String(e)); }
  }
</script>

<h1 class="text-2xl font-semibold mb-4">Órdenes</h1>
<div class="space-y-3">
  {#each orders as o}
    <div class="rounded border bg-white p-4">
      <div class="flex items-center justify-between">
        <div class="font-medium">#{o.number} — {o.full_name} — ${o.total}</div>
        <div class="text-sm">Estado:
          <select bind:value={o.status} on:change={(e:any)=>setStatus(o, e.target.value)}>
            <option value="pending">pending</option>
            <option value="paid">paid</option>
            <option value="cancelled">cancelled</option>
          </select>
        </div>
      </div>
      <div class="text-sm text-slate-600">{o.email} · {o.address}, {o.city}</div>
      <ul class="mt-2 text-sm list-disc pl-5">
        {#each o.items as it}
          <li>{it.product_name} × {it.qty} — ${it.subtotal}</li>
        {/each}
      </ul>
    </div>
  {/each}
</div>
