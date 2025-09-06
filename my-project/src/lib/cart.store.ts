import { writable, derived } from 'svelte/store';
import { getCart, addToCart, updateCartItem, removeCartItem } from '$lib/api';

type CartItem = { id:number; product:{id:number; name:string; price:number}; qty:number; unit_price:number; subtotal:number };
type Cart = { id:number; items:CartItem[]; total:number };

export const cart = writable<Cart | null>(null);
export const count = derived(cart, (c) => c ? c.items.reduce((n,i)=>n+i.qty,0) : 0);
export const total = derived(cart, (c) => c?.total ?? 0);

export async function loadCart() {
  cart.set(await getCart());
}

export async function add(product_id:number, qty=1) {
  const r = await addToCart(product_id, qty);
  cart.set(r.cart);
}

export async function update(item_id:number, qty:number) {
  const r = await updateCartItem(item_id, qty);
  cart.set(r.cart);
}

export async function remove(item_id:number) {
  const r = await removeCartItem(item_id);
  cart.set(r.cart);
}
