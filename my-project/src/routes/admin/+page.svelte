<script lang="ts">
  import { user } from '$lib/auth.store';
</script>

<h1 class="text-2xl font-semibold">Panel</h1>

{#if $user?.authenticated && $user?.is_staff}
  <!-- Accesos rápidos -->
  <div class="mt-4 flex flex-wrap gap-2">
    <a href="/admin/products"
       class="px-3 py-1.5 rounded ring-1 ring-slate-300 hover:bg-slate-100">
      Productos
    </a>
    <a href="/admin/orders"
       class="px-3 py-1.5 rounded ring-1 ring-slate-300 hover:bg-slate-100">
      Órdenes
    </a>
  </div>

  <!-- Tarjetas -->
  <div class="mt-6 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
    <a href="/admin/products"
       class="group rounded-2xl bg-white ring-1 ring-slate-200 p-5 hover:shadow">
      <div class="text-slate-800 font-semibold">Productos</div>
      <p class="text-sm text-slate-600">Gestiona catálogo, precios e imágenes.</p>
    </a>

    <a href="/admin/orders"
       class="group rounded-2xl bg-white ring-1 ring-slate-200 p-5 hover:shadow">
      <div class="text-slate-800 font-semibold">Órdenes</div>
      <p class="text-sm text-slate-600">Revisa pedidos y su estado.</p>
    </a>
  </div>
{:else}
  <!-- Mensaje si no es staff o no está logueado -->
  <p class="mt-4 text-slate-600">Inicia sesión con una cuenta de staff para ver el panel.</p>
{/if}
