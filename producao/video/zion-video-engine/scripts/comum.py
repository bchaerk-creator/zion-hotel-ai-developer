"""Caminhos e argumentos compartilhados pelos scripts do motor.

Todo script recebe --lesson <id>; a pasta da aula é lessons/<id>/ dentro do motor.
Nada de caminho absoluto de sessão: tudo é relativo a este arquivo.
"""
import argparse
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELOS = RAIZ / 'models'
ASSETS = RAIZ / 'assets'
CHROMIUM = '/opt/pw-browsers/chromium-1243/chrome-linux64/chrome'

# Identidade Zion
CORES = {'black': '#040605', 'moss': '#1B2117', 'cream': '#FEF5F0', 'sand': '#DED6BF',
         'earth': '#8B714E', 'gold': '#C9A96E', 'painel': '#F4EEE6'}


def args_aula(descricao, extra=None):
    ap = argparse.ArgumentParser(description=descricao)
    ap.add_argument('--lesson', required=True, help='id da aula, ex.: p01-a01')
    if extra:
        extra(ap)
    a = ap.parse_args()
    a.pasta = RAIZ / 'lessons' / a.lesson
    a.pasta.mkdir(parents=True, exist_ok=True)
    return a


def chromium_path():
    """Chromium do Playwright: usa o pré-instalado se existir, senão o padrão do Playwright."""
    return CHROMIUM if Path(CHROMIUM).exists() else None
