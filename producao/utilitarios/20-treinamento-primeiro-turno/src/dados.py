"""Lista sugerida e exemplo fictício da Ferramenta 20 (Kit de Treinamento do Primeiro Turno).
As seis etapas partem da trilha de onboarding usada nas unidades da Zion (Bíblia Operacional, Notion)."""
ETAPAS = ["1 · Conhecer o lugar", "2 · Cultura e padrão da casa", "3 · Ver a função", "4 · Ler o procedimento",
          "5 · Primeira execução acompanhada", "6 · Confirmação e turno sozinho"]
# (etapa 1-6, tarefa, obrigatória, prazo em dias depois do início)
SUGERIDAS = [
    (1, "Volta por todas as unidades e áreas comuns", "Sim", 0),
    (1, "Onde ficam enxoval, produtos, ferramentas e chaves", "Sim", 0),
    (1, "Contatos de emergência e quem chamar em cada caso", "Sim", 0),
    (2, "Jeito de atender e postura da casa", "Sim", 0),
    (2, "O que nunca pode acontecer (lista da casa)", "Sim", 0),
    (3, "Ver uma limpeza completa de unidade", "Sim", 1),
    (3, "Ver uma troca de enxoval", "Sim", 1),
    (3, "Ver a ronda diária de manutenção", "Sim", 1),
    (3, "Ver um check-in com hóspede", "Não", 2),
    (4, "Ler o checklist ou procedimento da função", "Sim", 2),
    (5, "Fazer uma limpeza completa acompanhada", "Sim", 3),
    (5, "Fazer a ronda diária acompanhada", "Sim", 3),
    (5, "Registrar uma ocorrência (algo quebrado ou faltando)", "Sim", 3),
    (5, "Fazer um check-in acompanhado", "Não", 4),
    (6, "Confirmar que entendeu o padrão da casa", "Sim", 5),
    (6, "Primeiro turno sozinho, com conferência no fim", "Sim", 7),
]
EX = dict(pessoa="Júlia (fictícia)", funcao="Governança e limpeza", inicio="2026-11-02", treina="Carla (fictícia)", hoje="2026-11-05")
# (mostrado, feito junto, fez sozinho e conferido, conferido por) por tarefa sugerida, na mesma ordem
EX_DATAS = [
    ("2026-11-02", "2026-11-02", "2026-11-02", "Carla"),
    ("2026-11-02", "2026-11-02", "2026-11-03", "Carla"),
    ("2026-11-02", None, None, None),
    ("2026-11-02", "2026-11-02", "2026-11-02", "Carla"),
    ("2026-11-02", "2026-11-02", "2026-11-02", "Carla"),
    ("2026-11-03", "2026-11-04", "2026-11-05", "Carla"),
    ("2026-11-03", "2026-11-04", None, None),
    ("2026-11-03", None, None, None),
    (None, None, None, None),
    ("2026-11-04", "2026-11-04", "2026-11-04", "Carla"),
    ("2026-11-05", "2026-11-05", None, None),
    (None, None, None, None),
    ("2026-11-05", "2026-11-05", "2026-11-04", "Carla"),
    (None, None, None, None),
    (None, None, None, None),
    (None, None, None, None),
]
NT, T0 = 60, 10          # 60 tarefas, a partir da linha 10 da aba Treinamento
