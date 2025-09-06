const API = import.meta.env.VITE_API_URL;

function getCookie(name: string) {
  return document.cookie.split('; ')
    .find(r => r.startsWith(name + '='))?.split('=')[1] ?? '';
}

async function apiGet(path: string) {
  const r = await fetch(`${API}${path}`, { credentials: 'include' });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function apiPost(path: string, data: any, extraHeaders: Record<string,string> = {}) {
  const r = await fetch(`${API}${path}`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', ...extraHeaders },
    body: JSON.stringify(data),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function ensureCsrf() { return apiGet('/api/csrf/'); }
export async function ping()       { return apiGet('/api/ping/'); }
export async function me()         { return apiGet('/api/auth/me/'); }

export async function login(username: string, password: string) {
  await ensureCsrf();
  const token = getCookie('csrftoken');
  return apiPost('/api/auth/login/', { username, password }, { 'X-CSRFToken': token });
}
export async function logout() {
  const token = getCookie('csrftoken');
  return apiPost('/api/auth/logout/', {}, { 'X-CSRFToken': token });
}

export async function register(payload: {
  username: string; email: string; password: string; password2: string;
}) {
  await ensureCsrf();
  const token = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
  return apiPost('/api/auth/register/', payload, { 'X-CSRFToken': token });
}


// ... lo que ya tienes arriba (ensureCsrf, me, login, logout)

export async function listProducts() {
  return apiGet('/api/products/');
}
export async function getCart() {
  return apiGet('/api/cart/');
}
export async function addToCart(product_id: number, qty = 1) {
  await ensureCsrf();
  const token = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
  return apiPost('/api/cart/items/', { product_id, qty }, { 'X-CSRFToken': token });
}
export async function updateCartItem(item_id: number, qty: number) {
  await ensureCsrf();
  const token = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
  // PATCH:
  return fetch(`${import.meta.env.VITE_API_URL}/api/cart/items/${item_id}/`, {
    method: 'PATCH',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': token },
    body: JSON.stringify({ qty })
  }).then(r => { if(!r.ok) throw r.text(); return r.json(); });
}
export async function removeCartItem(item_id: number) {
  await ensureCsrf();
  const token = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
  return fetch(`${import.meta.env.VITE_API_URL}/api/cart/items/${item_id}/delete/`, {
    method: 'DELETE',
    credentials: 'include',
    headers: { 'X-CSRFToken': token }
  }).then(r => { if(!r.ok) throw r.text(); return r.json(); });
}

export async function checkoutSummary() {
  return apiGet('/api/checkout/summary/');
}

export async function checkoutConfirm(payload: {
  email: string; full_name: string; phone?: string;
  address: string; city: string; region?: string; notes?: string;
}) {
  await ensureCsrf();
  const token = document.cookie.split('; ').find(r => r.startsWith('csrftoken='))?.split('=')[1] ?? '';
  return apiPost('/api/checkout/confirm/', payload, { 'X-CSRFToken': token });
}
