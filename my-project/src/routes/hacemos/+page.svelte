<!-- src/routes/que-hacemos/+page.svelte (o pégalo en tu home si prefieres) -->
<script>
  const STOVE = "/images/QueHacemos.webp"; // cambia por tu archivo en /static/images
</script>

<section class="mx-auto max-w-7xl px-4 py-10">
  <!-- Título -->
  <h1 class="text-center text-3xl md:text-5xl font-semibold text-amber-800">
    Calefactores de combustión lenta en Coyhaique
  </h1>

  <div class="mt-8 grid gap-8 lg:grid-cols-3">
    <!-- Columna de texto -->
    <div class="lg:col-span-2">
      <!-- Franja amarilla -->
      <div
        class="mb-6 rounded-md bg-amber-500 px-4 py-3 text-center text-xl md:text-2xl font-semibold text-black/90"
      >
        Qué hacemos
      </div>

      <p class="text-lg">
        En <strong>Cocinas Appel</strong> estamos especializados en la
        fabricación y venta de:
      </p>

      <ul class="mt-4 list-disc pl-6 text-lg leading-8 space-y-1">
        <li>Cocinas a leña tradicionales y de combustión lenta.</li>
        <li>Calefactores de combustión lenta.</li>
        <li>Hojalatería.</li>
        <li>Bullones al caño.</li>
        <li>Termo a leña.</li>
        <li>Estanque para serpentin.</li>
        <li>Discos, parrillas enlozadas y en acero inoxidable.</li>
      </ul>

      <h3 class="mt-8 text-xl font-semibold">Nuestra Maestranza</h3>
      <ul class="mt-3 space-y-3 text-lg">
        <li class="flex items-start gap-2">
          <svg class="mt-1 h-4 w-4 text-amber-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path d="M10 1.5 12.7 7l6 .5-4.6 3.9 1.4 5.9L10 14.9 4.5 17.3l1.4-5.9L1.3 7.5 7.3 7 10 1.5z"/>
          </svg>
          <span>Fabricamos cilindrado.</span>
        </li>
        <li class="flex items-start gap-2">
          <svg class="mt-1 h-4 w-4 text-amber-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path d="M10 1.5 12.7 7l6 .5-4.6 3.9 1.4 5.9L10 14.9 4.5 17.3l1.4-5.9L1.3 7.5 7.3 7 10 1.5z"/>
          </svg>
          <span>Corte de plancha de distintas dimensiones.</span>
        </li>
        <li class="flex items-start gap-2">
          <svg class="mt-1 h-4 w-4 text-amber-600" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path d="M10 1.5 12.7 7l6 .5-4.6 3.9 1.4 5.9L10 14.9 4.5 17.3l1.4-5.9L1.3 7.5 7.3 7 10 1.5z"/>
          </svg>
          <span>Confeccionamos bandejas de panadería enlozadas.</span>
        </li>
      </ul>

      <p class="mt-6 text-lg">
        Además, brindamos <strong>cocinas a leña industriales a pedido</strong>,
        precios cómodos y facilidades de pago. Realizamos distribución desde otros
        locales de la región. Conozca nuestra <strong>maestranza</strong>.
      </p>

      <p class="mt-4 text-lg">
        Nos damos a conocer mediante recomendación de los clientes, tarjetas de
        presentación, calendarios y flyers.
      </p>
    </div>

    <!-- Imagen derecha -->
    <aside class="lg:col-span-1">
      <figure
        class="rounded-xl overflow-hidden ring-1 ring-black/10 bg-white lg:sticky lg:top-28"
      >
        <img
          src={STOVE}
          alt="Cocina a leña Appel"
          class="w-full h-auto object-cover"
        />
      </figure>
    </aside>
  </div>
</section>
