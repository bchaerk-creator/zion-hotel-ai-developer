"""Exemplo fictício da Ferramenta 29 (Calculadora de Custos de Experiências). Todos os números são inventados."""
EX = dict(nome="Trilha guiada com café colonial (fictícia)", preco=180, taxa=5, imposto=6, capacidade=12, previstos=8)
EX_FIXOS = [("Guia (por saída)", 250), ("Transporte de van", 300), ("Seguro do grupo", 60)]          # R$ por sessão
EX_VAR = [("Café colonial", 45), ("Kit com água e lanche", 15), ("Entrada no parque", 20)]          # R$ por participante
NFIX, NVAR, NCEN = 15, 15, 40
