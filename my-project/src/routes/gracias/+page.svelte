<script lang="ts">
  import { page } from '$app/stores';
  $: orderNum = $page.url.searchParams.get('o');
</script>

<div class="max-w-xl mx-auto p-6 text-center">
  <h1 class="text-2xl font-semibold mb-2">¡Gracias por tu compra!</h1>
  {#if orderNum}
    <p class="text-slate-600">Número de orden: <b>{orderNum}</b></p>
  {/if}
  <a href="/productos" class="mt-6 inline-block rounded bg-slate-900 text-white px-4 py-2">Seguir comprando</a>
</div>
