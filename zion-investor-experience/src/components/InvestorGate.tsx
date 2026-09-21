"use client";

import { useEffect, useState, type FormEvent, type ReactNode } from "react";
import Link from "next/link";
import { Logo } from "./Logo";

const STORAGE_KEY = "zion-investor-unlocked";
const HASH = process.env.NEXT_PUBLIC_INVESTOR_CODE_HASH ?? "";

async function sha256(text: string) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

/**
 * Bloqueio por código de acesso, Fase 1. O código nunca está no site: só o
 * hash SHA-256, definido no build. Não substitui o login por NDA da Fase 3.
 */
export function InvestorGate({ children }: { children: ReactNode }) {
  const [state, setState] = useState<"checking" | "locked" | "open">("checking");
  const [error, setError] = useState(false);

  useEffect(() => {
    try {
      setState(sessionStorage.getItem(STORAGE_KEY) === HASH && HASH ? "open" : "locked");
    } catch {
      setState("locked");
    }
  }, []);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const code = String(new FormData(e.currentTarget).get("code") ?? "").trim();
    const ok = HASH !== "" && (await sha256(code)) === HASH;
    if (ok) {
      try {
        sessionStorage.setItem(STORAGE_KEY, HASH);
      } catch {
        /* sem armazenamento, o acesso vale só nesta página */
      }
      setState("open");
    } else {
      setError(true);
    }
  }

  if (state === "open") return <>{children}</>;

  return (
    <main className="flex min-h-[100svh] flex-col justify-center bg-moss tone-dark text-cream">
      <div className="wrap chapter">
        <div className="text-gold">
          <Logo variant="wordmark" height={18} />
        </div>
        <p className="t-label mt-10">Edição para investidores</p>
        <h1 className="t-statement mt-4 max-w-[16ch]">Uso confidencial, após NDA.</h1>
        {state === "locked" && (
          <form onSubmit={onSubmit} className="mt-12 max-w-[420px]" noValidate>
            <label htmlFor="code" className="t-label block">Código de acesso</label>
            <input
              id="code"
              name="code"
              type="password"
              autoComplete="off"
              required
              className="t-body w-full border-0 border-b bg-transparent px-0 py-3 text-cream focus:border-cream focus:outline-none"
              style={{ borderColor: "var(--line)", minHeight: 48 }}
              onChange={() => setError(false)}
            />
            {error && <p className="t-table mt-3 text-sand">Código não reconhecido.</p>}
            {HASH === "" && <p className="t-table mt-3 text-sand">Acesso ainda não configurado neste ambiente.</p>}
            <div className="mt-8 flex flex-wrap gap-4">
              <button type="submit" className="t-table inline-flex min-h-12 items-center bg-cream px-8 font-medium text-ink hover:bg-sand">
                Entrar
              </button>
              <Link href="/acesso/" className="t-table inline-flex min-h-12 items-center border border-sand px-7 text-sand hover:border-cream hover:text-cream">
                Pedir acesso
              </Link>
            </div>
          </form>
        )}
      </div>
    </main>
  );
}
