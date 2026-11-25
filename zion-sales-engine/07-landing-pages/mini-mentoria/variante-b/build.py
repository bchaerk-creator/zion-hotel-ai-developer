#!/usr/bin/env python3
"""Variante B da landing /mini-mentoria. Uso: python3 -I build.py"""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent))
import comum
comum.build("B", AQUI)
