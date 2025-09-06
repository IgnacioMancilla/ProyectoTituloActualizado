  <script>
    const img1 = "/images/1.jpg";
    const img2 = "/images/2.jpg";
    const img3 = "/images/3.jpg";

    
    const HERO = "/images/hero.webp";
    
    
  </script>

  <!-- HERO full-bleed (de borde a borde) -->
  <section class="relative left-1/2 right-1/2 -ml-[50vw] -mr-[50vw] w-screen">
<div class="relative h-[clamp(220px,45vw,340px)]">
  <img
    src={HERO}
    alt="Cocina a leña tradicional"
    class="absolute inset-0 w-full h-full object-cover object-[100%_50%] contrast-110"
    loading="eager"
    fetchpriority="high"
  />
  <div class="absolute inset-0 bg-gradient-to-t from-black/55 via-black/20 to-transparent"></div>
</div>


    <!-- Fajas negras con el texto a la derecha -->
    <div class="pointer-events-none absolute inset-0 flex items-center justify-end">
      <div class="mr-4 sm:mr-8 md:mr-12 space-y-3 text-right">
      </div>
    </div>
  </section>


<!-- SECCIÓN DESTACADA -->
<section class="mx-auto max-w-7xl px-4 py-10">
  <!-- Título -->
  <h1 class="text-center text-3xl md:text-5xl font-semibold text-amber-800">
    Cocinas a leña en Coyhaique
  </h1>

  <!-- Franja de iconos -->
  <div
    class="mt-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 overflow-hidden rounded-2xl shadow ring-1 ring-black/5"
  >
    <!-- 1: Personas -->
    <div class="flex h-44 md:h-56 items-center justify-center bg-yellow-400">
      <svg viewBox="0 0 24 24" width="92" height="92" class="text-white" fill="currentColor" aria-hidden="true">
        <path d="M16 11a4 4 0 1 0-3.2-6.4A5.5 5.5 0 0 1 17.5 10c0 .35-.03.69-.08 1.02.2.0.4-.02.58-.02zM7 12a4 4 0 1 0-3.2-6.4A5.5 5.5 0 0 1 8.5 11c0 .35-.03.69-.08 1.02C8.86 12 9.3 12 9.7 12H7z"/>
        <path d="M7 14c-3.31 0-6 2.01-6 4.5V20h12v-1.5C13 16.01 10.31 14 7 14zm9 0c-.82 0-1.6.13-2.33.36A6.47 6.47 0 0 1 19 20v1h5v-1.5C24 16.01 21.31 14 16 14z"/>
      </svg>
    </div>

    <!-- 2: Documento -->
    <div class="flex h-44 md:h-56 items-center justify-center bg-amber-500">
      <svg viewBox="0 0 24 24" width="92" height="92" class="text-white" fill="currentColor" aria-hidden="true">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <path d="M14 2v6h6"/>
        <path d="M8 11h8M8 15h8M8 19h5" stroke="currentColor" stroke-width="2" fill="none"/>
      </svg>
    </div>

    <!-- 3: Carrito -->
    <div class="flex h-44 md:h-56 items-center justify-center bg-yellow-400">
      <svg viewBox="0 0 24 24" width="92" height="92" class="text-white" fill="currentColor" aria-hidden="true">
        <path d="M7 18a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm10 0a2 2 0 1 0 .001 3.999A2 2 0 0 0 17 18zM7.2 6h13l-1.5 7.5a2 2 0 0 1-2 1.6H9l-.4 2H5V15h2l2-9z"/>
      </svg>
    </div>

    <!-- 4: Pulgar -->
    <div class="flex h-44 md:h-56 items-center justify-center bg-amber-500">
      <svg viewBox="0 0 24 24" width="92" height="92" class="text-white" fill="currentColor" aria-hidden="true">
        <path d="M10 22h7a2 2 0 0 0 2-1.5l1.4-6.2A2 2 0 0 0 18.5 12H14l1-5a2 2 0 0 0-2-2h-.5l-4 6V22zM4 22H2V10h2v12z"/>
      </svg>
    </div>
  </div>

  <div class="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-10 text-center">
    <article>
      <h3 class="text-2xl font-semibold mb-3">Quiénes somos</h3>
      <p class="leading-7 text-slate-700">
        Somos <strong class="font-semibold">Cocinas Appel</strong>, una empresa regional con más de 55 años de experiencia.
        Contamos con lo mejor en <strong class="font-semibold">cocinas a leña y calefactores de combustión lenta</strong>.
      </p>
    </article>

    <article>
      <h3 class="text-2xl font-semibold mb-3">Calidad</h3>
      <p class="leading-7 text-slate-700">
        Trabajamos con productos de la más alta calidad. En nuestra <strong class="font-semibold">Fábrica de estufas</strong>
        tenemos <strong class="font-semibold">cocinas a leña, parrillas</strong> y <strong class="font-semibold">bullones al caño</strong>,
        entre otros. ¡Consúltanos!
      </p>
    </article>

    <article>
      <h3 class="text-2xl font-semibold mb-3">Materiales</h3>
      <p class="leading-7 text-slate-700">
        Elaboramos nuestros productos con los mejores materiales del mercado. Profesionales calificados te atenderán de la mejor manera.
      </p>
    </article>

    <article>
      <h3 class="text-2xl font-semibold mb-3">Nuestro servicio</h3>
      <p class="leading-7 text-slate-700">
        Empresas y particulares encontrarán una completa <strong class="font-semibold">atención personalizada</strong>.
        Estamos ubicados en <strong class="font-semibold">Coyhaique</strong>.
      </p>
    </article>
  </div>
</section>

<section class="mt-10">

  <h2 class="text-xl font-semibold mb-4 text-center">Sección 1</h2>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">

    <article class="bg-white rounded-2xl shadow overflow-hidden">

      <img src={img1} alt="Imagen 1" class="w-full h-56 object-cover" loading="lazy" />

      <div class="p-4 text-sm text-slate-600">Descripción breve de la imagen 1.</div>
    </article>


    <article class="bg-white rounded-2xl shadow overflow-hidden">
      <img src={img2} alt="Imagen 2" class="w-full h-56 object-cover" loading="lazy" />
      <div class="p-4 text-sm text-slate-600">Descripción breve de la imagen 2.</div>
    </article>


    <article class="bg-white rounded-2xl shadow overflow-hidden">
      <img src={img3} alt="Imagen 3" class="w-full h-56 object-cover" loading="lazy" />
      <div class="p-4 text-sm text-slate-600">Descripción breve de la imagen 3.</div>
    </article>

  </div>
</section>

