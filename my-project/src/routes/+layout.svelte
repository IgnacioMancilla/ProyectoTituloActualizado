<script lang="ts">
  import { page } from '$app/stores';
  import "../app.css";
  import { onMount } from "svelte";
  import { initSession, user, doLogout } from "$lib/auth.store";
  import CartMini from '$lib/components/CartMini.svelte';
  let adminOpen = false;
  function toggleAdmin() { adminOpen = !adminOpen; }
  // Logo servido desde /static/images/LogoCocinas.png
  const LOGO = "/images/LogoCocinas.png";

  let mobileOpen = false;
  const toggle = () => (mobileOpen = !mobileOpen);
  const close = () => (mobileOpen = false);

  onMount(initSession);

  async function handleLogout(e: Event) {
    e.preventDefault();
    await doLogout();
    window.location.href = "/"; // o usa goto("/") si prefieres SPA
  }

  import ToastHost from '$lib/ui/ToastHost.svelte';
  $: current = $page.url.pathname;

const linkBase = 'px-3 py-1.5 rounded-lg text-sm font-medium transition';
function navClass(href: string) {
  const active = current === href;
  return `${linkBase} ${active ? 'bg-slate-100 text-slate-900' : 'text-slate-700 hover:bg-slate-100'}`;
}

const btn = 'inline-flex items-center gap-2 rounded-xl px-3 py-1.5 text-sm font-medium transition';
const btnGhost = `${btn} ring-1 ring-slate-300 hover:bg-slate-100`;
const btnPrimary = `${btn} bg-amber-600 text-white hover:bg-amber-700 shadow`;
</script>

<ToastHost />

<div class="min-h-screen flex flex-col bg-slate-50 text-slate-900">
  <nav class="sticky top-0 z-40 bg-white/80 backdrop-blur border-b border-slate-200">
  <div class="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-3">
    <!-- Logo -->
    <a href="/" class="inline-flex items-center" aria-label="Ir al inicio">
      <img src={LOGO} alt="Cocinas Appel" class="h-10 sm:h-12 w-auto select-none" draggable="false" />
    </a>

    <!-- Links desktop -->
    <div class="hidden md:flex gap-1.5 items-center">
      <a href="/" class={navClass('/')}>Inicio</a>
      <a href="/hacemos" class={navClass('/hacemos')}>Qué hacemos</a>
      <a href="/productos" class={navClass('/productos')}>Productos</a>
      <a href="/contacto" class={navClass('/contacto')}>Contacto</a>
      <a href="/galeria" class={navClass('/galeria')}>Galería</a>
    </div>

    <!-- Acciones desktop -->
    <div class="hidden md:flex items-center gap-2">
      {#if $user?.authenticated}
        <span class="text-sm text-slate-600 hidden lg:inline">Hola, <b>{$user.username}</b></span>

        {#if $user?.is_staff}
          <div class="relative"
              on:keydown={(e)=> e.key === 'Escape' && (adminOpen = false)}
              on:focusout={(e)=> { if (!e.currentTarget.contains(e.relatedTarget as Node)) adminOpen = false; }}>
            <button type="button"
                    class={`${btnGhost} inline-flex items-center gap-1`}
                    aria-haspopup="menu"
                    aria-expanded={adminOpen}
                    on:click={toggleAdmin}>
              Panel
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8">
                <path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>

            {#if adminOpen}
              <div class="absolute right-0 mt-2 w-44 rounded-xl border border-slate-200 bg-white shadow-lg py-1 z-50">
                <a href="/admin/products" class="block px-3 py-2 text-sm hover:bg-slate-50" on:click={() => adminOpen=false}>Productos</a>
                <a href="/admin/orders"   class="block px-3 py-2 text-sm hover:bg-slate-50" on:click={() => adminOpen=false}>Órdenes</a>
                <div class="my-1 border-t border-slate-100"></div>
                <a href="/admin"          class="block px-3 py-2 text-sm hover:bg-slate-50" on:click={() => adminOpen=false}>Ir al panel</a>
              </div>
            {/if}
          </div>
        {:else}
          <!-- Si NO es staff, deja el link al panel como estaba -->
          <a href="/admin" class={btnGhost}>Panel</a>
        {/if}

        

        <!-- Botón cerrar sesión -->
        <a href="/logout" on:click|preventDefault={handleLogout} class={btnGhost}>
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M9 12h10m0 0-3-3m3 3-3 3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M13 6V5a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h5a2 2 0 0 0 2-2v-1" stroke-linecap="round"/>
          </svg>
          Cerrar
        </a>
      {:else}
        <a href="/login" class={btnGhost}>
          <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M15 12H5m0 0 3-3M5 12l3 3" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M10 6V5a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-5a2 2 0 0 1-2-2v-1" stroke-linecap="round"/>
          </svg>
          Iniciar sesión
        </a>
        <a href="/registro" class={btnPrimary}>Crear cuenta</a>
      {/if}

      <!-- Carrito mini (desktop) -->
      <CartMini />
    </div>

    <!-- Botón menú móvil -->
    <button
      class="md:hidden inline-flex items-center justify-center rounded-lg p-2 ring-1 ring-slate-300 hover:bg-slate-100"
      on:click={toggle}
      aria-expanded={mobileOpen}
      aria-controls="mobile-menu"
      aria-label="Abrir menú"
    >
      {#if mobileOpen}
        <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M6 6l12 12M18 6L6 18" stroke-linecap="round"/>
        </svg>
      {:else}
        <svg class="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M4 7h16M4 12h16M4 17h16" stroke-linecap="round"/>
        </svg>
      {/if}
    </button>
  </div>

  <!-- Menú móvil -->
  {#if mobileOpen}
    <div id="mobile-menu" class="md:hidden border-t border-slate-200 bg-white">
      <div class="max-w-6xl mx-auto px-4 py-3 space-y-2">
        <div class="grid grid-cols-2 gap-2">
          <a href="/" class={navClass('/')} on:click={close}>Inicio</a>
          <a href="/hacemos" class={navClass('/hacemos')} on:click={close}>Qué hacemos</a>
          <a href="/productos" class={navClass('/productos')} on:click={close}>Productos</a>
          <a href="/contacto" class={navClass('/contacto')} on:click={close}>Contacto</a>
          <a href="/galeria" class={navClass('/galeria')} on:click={close}>Galería</a>
        </div>

        <div class="pt-2 border-t border-slate-200 flex items-center gap-2">
          {#if $user?.authenticated}
            {#if $user?.is_staff}
              <a href="/admin/products" class={btnGhost} on:click={close}>Productos</a>
              <a href="/admin/orders"   class={btnGhost} on:click={close}>Órdenes</a>
            {/if}
            <a href="/admin" class={btnGhost} on:click={close}>Panel</a>
            <a href="/logout" on:click|preventDefault={(e)=>{handleLogout(e); close();}} class={btnGhost}>Cerrar sesión</a>
          {:else}
            <a href="/login" class={btnGhost} on:click={close}>Iniciar sesión</a>
            <a href="/registro" class={btnPrimary} on:click={close}>Crear cuenta</a>
          {/if}
          <div class="ml-auto">
            <CartMini />
          </div>
        </div>
      </div>
    </div>

    <!-- Cierra al tocar fuera -->
    <div class="fixed inset-0 -z-10 md:hidden" on:click={close}></div>
  {/if}
</nav>

  

  

  <!-- Contenido -->
  <main class="flex-1 max-w-6xl mx-auto px-4 py-8">
    <slot />
  </main>

  <!-- Barra de redes -->
  <div class="flex justify-center gap-6 py-8">
    <!-- Facebook -->
    <a href="https://www.facebook.com/cocinasappel/?locale=es_LA" target="_blank" rel="noopener"
       aria-label="Facebook"
       class="grid h-12 w-12 place-items-center rounded-full bg-[#1877F2] text-white shadow hover:shadow-lg hover:scale-105 transition">
      <svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor" aria-hidden="true">
        <path d="M22 12a10 10 0 1 0-11.6 9.9v-7h-2.6V12h2.6V9.7c0-2.6 1.5-4 3.9-4 1.1 0 2.3.2 2.3.2v2.5h-1.3c-1.3 0-1.8.8-1.8 1.7V12h3l-.5 2.9h-2.5v7A10 10 0 0 0 22 12z"/>
      </svg>
    </a>

    <!-- WhatsApp -->
    <a href="https://wa.me/56942312053?text=Hola%20quiero%20información" target="_blank" rel="noopener"
       aria-label="WhatsApp"
       class="grid h-12 w-12 place-items-center rounded-full bg-[#25D366] text-white shadow hover:shadow-lg hover:scale-105 transition">
      <svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor" aria-hidden="true">
        <path d="M20.5 3.5A11.9 11.9 0 0 0 12 0C5.4 0 0 5.4 0 12c0 2 .5 3.8 1.4 5.5L0 24l6.7-1.8A12 12 0 0 0 12 24c6.6 0 12-5.4 12-12 0-3.2-1.3-6.2-3.5-8.5zM12 22a10 10 0 0 1-5.1-1.4l-.4-.3-4 .9.9-3.9-.3-.4A9.9 9.9 0 1 1 22 12c0 5.5-4.5 10-10 10zm5-7.6c-.3-.2-1.8-.9-2-.9-.3-.1-.5-.2-.7.2-.2.3-.8 1-.9 1.2-.2.2-.4.2-.7 0a7.6 7.6 0 0 1-2.2-1.4 8.2 8.2 0 0 1-1.5-1.9c-.2-.3 0-.5.2-.7l.5-.6c.1-.2.2-.3.3-.6 0-.2 0-.4 0-.6 0-.2-.7-1.7-1-2.3-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.9 4.2 4 .6.3 1.1.5 1.5.6.6.2 1.1.2 1.6.1.5-.1 1.8-.7 2-1.4.2-.7.2-1.3.1-1.4z"/>
      </svg>
    </a>

    <!-- Email -->
    <a href="mailto:appelpatagonia@gmail.com?subject=Consulta&body=Hola%2C%20quisiera%20informaci%C3%B3n..."
       aria-label="Email"
       class="grid h-12 w-12 place-items-center rounded-full bg-slate-500 text-white shadow hover:shadow-lg hover:scale-105 transition">
      <svg viewBox="0 0 24 24" class="h-6 w-6" fill="currentColor" aria-hidden="true">
        <path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5L4 8V6l8 5 8-5v2Z"/>
      </svg>
    </a>
  </div>

  <footer class="bg-slate-100">
    <div class="max-w-6xl mx-auto px-4 py-6 text-sm text-slate-600 text-center">
      © {new Date().getFullYear()} Cocinas Appel. Todos los derechos reservados.
    </div>
  </footer>
</div>


