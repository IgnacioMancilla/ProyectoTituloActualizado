const API = import.meta.env.VITE_API_URL;

function getCSRFTOKEN() {
  return document.cookie.split('; ').find(x => x.startsWith('csrftoken='))?.split('=')[1] ?? '';
}

export async function adminListProducts() {
  const r = await fetch(`${API}/api/admin/products/`, { credentials: 'include' });
  return r.json();
}
export async function adminCreateProduct(p: {name:string; slug:string; price:number; stock:number; is_active:boolean}) {
  const r = await fetch(`${API}/api/admin/products/`, {
    method: 'POST', credentials: 'include',
    headers: { 'Content-Type':'application/json', 'X-CSRFToken': getCSRFTOKEN() },
    body: JSON.stringify(p)
  });
  if (!r.ok) throw await r.text();
  return r.json();
}
export async function adminPatchProduct(id:number, patch: any) {
  const r = await fetch(`${API}/api/admin/products/${id}/`, {
    method: 'PATCH', credentials: 'include',
    headers: { 'Content-Type':'application/json', 'X-CSRFToken': getCSRFTOKEN() },
    body: JSON.stringify(patch)
  });
  if (!r.ok) throw await r.text();
  return r.json();
}
export async function adminUploadMainImage(id:number, file: File) {
  const fd = new FormData(); fd.append('image', file);
  const r = await fetch(`${API}/api/admin/products/${id}/upload-main/`, {
    method: 'POST', credentials: 'include',
    headers: { 'X-CSRFToken': getCSRFTOKEN() }, body: fd
  });
  if (!r.ok) throw await r.text(); return r.json();
}
export async function adminUploadGallery(id:number, file: File) {
  const fd = new FormData(); fd.append('image', file);
  const r = await fetch(`${API}/api/admin/products/${id}/gallery/`, {
    method: 'POST', credentials: 'include',
    headers: { 'X-CSRFToken': getCSRFTOKEN() }, body: fd
  });
  if (!r.ok) throw await r.text(); return r.json();
}
export async function adminDeleteGallery(imgId:number) {
  const r = await fetch(`${API}/api/admin/products/gallery/${imgId}/delete/`, {
    method: 'DELETE', credentials: 'include',
    headers: { 'X-CSRFToken': getCSRFTOKEN() }
  });
  if (!r.ok) throw await r.text(); return r.json();
}

export async function adminListOrders() {
  const r = await fetch(`${API}/api/admin/orders/`, { credentials: 'include' });
  return r.json();
}
export async function adminUpdateOrderStatus(id:number, status:'pending'|'paid'|'cancelled') {
  const r = await fetch(`${API}/api/admin/orders/${id}/status/`, {
    method: 'PATCH', credentials: 'include',
    headers: { 'Content-Type':'application/json', 'X-CSRFToken': getCSRFTOKEN() },
    body: JSON.stringify({ status })
  });
  if (!r.ok) throw await r.text();
  return r.json();
}
