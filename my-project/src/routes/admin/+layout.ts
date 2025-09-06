export const ssr = false;
import { redirect } from '@sveltejs/kit';

export async function load({ fetch }) {
  const r = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/me/`, { credentials: 'include' });
  if (!r.ok) throw redirect(302, '/login');
  const me = await r.json();
  if (!(me.is_staff && me.authenticated)) throw redirect(302, '/');
  return { me };
}
