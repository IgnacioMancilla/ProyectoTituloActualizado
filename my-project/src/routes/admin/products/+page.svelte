<script lang="ts">
  import { onMount } from 'svelte';
  import {
    adminListProducts,
    adminCreateProduct,
    adminPatchProduct,
    adminUploadMainImage,
    adminUploadGallery,
    adminDeleteGallery
  } from '$lib/api.admin';
  import { toastError, toastSuccess } from '$lib/ui/toast';

  // ---------- Estado ----------
  let items: any[] = [];
  let creating = false;

  // estados ocupados por acción
  let busyToggle = new Set<number>();
  let busyMain   = new Set<number>();
  let busyGal    = new Set<number>();
  let busyDel    = new Set<string>(); // `${productId}:${imageId}`

  let form = { name: '', slug: '', price: 0, stock: 0, is_active: true };
  let createMainImage: File | null = null;
  let createPreview: string | null = null;

  const money = new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP' });
  const fmt = (n: unknown) => money.format(Number(n ?? 0) || 0);

  const API = (import.meta.env.VITE_API_URL || '').replace(/\/+$/, '');
  const joinURL = (base: string, path: string) => `${base}${path?.startsWith('/') ? '' : '/'}${path || ''}`;

  onMount(load);

  async function load() {
    try {
      const data = await adminListProducts();
      items = (data || []).map((p: any) => ({ ...p, images: p.images ?? [] }));
    } catch (e: any) {
      toastError(String(e?.message ?? e));
    }
  }

  // util para sets reactivos (Svelte necesita reasignar)
  function addBusy(set: Set<any>, key: any) { const s = new Set(set); s.add(key); return s; }
  function delBusy(set: Set<any>, key: any) { const s = new Set(set); s.delete(key); return s; }

  function onPickCreateMain(e: Event) {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    createMainImage = file;
    if (createPreview) URL.revokeObjectURL(createPreview);
    createPreview = URL.createObjectURL(file);
    input.value = ''; // permite re-seleccionar el mismo archivo
  }
  function clearCreateMain() {
    createMainImage = null;
    if (createPreview) URL.revokeObjectURL(createPreview);
    createPreview = null;
  }

  // ---------- Crear producto (con imagen opcional) ----------
  async function create() {
    if (!form.name?.trim() || !form.slug?.trim()) {
      toastError('Completa Nombre y Slug');
      return;
    }
    creating = true;
    try {
      const product = await adminCreateProduct(form);
      const id = product.id;
      if (createMainImage) {
        busyMain = addBusy(busyMain, id);
        await adminUploadMainImage(id, createMainImage);
      }
      toastSuccess('Producto creado');
      // reset
      form = { name: '', slug: '', price: 0, stock: 0, is_active: true };
      clearCreateMain();
      await load();
    } catch (e: any) {
      toastError(String(e?.message ?? e));
    } finally {
      creating = false;
      busyMain = new Set(); // limpio
    }
  }

  // ---------- Acciones por producto ----------
  async function toggleActive(p: any) {
    const id = p.id;
    const prev = p.is_active;

    // optimista
    updateItem(id, (it) => ({ ...it, is_active: !prev }));
    busyToggle = addBusy(busyToggle, id);

    try {
      await adminPatchProduct(id, { is_active: !prev });
      toastSuccess(`Producto ${prev ? 'desactivado' : 'activado'}`);
    } catch (e: any) {
      // rollback
      updateItem(id, (it) => ({ ...it, is_active: prev }));
      toastError(String(e?.message ?? e));
    } finally {
      busyToggle = delBusy(busyToggle, id);
    }
  }

  async function uploadMain(p: any, file?: File, ev?: Event) {
    if (!file) return;
    const id = p.id;
    busyMain = addBusy(busyMain, id);
    try {
      await adminUploadMainImage(id, file);
      toastSuccess('Imagen principal actualizada');
      await load();
    } catch (e: any) {
      toastError(String(e?.message ?? e));
    } finally {
      busyMain = delBusy(busyMain, id);
      if (ev) (ev.target as HTMLInputElement).value = '';
    }
  }

  async function addGallery(p: any, files?: FileList | File[], ev?: Event) {
    if (!files || !files[0]) return;
    const id = p.id;
    busyGal = addBusy(busyGal, id);
    try {
      const list = Array.from(files as any);

      // UI optimista: blobs temporales
      const optimistic = list.map((f) => ({ id: `tmp-${Math.random()}`, image: URL.createObjectURL(f) }));
      const prevImages = p.images ?? [];
      updateItem(id, (it) => ({ ...it, images: [...prevImages, ...optimistic] }));

      for (const f of list) await adminUploadGallery(id, f);

      // liberar blobs
      optimistic.forEach((o) => URL.revokeObjectURL(o.image));
      await load();
      toastSuccess('Galería actualizada');
    } catch (e: any) {
      toastError(String(e?.message ?? e));
    } finally {
      busyGal = delBusy(busyGal, id);
      if (ev) (ev.target as HTMLInputElement).value = '';
    }
  }

  async function delGallery(p: any, img: any) {
    const pid = p.id;
    const key = `${pid}:${img.id}`;

    // optimista
    const prev = p.images ?? [];
    updateItem(pid, (it) => ({ ...it, images: prev.filter((g: any) => g.id !== img.id) }));
    busyDel = addBusy(busyDel, key);

    try {
      await adminDeleteGallery(img.id);
      toastSuccess('Imagen eliminada');
    } catch (e: any) {
      // rollback
      updateItem(pid, (it) => ({ ...it, images: prev }));
      toastError(`No se pudo eliminar: ${String(e?.message ?? e)}`);
    } finally {
      busyDel = delBusy(busyDel, key);
    }
  }

  // actualizar un producto dentro de items
  function updateItem(id: number, updater: (it: any) => any) {
    items = items.map((it) => (it.id === id ? updater(it) : it));
  }

  // slug desde nombre (opcional)
  function slugify(s: string) {
    return s
      .toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '');
  }
</script>

<h1 class="text-2xl font-semibold mb-5">Productos</h1>

<!-- Crear producto -->
<div class="rounded-2xl border border-slate-200 bg-white p-4 sm:p-5 mb-8">
  <h2 class="text-sm font-semibold text-slate-800 mb-3">Nuevo producto</h2>

  <div class="grid sm:grid-cols-5 gap-3">
    <label class="sm:col-span-2">
      <span class="block text-xs text-slate-600 mb-1">Nombre</span>
      <input
        class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/70"
        placeholder="Ej: Cocina Lenga 90cm"
        bind:value={form.name}
        on:blur={() => { if (!form.slug.trim() && form.name) form.slug = slugify(form.name); }}
      />
    </label>

    <label class="sm:col-span-1">
      <span class="block text-xs text-slate-600 mb-1">Slug</span>
      <div class="flex gap-2">
        <input
          class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/70"
          placeholder="cocina-lenga-90"
          bind:value={form.slug}
        />
        <button type="button" class="rounded-xl ring-1 ring-slate-300 px-3 text-xs hover:bg-slate-50"
          on:click={() => (form.slug = slugify(form.name || form.slug))}>Auto</button>
      </div>
    </label>

    <label>
      <span class="block text-xs text-slate-600 mb-1">Precio</span>
      <input
        class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/70"
        type="number" min="0" placeholder="0" bind:value={form.price}
      />
    </label>

    <label>
      <span class="block text-xs text-slate-600 mb-1">Stock</span>
      <input
        class="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500/70"
        type="number" min="0" placeholder="0" bind:value={form.stock}
      />
    </label>
  </div>

  <div class="mt-3 flex flex-wrap items-center gap-3">
    <!-- Switch activo (animado) -->
    <label class="inline-flex items-center gap-2 select-none text-sm text-slate-700 cursor-pointer">
      <input type="checkbox" bind:checked={form.is_active} class="peer sr-only" />
      <span
        class="relative inline-flex h-6 w-11 items-center rounded-full ring-1 ring-slate-300
               bg-slate-300 peer-checked:bg-amber-600 peer-checked:ring-amber-500/40
               transition-colors duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]"
      >
        <span
          class="absolute left-1 h-4 w-4 rounded-full bg-white shadow-sm transform-gpu
                 transition-transform duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]
                 peer-checked:translate-x-5 peer-active:scale-95"
        />
      </span>
      <span class="ml-1">{form.is_active ? 'Activo' : 'Inactivo'}</span>
    </label>

    <!-- Imagen principal al crear -->
    <div class="flex items-center gap-2">
      <label class="text-sm text-slate-700">Imagen principal</label>
      <label class="relative inline-flex cursor-pointer">
        <input type="file" accept="image/*" class="sr-only" on:change={onPickCreateMain} />
        <span class="rounded-xl ring-1 ring-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50">Seleccionar</span>
      </label>
      {#if createPreview}
        <div class="flex items-center gap-2">
          <img src={createPreview} alt="preview" class="h-10 w-10 object-cover rounded-lg ring-1 ring-slate-200" />
          <button type="button" class="text-xs text-rose-600 hover:underline" on:click={clearCreateMain}>Quitar</button>
        </div>
      {/if}
    </div>

    <div class="ml-auto">
      <button
        type="button"
        class="inline-flex items-center gap-2 rounded-xl bg-amber-600 text-white px-4 py-2 text-sm font-medium shadow hover:bg-amber-700 disabled:opacity-60 disabled:cursor-not-allowed"
        on:click={create}
        disabled={creating}
      >
        {#if creating}
          <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"/>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 0 1 8-8v3a5 5 0 0 0-5 5H4z"/>
          </svg>
          Creando…
        {:else}
          Crear
        {/if}
      </button>
    </div>
  </div>
</div>

<!-- Grid de productos -->
<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
  {#each items as p (p.id)}
    <div class="rounded-2xl border border-slate-200 bg-white overflow-hidden">
      <!-- Imagen principal -->
      <div class="relative h-40 bg-slate-100">
        {#if p.image}
          <img src={joinURL(API, p.image)} alt={p.name} class="h-full w-full object-cover" />
        {:else}
          <div class="grid h-full place-items-center text-slate-400 text-sm">Sin imagen</div>
        {/if}

        <!-- Badge estado -->
        {#if !p.is_active}
          <span class="absolute top-2 left-2 rounded-full bg-slate-900/80 text-white text-[11px] px-2 py-0.5">Inactivo</span>
        {/if}
      </div>

      <!-- Info -->
      <div class="p-4 space-y-3">
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <p class="truncate font-medium text-slate-900">{p.name}</p>
            <p class="text-xs text-slate-500">/{p.slug}</p>
          </div>

          <!-- Switch activo (animado, con busy) -->
          <label class="inline-flex items-center gap-2 select-none text-xs text-slate-700 cursor-pointer">
            <input
              type="checkbox"
              checked={p.is_active}
              on:change={() => toggleActive(p)}
              class="peer sr-only"
              disabled={busyToggle.has(p.id)}
            />
            <span
              class="relative inline-flex h-5 w-9 items-center rounded-full ring-1 ring-slate-300
                     bg-slate-300 peer-checked:bg-amber-600 peer-checked:ring-amber-500/40
                     transition-colors duration-300 ease-[cubic-bezier(0.34,1.56,0.64,1)]
                     disabled:opacity-60"
            >
              <span
                class="absolute left-1 h-3.5 w-3.5 rounded-full bg-white shadow-sm transform-gpu
                       transition-transform duration-50 ease-[cubic-bezier(0.34,1.56,0.64,1)]
                       peer-checked:translate-x-4 peer-active:scale-95"
              />
            </span>
            {#if busyToggle.has(p.id)}
              <svg class="h-3.5 w-3.5 animate-spin text-slate-500" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-opacity=".25" stroke-width="3" />
                <path d="M21 12a9 9 0 0 1-9 9" stroke="currentColor" stroke-width="3" stroke-linecap="round" />
              </svg>
            {:else}
              {p.is_active ? 'activo' : 'inactivo'}
            {/if}
          </label>
        </div>

        <div class="flex items-center justify-between text-sm text-slate-700">
          <span>Precio: <b>{fmt(p.price)}</b></span>
          <span>Stock: <b>{p.stock}</b></span>
        </div>

        <!-- Subir imagen principal -->
        <div class="pt-1">
          <label class="block text-xs text-slate-600 mb-1">Imagen principal</label>
          <label class="relative inline-flex cursor-pointer">
            <input
              type="file"
              accept="image/*"
              class="sr-only"
              on:change={(e: any) => uploadMain(p, e.target.files?.[0], e)}
              disabled={busyMain.has(p.id)}
            />
            <span class="rounded-xl ring-1 ring-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-60">
              {busyMain.has(p.id) ? 'Subiendo…' : 'Seleccionar'}
            </span>
          </label>
        </div>

        <!-- Galería -->
        <div class="pt-1">
          <label class="block text-xs text-slate-600 mb-1">Galería</label>

          <div class="flex flex-wrap items-center gap-2">
            <label class="relative inline-flex cursor-pointer">
              <input
                type="file"
                accept="image/*"
                multiple
                class="sr-only"
                on:change={(e: any) => addGallery(p, e.target.files, e)}
                disabled={busyGal.has(p.id)}
              />
              <span class="rounded-xl ring-1 ring-slate-300 px-3 py-1.5 text-sm hover:bg-slate-50 disabled:opacity-60">
                {busyGal.has(p.id) ? 'Subiendo…' : 'Agregar imágenes'}
              </span>
            </label>
            <span class="text-xs text-slate-500">({p.images?.length || 0})</span>
          </div>

          <div class="grid grid-cols-4 gap-2 pt-2">
            {#each p.images ?? [] as img (img.id)}
              {#key img.id}
                <div class="relative group">
                  <img src={joinURL(API, img.image)} alt="miniatura"
                       class="h-16 w-full object-cover rounded-lg ring-1 ring-slate-200" />
                  <button
                    type="button"
                    class="absolute top-1 right-1 rounded bg-rose-600/90 text-white text-[11px] px-1.5 py-0.5 opacity-0 group-hover:opacity-100 transition
                           disabled:opacity-60"
                    on:click|stopPropagation|preventDefault={() => delGallery(p, img)}
                    aria-label="Eliminar imagen"
                    disabled={busyDel.has(`${p.id}:${img.id}`)}
                  >
                    {busyDel.has(`${p.id}:${img.id}`) ? '...' : 'Eliminar'}
                  </button>
                </div>
              {/key}
            {/each}
          </div>
        </div>
      </div>
    </div>
  {/each}
</div>
