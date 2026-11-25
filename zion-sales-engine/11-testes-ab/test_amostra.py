#!/usr/bin/env python3
"""Testa amostra.py contra valores de referência conhecidos (calculadoras padrão). python3 -I test_amostra.py"""
import sys; sys.path.insert(0, __import__("pathlib").Path(__file__).parent.as_posix())
from amostra import n_por_variante
# Referência 1: ClickMax docs (ab-test): base 10%, efeito 20% relativo, 95% confiança -> cerca de 3.841 por variação (poder não declarado; ~ poder 80%)
n = n_por_variante(0.10, 0.20, 0.05, 0.80); print("10% +20% rel:", n); assert 3600 <= n <= 3900, n
# Referência 2 (fórmula clássica): 5% -> 6% (efeito 20% rel), alfa 5%, poder 80% => ~8.155 por grupo
n = n_por_variante(0.05, 0.20); print("5% +20% rel:", n); assert 8000 <= n <= 8300, n
# Monotonia: efeito menor exige amostra maior; poder maior exige amostra maior
assert n_por_variante(0.02, 0.2) > n_por_variante(0.02, 0.5)
assert n_por_variante(0.02, 0.3, poder=0.9) > n_por_variante(0.02, 0.3, poder=0.8)
print("OK")
