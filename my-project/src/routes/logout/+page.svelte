<script lang="ts">
  import { onMount } from 'svelte';
  import { doLogout } from '$lib/auth.store';
  import { goto } from '$app/navigation';
  import { toastInfo } from '$lib/ui/toast';

  onMount(async () => {
    await doLogout();
    toastInfo('Sesión cerrada');
    goto('/');
  });
</script>

<p class="p-6">Cerrando sesión…</p>
