import { writable } from 'svelte/store';
import { me, login as apiLogin, logout as apiLogout } from '$lib/api';

export type Session = {
  authenticated: boolean;
  username?: string | null;
  email?: string | null;
  is_staff?: boolean; // <-- agregado
};

export const user = writable<Session | null>(null);

export async function initSession() {
  try {
    const data: any = await me();
    // Normaliza para que siempre existan las claves usadas en el navbar
    user.set(
      data
        ? {
            authenticated: !!data.authenticated,
            username: data.username ?? null,
            email: data.email ?? null,
            is_staff: !!data.is_staff, // <-- clave para {#if $user?.is_staff}
          }
        : null
    );
  } catch {
    user.set(null);
  }
}

export async function doLogin(u: string, p: string) {
  await apiLogin(u, p);
  await initSession();
}

export async function doLogout() {
  await apiLogout();
  user.set(null);
}
