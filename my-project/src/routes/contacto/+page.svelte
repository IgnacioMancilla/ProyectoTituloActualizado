<script lang="ts">
  import { enhance, type SubmitEnhanceOptions } from '$app/forms';
  let { form } = $props<{ form?: import('./$types').ActionData }>();

  let sending = false;
  const enhanceOpts: SubmitEnhanceOptions = {
    pending: () => (sending = true),
    result: () => (sending = false),
    error: () => (sending = false)
  };
</script>

<section class="max-w-5xl mx-auto">
  <div class="grid gap-6 md:grid-cols-5">
    <!-- Lado informativo -->
    <aside class="md:col-span-2 rounded-2xl bg-slate-900 text-white p-6 relative overflow-hidden">
      <div class="absolute -top-16 -right-16 w-56 h-56 rounded-full bg-white/10 blur-2xl"></div>
      <h1 class="text-2xl font-semibold">¿Hablamos?</h1>
      <p class="mt-2 text-slate-200">
        Cuéntanos tu idea y te respondemos a la brevedad.
      </p>

      <ul class="mt-6 space-y-3 text-sm">
        <li class="flex items-center gap-3">
          <!-- icono mail -->
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v1.2l10 6.25 10-6.25V6a2 2 0 0 0-2-2Zm2 6.05-9.34 5.83a2 2 0 0 1-2.32 0L1 10.05V18a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-7.95Z"/></svg>
          appelpatagonia@gmail.com
        </li>
        <li class="flex items-center gap-3">
          <!-- icono phone -->
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M6.62 10.79a15.05 15.05 0 0 0 6.59 6.59l2.2-2.2a1 1 0 0 1 1.02-.24 11.36 11.36 0 0 0 3.56.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1C10.3 21 3 13.7 3 4a1 1 0 0 1 1-1h2.49a1 1 0 0 1 1 1 11.36 11.36 0 0 0 .57 3.56 1 1 0 0 1-.24 1.02l-2.2 2.2Z"/></svg>
          +56 9 1234 5678
        </li>
        <li class="flex items-center gap-3">
          <!-- icono pin -->
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>
          Coyhaique, Chile
        </li>
      </ul>

      <!-- mini mapa opcional -->
      <div class="mt-6 rounded-xl overflow-hidden ring-1 ring-white/10">
        <iframe
          class="w-full h-40 border-0"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"
          src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2792.636582946514!2d-72.06736028826666!3d-45.577746316175755!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xbdf2c5e1e9c3d929%3A0xb79dd3a3375c87f6!2sF%C3%A1brica%20de%20Cocinas%20Appel!5e0!3m2!1ses!2scl!4v1754943316144!5m2!1ses!2scl">
        </iframe>
      </div>
    </aside>

    <!-- Formulario -->
    <form
      method="POST"
      use:enhance={enhanceOpts}
      novalidate
      class="md:col-span-3 bg-white rounded-2xl shadow p-6 md:p-8 space-y-5"
    >
      <h2 class="text-lg font-semibold">Envíanos un mensaje</h2>

      {#if form?.success}
        <div class="rounded-lg bg-green-100 text-green-900 p-3 text-sm">
          ✅ ¡Gracias! Tu mensaje fue enviado correctamente.
        </div>
      {/if}
      {#if form?.server}
        <div class="rounded-lg bg-red-100 text-red-900 p-3 text-sm">
          {form.server}
        </div>
      {/if}

      <!-- honeypot -->
      <div class="hidden">
        <label> No llenar este campo:
          <input name="company" type="text" tabindex="-1" autocomplete="off" />
        </label>
      </div>

      <div class="grid gap-4 sm:grid-cols-2">
        <div>
          <label for="name" class="block text-sm font-medium mb-1">Nombre *</label>
          <input
            id="name" name="name" type="text" required
            value={form?.values?.name ?? ''}
            class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400
                   class:border-red-500={!!form?.errors?.name}"
            aria-invalid={!!form?.errors?.name}
          />
          {#if form?.errors?.name}
            <p class="mt-1 text-xs text-red-600">{form.errors.name}</p>
          {/if}
        </div>

        <div>
          <label for="email" class="block text-sm font-medium mb-1">Email *</label>
          <input
            id="email" name="email" type="email" required
            value={form?.values?.email ?? ''}
            class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400
                   class:border-red-500={!!form?.errors?.email}"
            aria-invalid={!!form?.errors?.email}
          />
          {#if form?.errors?.email}
            <p class="mt-1 text-xs text-red-600">{form.errors.email}</p>
          {/if}
        </div>
      </div>

      <div class="grid gap-4 sm:grid-cols-2">
        <div>
          <label for="phone" class="block text-sm font-medium mb-1">Teléfono</label>
          <input
            id="phone" name="phone" type="tel"
            value={form?.values?.phone ?? ''}
            class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400"
          />
        </div>

        <div>
          <label for="subject" class="block text-sm font-medium mb-1">Asunto</label>
          <input
            id="subject" name="subject" type="text"
            value={form?.values?.subject ?? ''}
            class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400"
          />
        </div>
      </div>

      <div>
        <label for="message" class="block text-sm font-medium mb-1">Mensaje *</label>
        <textarea
          id="message" name="message" required rows="6"
          class="w-full rounded-lg border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-slate-400
                 class:border-red-500={!!form?.errors?.message}"
          aria-invalid={!!form?.errors?.message}
        >{form?.values?.message ?? ''}</textarea>
        {#if form?.errors?.message}
          <p class="mt-1 text-xs text-red-600">{form.errors.message}</p>
        {/if}
      </div>

      <div class="flex items-center justify-between gap-4 pt-2">
        <p class="text-xs text-slate-500">* Campos obligatorios</p>
        <button
          type="submit"
          class="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60 active:scale-[.98]"
          disabled={sending}
        >
          {#if sending}
            <svg class="animate-spin" width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity=".25"/>
              <path d="M22 12a10 10 0 0 1-10 10" stroke="currentColor" stroke-width="4" />
            </svg>
            Enviando…
          {:else}
            Enviar
          {/if}
        </button>
      </div>
    </form>
  </div>
</section>