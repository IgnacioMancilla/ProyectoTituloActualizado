// src/app.d.ts
// Asegúrate que este archivo exista
declare global {
  namespace App {
    interface Locals {
      token: string | null;
    }
  }
}
export {};
