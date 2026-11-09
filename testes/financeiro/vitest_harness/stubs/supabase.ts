// STUB do harness de auditoria: cliente Supabase inexistente. Qualquer chamada real falha de propósito (sem serviço externo).
export const supabase = new Proxy({}, { get() { throw new Error("Serviço externo (Supabase) indisponível no harness de auditoria"); } });
export type Json = unknown;
