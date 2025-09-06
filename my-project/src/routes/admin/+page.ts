export const ssr = false;  // importante: que corra en el cliente
import { redirect } from '@sveltejs/kit';
import { me } from '$lib/api';

export async function load() {
  const u = await me().catch(() => ({authenticated:false}));
  if (!u.authenticated) throw redirect(302, '/login');
  return { user: u };
}
