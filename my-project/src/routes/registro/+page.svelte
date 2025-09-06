<script lang="ts">
  import { register } from '$lib/api';
  import { initSession } from '$lib/auth.store';
  import { goto } from '$app/navigation';
  import { toastSuccess, toastError } from '$lib/ui/toast';

  let username = '';
  let email = '';
  let password = '';
  let password2 = '';
  let loading = false;

  // UI state
  let showPw = false;
  let showPw2 = false;
  let formError = '';

  function validateClient() {
    if (!username || !email || !password || !password2) {
      throw new Error('Completa todos los campos');
    }
    if (password !== password2) {
      throw new Error('Las contraseñas no coinciden');
    }
    if (password.length < 8) {
      throw new Error('La contraseña debe tener al menos 8 caracteres');
    }
    // Validación simple de email (opcional, el backend valida de todas formas)
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    if (!emailOk) {
      throw new Error('Ingresa un email válido');
    }
  }

  function scorePassword(p: string): number {
    if (!p) return 0;
    let score = 0;
    if (p.length >= 8) score++;
    if (p.length >= 12) score++;
    const hasLower = /[a-z]/.test(p);
    const hasUpper = /[A-Z]/.test(p);
    const hasDigit = /\d/.test(p);
    const hasSymbol = /[^A-Za-z0-9]/.test(p);
    const diversity = [hasLower, hasUpper, hasDigit, hasSymbol].filter(Boolean).length;
    if (diversity >= 2) score++;
    if (diversity >= 3) score++;
    return Math.min(score, 4);
  }

  $: pwdScore = scorePassword(password);
  $: pwdLabel = ['Muy débil', 'Débil', 'Aceptable', 'Fuerte', 'Muy fuerte'][pwdScore];
  $: pwdWidth = ['w-0', 'w-1/4', 'w-2/4', 'w-3/4', 'w-full'][pwdScore];

  async function onSubmit() {
    loading = true;
    formError = '';
    try {
      validateClient();
      await register({ username, email, password, password2 });
      await initSession(); // ya debe venir autenticado
      toastSuccess('Cuenta creada, sesión iniciada');
      goto('/');
    } catch (e: any) {
      let msg = String(e?.message ?? e);
      try {
        // Intenta parsear errores JSON del backend
        const err = JSON.parse(msg);
        msg = (err.detail) ??
              (err.username && `Usuario: ${err.username}`) ??
              (err.email && `Email: ${err.email}`) ??
              (err.password && `Contraseña: ${err.password}`) ??
              msg;
      } catch {}
      formError = msg;
      toastError(msg);
    } finally {
      loading = false;
    }
  }
</script>

<!-- Fondo con degradado sutil -->
<div class="min-h-screen bg-gradient-to-br from-amber-50 via-slate-50 to-white flex items-center justify-center p-4">
  <div class="w-full max-w-md">
    <!-- Card con borde degradado -->
    <div class="p-[1px] rounded-2xl bg-gradient-to-br from-amber-500/60 via-amber-300/50 to-slate-200/60 shadow-[0_10px_30px_-12px_rgba(0,0,0,0.2)]">
      <div class="rounded-2xl bg-white backdrop-blur-sm border border-slate-200/60">
        <!-- Header -->
        <div class="px-6 pt-6">
          <div class="flex items-center gap-3">
            <div class="h-10 w-10 rounded-xl bg-amber-100 flex items-center justify-center">
              <!-- Logo/Ícono -->
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                      d="M12 14c3.866 0 7 1.79 7 4v1H5v-1c0-2.21 3.134-4 7-4Zm0-2a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-2xl font-semibold text-slate-900">Crear cuenta</h1>
              <p class="text-sm text-slate-500">Regístrate para continuar con tu compra.</p>
            </div>
          </div>

          {#if formError}
            <div class="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              <div class="flex items-start gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="mt-0.5 h-5 w-5 flex-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                        d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0Z" />
                </svg>
                <p class="leading-5">{formError}</p>
              </div>
            </div>
          {/if}
        </div>

        <!-- Form -->
        <form class="px-6 pb-6 pt-4 space-y-4" on:submit|preventDefault={onSubmit}>
          <!-- Usuario -->
          <div>
            <label for="username" class="block text-sm font-medium text-slate-700">Usuario</label>
            <div class="mt-1 relative">
              <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <!-- icono -->
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 10a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-7 7a7 7 0 1 1 14 0H3Z" />
                </svg>
              </span>
              <input
                id="username"
                class="w-full rounded-xl border border-slate-300 pl-10 pr-3 py-2.5 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/70 focus:border-amber-500 transition"
                placeholder="Tu usuario"
                bind:value={username}
                autocomplete="username"
                aria-invalid={!!formError}
              />
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-slate-700">Email</label>
            <div class="mt-1 relative">
              <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M2 6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v.4l-10 6.25L2 6.4V6Zm0 3.2v8.8a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9.2l-9.4 5.87a2 2 0 0 1-2.2 0L2 9.2Z"/>
                </svg>
              </span>
              <input
                id="email"
                class="w-full rounded-xl border border-slate-300 pl-10 pr-3 py-2.5 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/70 focus:border-amber-500 transition"
                type="email"
                placeholder="tu@correo.com"
                bind:value={email}
                autocomplete="email"
              />
            </div>
          </div>

<!-- Contraseña -->
<div>
  <label for="password" class="block text-sm font-medium text-slate-700">Contraseña</label>
  <div class="mt-1 relative">
    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 1a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5Zm-3 8V6a3 3 0 0 1 6 0v3H9Z"/>
      </svg>
    </span>
    <input
      id="password"
      class="w-full rounded-xl border border-slate-300 pl-10 pr-11 py-2.5 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/70 focus:border-amber-500 transition"
      type={showPw ? 'text' : 'password'}
      placeholder="Mínimo 8 caracteres"
      bind:value={password}
      autocomplete="new-password"
    />
    <button
      type="button"
      class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
      on:click={() => (showPw = !showPw)}
      aria-label={showPw ? 'Ocultar contraseña' : 'Mostrar contraseña'}
    >
      {#if showPw}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor"><path d="M3.53 2.47 2.47 3.53l3.3 3.3C3.92 8.1 2.46 9.9 2 12c2.1 5 7.02 8 10 8 1.69 0 3.57-.58 5.3-1.66l3.17 3.17 1.06-1.06L3.53 2.47ZM12 6c3.2 0 6.52 1.94 8.38 5.27-.36 1.05-1 2.12-1.87 3.12l-2.2-2.2A4.5 4.5 0 0 0 9.8 8.27L7.7 6.17C9.07 5.63 10.54 6 12 6Zm2.7 7.88-4.58-4.58A3 3 0 0 1 14.7 13.9Z"/></svg>
      {:else}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 6c-5 0-9 4.5-10 6 1 1.5 5 6 10 6s9-4.5 10-6c-1-1.5-5-6-10-6Zm0 10a4 4 0 1 1 .001-8.001A4 4 0 0 1 12 16Z"/></svg>
      {/if}
    </button>
  </div>

  <!-- Medidor de fortaleza (solo una vez) -->
  <div class="mt-2">
    <div class="h-2 w-full rounded-full bg-slate-200 overflow-hidden">
      <div class={`h-full ${pwdWidth} transition-all duration-300 rounded-full bg-gradient-to-r from-rose-500 via-amber-500 to-emerald-500`}></div>
    </div>
    <p class="mt-1 text-xs text-slate-500">Fortaleza: <span class="font-medium">{pwdLabel}</span></p>
  </div>
</div>

<!-- Repite contraseña -->
<div>
  <label for="password2" class="block text-sm font-medium text-slate-700">Repite contraseña</label>
  <div class="mt-1 relative">
    <span class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-slate-400" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 1a5 5 0 0 0-5 5v3H6a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8a2 2 0 0 0-2-2h-1V6a5 5 0 0 0-5-5Zm-3 8V6a3 3 0 0 1 6 0v3H9Z"/>
      </svg>
    </span>
    <input
      id="password2"
      class="w-full rounded-xl border border-slate-300 pl-10 pr-11 py-2.5 text-sm placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-amber-500/70 focus:border-amber-500 transition"
      type={showPw2 ? 'text' : 'password'}
      placeholder="Repite tu contraseña"
      bind:value={password2}
      autocomplete="new-password"
    />
    <button
      type="button"
      class="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600"
      on:click={() => (showPw2 = !showPw2)}
      aria-label={showPw2 ? 'Ocultar contraseña' : 'Mostrar contraseña'}
    >
      {#if showPw2}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor"><path d="M3.53 2.47 2.47 3.53l3.3 3.3C3.92 8.1 2.46 9.9 2 12c2.1 5 7.02 8 10 8 1.69 0 3.57-.58 5.3-1.66l3.17 3.17 1.06-1.06L3.53 2.47ZM12 6c3.2 0 6.52 1.94 8.38 5.27-.36 1.05-1 2.12-1.87 3.12l-2.2-2.2A4.5 4.5 0 0 0 9.8 8.27L7.7 6.17C9.07 5.63 10.54 6 12 6Zm2.7 7.88-4.58-4.58A3 3 0 0 1 14.7 13.9Z"/></svg>
      {:else}
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 24 24" fill="currentColor"><path d="M12 6c-5 0-9 4.5-10 6 1 1.5 5 6 10 6s9-4.5 10-6c-1-1.5-5-6-10-6Zm0 10a4 4 0 1 1 .001-8.001A4 4 0 0 1 12 16Z"/></svg>
      {/if}
    </button>
  </div>
</div>

                        

          <!-- CTA -->
          <button
            class="w-full rounded-xl bg-amber-600 text-white py-2.5 text-sm font-medium shadow hover:bg-amber-700 active:bg-amber-800 disabled:opacity-60 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
            disabled={loading}
            type="submit"
          >
            {#if loading}
              <svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"/>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 0 1 8-8v3a5 5 0 0 0-5 5H4z"/>
              </svg>
              Creando…
            {:else}
              Crear cuenta
            {/if}
          </button>

          <!-- Footer -->
          <p class="text-center text-sm text-slate-600">
            ¿Ya tienes cuenta?
            <a href="/login" class="font-medium text-amber-700 hover:text-amber-800 underline underline-offset-4">Inicia sesión</a>
          </p>
        </form>
      </div>
    </div>
  </div>
</div>
