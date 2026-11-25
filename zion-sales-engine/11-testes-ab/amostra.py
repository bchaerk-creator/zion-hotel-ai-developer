#!/usr/bin/env python3
"""Tamanho de amostra para comparar duas proporções (conversão A × B), bicaudal. Só biblioteca padrão.
n por variante = ( z(1-a/2)*sqrt(2*pbar*(1-pbar)) + z(1-b)*sqrt(p1(1-p1)+p2(1-p2)) )^2 / (p2-p1)^2,  pbar=(p1+p2)/2
Uso:  python3 -I amostra.py --base 0.02 --efeito-relativo 0.30 [--alfa 0.05] [--poder 0.80]
      python3 -I amostra.py --cenarios        (tabela de cenários ROTULADOS como hipotéticos)
Nenhuma taxa de conversão real do negócio está neste arquivo: informe --base com a taxa medida (ClickMax)."""
import argparse, math
from statistics import NormalDist

def n_por_variante(p1, efeito_rel, alfa=0.05, poder=0.80):
    p2 = p1 * (1 + efeito_rel)
    if not (0 < p1 < 1 and 0 < p2 < 1):
        raise ValueError("taxas devem ficar entre 0 e 1")
    z = NormalDist().inv_cdf
    pbar = (p1 + p2) / 2
    num = (z(1 - alfa / 2) * math.sqrt(2 * pbar * (1 - pbar)) + z(poder) * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (p2 - p1) ** 2)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", type=float); ap.add_argument("--efeito-relativo", type=float, default=0.30)
    ap.add_argument("--alfa", type=float, default=0.05); ap.add_argument("--poder", type=float, default=0.80)
    ap.add_argument("--cenarios", action="store_true")
    a = ap.parse_args()
    if a.cenarios:
        print("CENÁRIOS HIPOTÉTICOS (não são taxas reais do negócio). n = visitantes únicos por variante; alfa 5%, poder 80%.")
        print("taxa base | efeito relativo | n por variante | total (A+B)")
        for p in (0.01, 0.02, 0.03, 0.05):
            for e in (0.20, 0.30, 0.50):
                n = n_por_variante(p, e); print(f"{p:8.1%} | {e:14.0%} | {n:14d} | {2*n:d}")
    elif a.base:
        n = n_por_variante(a.base, a.efeito_relativo, a.alfa, a.poder)
        print(f"n por variante: {n} visitantes únicos (total {2*n}); compras esperadas por variante em A: {n*a.base:.1f}")
    else:
        ap.error("use --base ou --cenarios")
