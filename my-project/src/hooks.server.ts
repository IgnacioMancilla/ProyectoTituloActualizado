// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('jwt') ?? null;
  event.locals.token = token; // disponible en server load/actions
  return resolve(event);
};
