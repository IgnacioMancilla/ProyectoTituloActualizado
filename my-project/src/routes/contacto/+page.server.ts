import type { Actions } from './$types';
import { fail } from '@sveltejs/kit';

export const actions: Actions = {
  default: async ({ request }) => {
    const fd = await request.formData();

    const name = (fd.get('name') as string | null)?.trim() ?? '';
    const email = (fd.get('email') as string | null)?.trim() ?? '';
    const phone = (fd.get('phone') as string | null)?.trim() ?? '';
    const subject = (fd.get('subject') as string | null)?.trim() ?? '';
    const message = (fd.get('message') as string | null)?.trim() ?? '';
    const trap = (fd.get('company') as string | null)?.trim() ?? ''; // honeypot

    const errors: Record<string, string> = {};
    if (!name) errors.name = 'Ingresa tu nombre.';
    if (!email || !/^\S+@\S+\.\S+$/.test(email)) errors.email = 'Email inválido.';
    if (!message || message.length < 10) errors.message = 'Escribe al menos 10 caracteres.';

    if (Object.keys(errors).length) {
      return fail(400, { success: false, errors, values: { name, email, phone, subject, message } });
    }

    if (trap) return { success: true }; // bot atrapado, respondemos OK sin procesar

    // Aquí iría el post a tu backend Django si quieres enviarlo:
    // await fetch('/api/contact', { method:'POST', headers:{'Content-Type':'application/json'},
    //   body: JSON.stringify({ name, email, phone, subject, message })
    // });

    return { success: true };
  }
};
