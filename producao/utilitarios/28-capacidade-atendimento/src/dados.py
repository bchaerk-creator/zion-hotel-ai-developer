"""Fonte única do exemplo fictício da Ferramenta 28 (Planner de Capacidade e Atendimento)."""
EX_HOJE = "2026-11-20"
# (experiência, capacidade por saída, pessoas por condutor, mínimo para confirmar, decidir com quantos dias, ponto de encontro)
EX_EXP = [
    ("Trilha da Cachoeira (fictícia)", 12, 6, 4, 2, "Recepção"),
    ("Café colonial (fictício)", 20, 10, 6, 1, "Salão"),
    ("Aula de pão caseiro (fictícia)", 8, 8, 3, 2, "Cozinha"),
    ("Passeio de barco (fictício)", 10, 5, None, None, "Píer"),
]
# (data, horário, experiência, pessoas reservadas, condutores escalados, lista de espera)
EX_SAI = [
    ("2026-11-18", "08:00", "Trilha da Cachoeira (fictícia)", 9, 2, None),
    ("2026-11-21", "08:00", "Trilha da Cachoeira (fictícia)", 12, 2, 3),
    ("2026-11-21", "09:00", "Café colonial (fictício)", 14, 1, None),
    ("2026-11-22", "15:00", "Aula de pão caseiro (fictícia)", 2, 1, None),
    ("2026-11-24", "08:00", "Trilha da Cachoeira (fictícia)", 3, 1, None),
    ("2026-11-25", "09:00", "Café colonial (fictício)", 8, 1, None),
    ("2026-11-26", "10:00", "Passeio de barco (fictício)", 11, 2, None),
    ("2026-11-27", "10:00", "Passeio de barco (fictício)", 6, 2, None),
    ("2026-11-28", "14:00", "Cavalgada (fictícia)", 4, 1, None),
    (None, "08:00", "Trilha da Cachoeira (fictícia)", 5, 1, None),
    ("2026-12-03", "15:00", "Aula de pão caseiro (fictícia)", 8, 1, None),
]
FUTURAS = ("Acima da capacidade", "Falta condutor", "Decida: confirmar ou cancelar", "Abaixo do mínimo",
           "Lotada, com lista de espera", "Lotada", "Confirmada")
VALIDAS = ("Já passou",) + FUTURAS
