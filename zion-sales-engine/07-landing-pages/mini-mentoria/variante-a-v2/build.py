#!/usr/bin/env python3
"""Variante A v2 da landing da Mini Mentoria de Estruturação Zion. Uso: python3 -I build.py"""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import comum_v2
comum_v2.build("A", AQUI)
