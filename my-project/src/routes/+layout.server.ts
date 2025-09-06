import { env } from '$env/dynamic/public';

export async function load({ fetch }) {
  try {
    const res = await fetch(`${env.PUBLIC_API_BASE}/auth/me/`, {
      credentials: 'include'
    });
    if (res.ok) {
      const me = await res.json();
      return { authed: true, me };
    }
  } catch {}
  return { authed: false };
}
