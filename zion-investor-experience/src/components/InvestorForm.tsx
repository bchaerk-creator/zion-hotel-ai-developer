"use client";

import { useState, type FormEvent } from "react";

const profiles = ["Investidor pessoa física", "Family office", "Fundo ou gestora", "Proprietário de terreno", "Outro"];

const field =
  "w-full border-0 border-b bg-transparent px-0 py-3 t-body text-cream placeholder:text-muted-dark focus:outline-none focus:border-cream";

/**
 * Campos só com linha inferior, rótulo acima, alvos de toque de 48px.
 * Fase 1: guarda o pedido localmente e confirma. Fase 2: grava no CRM.
 */
export function InvestorForm() {
  const [sent, setSent] = useState(false);

  function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(e.currentTarget).entries());
    try {
      localStorage.setItem("zion-access-request", JSON.stringify({ ...data, at: new Date().toISOString() }));
    } catch {
      /* armazenamento indisponível: a confirmação segue mesmo assim */
    }
    setSent(true);
  }

  if (sent) {
    return (
      <div className="border-t border-line-dark pt-8">
        <p className="t-subtitle">Pedido registrado.</p>
        <p className="t-support mt-4 text-sand">
          A equipe da Zion entra em contato para a etapa de qualificação e o envio do NDA. O acesso à edição para investidores é liberado depois da assinatura.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="grid gap-8 md:grid-cols-2 md:gap-x-[6vw]" noValidate>
      <div>
        <label htmlFor="name" className="t-label block">Nome completo</label>
        <input id="name" name="name" required autoComplete="name" className={field} style={{ borderColor: "var(--line)", minHeight: 48 }} />
      </div>
      <div>
        <label htmlFor="email" className="t-label block">E-mail</label>
        <input id="email" name="email" type="email" required autoComplete="email" className={field} style={{ borderColor: "var(--line)", minHeight: 48 }} />
      </div>
      <div>
        <label htmlFor="phone" className="t-label block">Telefone</label>
        <input id="phone" name="phone" type="tel" autoComplete="tel" className={field} style={{ borderColor: "var(--line)", minHeight: 48 }} />
      </div>
      <div>
        <label htmlFor="organization" className="t-label block">Empresa ou family office</label>
        <input id="organization" name="organization" autoComplete="organization" className={field} style={{ borderColor: "var(--line)", minHeight: 48 }} />
      </div>
      <fieldset className="md:col-span-2">
        <legend className="t-label mb-3">Perfil</legend>
        <div className="grid gap-3 sm:grid-cols-2 md:grid-cols-3">
          {profiles.map((p) => (
            <label key={p} className="t-table flex min-h-12 items-center gap-3">
              <input type="radio" name="profile" value={p} className="h-5 w-5 accent-gold" />
              {p}
            </label>
          ))}
        </div>
      </fieldset>
      <div className="md:col-span-2">
        <label htmlFor="message" className="t-label block">Interesse</label>
        <textarea id="message" name="message" rows={3} className={field} style={{ borderColor: "var(--line)" }} placeholder="Destino, faixa de aporte ou terreno que quer apresentar" />
      </div>
      <label className="t-table flex min-h-12 items-start gap-3 md:col-span-2">
        <input type="checkbox" name="consent" required className="mt-1 h-5 w-5 accent-gold" />
        <span>Autorizo o contato da Zion e entendo que este material tem caráter informativo e não constitui oferta pública de valores mobiliários.</span>
      </label>
      <div className="md:col-span-2">
        <button type="submit" className="t-table inline-flex min-h-12 items-center bg-cream px-8 font-medium text-ink hover:bg-sand">
          Pedir acesso
        </button>
      </div>
    </form>
  );
}
