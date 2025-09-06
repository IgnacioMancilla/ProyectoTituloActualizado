// src/routes/login/+page.server.ts
import type { Actions } from './$types';
import { fail, redirect } from '@sveltejs/kit';

const API = 'http://localhost:8000'; // Ajusta si tu Django corre en otra URL/puerto

export const actions: Actions = {
  default: async ({ request, cookies, fetch }) => {
    const fd = await request.formData();
    const username = String(fd.get('username') ?? '');
    const password = String(fd.get('password') ?? '');

    const r = await fetch(`${API}/api/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });

    if (!r.ok) {
      return fail(400, { error: 'Credenciales inválidas.' });
    }
    const { access, refresh } = await r.json();

    // Guarda tokens en cookies HttpOnly
    cookies.set('jwt', access,   { path: '/', httpOnly: true, sameSite: 'lax', secure: false, maxAge: 60 * 60 }); // 1h
    cookies.set('rt',  refresh,  { path: '/', httpOnly: true, sameSite: 'lax', secure: false, maxAge: 60 * 60 * 24 * 7 });

    throw redirect(303, '/admin');
  }
};
