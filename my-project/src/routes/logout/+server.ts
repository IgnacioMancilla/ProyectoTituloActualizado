// src/routes/logout/+server.ts
import { redirect, type RequestHandler } from '@sveltejs/kit';
export const POST: RequestHandler = async ({ cookies }) => {
  cookies.delete('jwt', { path: '/' });
  cookies.delete('rt',  { path: '/' });
  throw redirect(303, '/');
};
