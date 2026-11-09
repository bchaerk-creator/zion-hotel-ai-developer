"""Lista sugerida e exemplo fictício da Ferramenta 18 (Planner de Manutenção Preventiva).
As frequências são sugestões de partida: o comprador ajusta à orientação do fabricante e do profissional responsável."""
FREQ = [("Diária", 1), ("Semanal", 7), ("Quinzenal", 15), ("Mensal", 30), ("Bimestral", 60),
        ("Trimestral", 90), ("Semestral", 180), ("Anual", 365)]
# (área, tarefa, frequência sugerida). As 8 primeiras partem da ronda diária usada nas unidades da Zion (Manual Técnico).
SUGERIDAS = [
    ("Hidromassagem", "Conferir nível da água, jatos e bomba", "Diária"),
    ("Hidromassagem", "Medir pH e cloro (registrar os valores)", "Diária"),
    ("Água quente", "Testar o aquecimento da água", "Diária"),
    ("Climatização", "Ligar e testar o ar-condicionado", "Diária"),
    ("Elétrica", "Conferir lâmpadas internas e externas", "Diária"),
    ("Hidráulica", "Conferir bombas e pressão da água", "Diária"),
    ("Estrutura", "Olhar o deck ou a varanda: tábuas, parafusos, limpeza", "Diária"),
    ("Área externa", "Jardinagem e organização", "Semanal"),
    ("Climatização", "Limpar o filtro do ar-condicionado", "Mensal"),
    ("Segurança", "Testar detector de fumaça e trocar pilha se preciso", "Mensal"),
    ("Segurança", "Conferir extintor: lacre, manômetro e validade", "Mensal"),
    ("Gás", "Conferir mangueira, registro e validade do regulador", "Trimestral"),
    ("Hidráulica", "Limpar ralos, sifões e arejadores", "Mensal"),
    ("Banheiro", "Conferir rejunte e silicone do box e da pia", "Trimestral"),
    ("Portas e janelas", "Lubrificar fechaduras, dobradiças e trilhos", "Trimestral"),
    ("Cobertura", "Limpar calhas e conferir telhas", "Semestral"),
    ("Hidráulica", "Limpar a caixa d'água (com profissional ou orientação)", "Semestral"),
    ("Pragas", "Controle de pragas com empresa responsável", "Semestral"),
    ("Quarto", "Virar ou girar os colchões", "Trimestral"),
    ("Estrutura", "Verniz ou tratamento da madeira externa", "Anual"),
    ("Elétrica", "Revisão do quadro elétrico por eletricista", "Anual"),
]
EX_HOJE = "2026-11-15"
EX_AVISO = 7
# (unidade, área, tarefa, frequência, dias personalizados, responsável, última vez (antes de começar), custo por vez)
EX_PLANO = [
    ("Chalé 1", "Hidromassagem", "Medir pH e cloro (registrar os valores)", "Diária", None, "Ana", "2026-11-14", None),
    ("Chalé 1", "Climatização", "Limpar o filtro do ar-condicionado", "Mensal", None, "Ana", "2026-10-10", None),
    ("Chalé 2", "Climatização", "Limpar o filtro do ar-condicionado", "Mensal", None, "Ana", "2026-10-28", None),
    ("Chalé 1", "Segurança", "Testar detector de fumaça e trocar pilha se preciso", "Mensal", None, "Ana", "2026-10-20", 12),
    ("Chalé 2", "Segurança", "Testar detector de fumaça e trocar pilha se preciso", "Mensal", None, "Ana", None, 12),
    ("Área comum", "Segurança", "Conferir extintor: lacre, manômetro e validade", "Mensal", None, "Carlos", "2026-11-01", None),
    ("Área comum", "Gás", "Conferir mangueira, registro e validade do regulador", "Trimestral", None, "Carlos", "2026-08-10", None),
    ("Chalé 1", "Banheiro", "Conferir rejunte e silicone do box e da pia", "Trimestral", None, "Carlos", "2026-09-05", 60),
    ("Chalé 2", "Banheiro", "Conferir rejunte e silicone do box e da pia", "Trimestral", None, "Carlos", "2026-10-01", 60),
    ("Área comum", "Cobertura", "Limpar calhas e conferir telhas", "Semestral", None, "Prestador", "2026-05-20", 350),
    ("Área comum", "Hidráulica", "Limpar a caixa d'água", "Semestral", None, "Prestador", "2026-06-10", 400),
    ("Área comum", "Pragas", "Controle de pragas com empresa responsável", "Semestral", None, "Prestador", "2026-07-01", 480),
    ("Chalé 1", "Quarto", "Virar ou girar os colchões", "Trimestral", None, "Ana", "2026-08-30", None),
    ("Chalé 2", "Estrutura", "Verniz do deck", "Anual", None, "Prestador", "2025-12-15", 900),
    ("Área comum", "Elétrica", "Revisão do quadro elétrico por eletricista", "Anual", None, "Prestador", "2026-03-01", 300),
    ("Área comum", "Hidráulica", "Trocar o refil do filtro de água", "", 120, "Carlos", "2026-07-25", 85),
]
# Registro do exemplo: (data, nº da tarefa, feito por, observação)
EX_REG = [
    ("2026-11-15", 1, "Ana", "pH 7,4 · cloro ok"),
    ("2026-11-12", 3, "Ana", "Filtro lavado"),
    ("2026-11-02", 9, "Carlos", "Silicone refeito na pia"),
    ("2026-11-10", 13, "Ana", "Colchões girados"),
    ("2026-11-05", 99, "Carlos", "Nº digitado errado (exemplo de conferência)"),
]
NP, P0 = 120, 8          # 120 tarefas, a partir da linha 8 da aba Plano
NR, R0 = 400, 5          # 400 registros, a partir da linha 5 da aba Registro
