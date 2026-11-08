"""Lista sugerida e exemplo fictício da Ferramenta 05 (Orçamento da Cabana). Todos os valores são inventados:
não servem como referência de preço."""
ETAPAS = [
    "Projeto e licenças", "Terreno e acesso", "Água, luz e esgoto", "Fundação", "Estrutura e cobertura",
    "Instalações elétricas e hidráulicas", "Acabamentos e esquadrias", "Móveis e equipamentos",
    "Enxoval, utensílios e decoração", "Abertura e lançamento",
]
EX = dict(nome="Cabana de madeira para casal (fictícia)", area=30, deck=12, reserva=10, verba=200000)
# (etapa 1-10, item, especificação, quantidade, cot1, cot2, cot3, escolhida, pago, mês)
ITENS = [
    (1, "Projeto arquitetônico", "Inclui aprovação na prefeitura", 1, 6500, 8000, 5200, 1, 6500, 1),
    (1, "Projetos complementares (estrutural, elétrico, hidráulico)", "", 1, 4800, 5500, None, None, None, 1),
    (1, "Taxas de aprovação e alvará", "Valor único da prefeitura", 1, 1800, None, None, 1, None, 2),
    (1, "Topografia e sondagem do solo", "", 1, 2200, 2600, 1900, None, 1900, 1),
    (2, "Limpeza do terreno", "", 1, 2500, 3200, None, None, 2500, 2),
    (2, "Terraplanagem", "", 1, 6000, 7500, 5800, None, None, 2),
    (2, "Acesso e estacionamento", "Cascalho", 1, 4500, None, None, None, None, 3),
    (3, "Entrada de energia", "", 1, 3800, 4200, None, None, None, 3),
    (3, "Poço ou ligação de água", "", 1, 9000, 12000, 10500, None, None, 3),
    (3, "Fossa, filtro e sumidouro", "Conforme o projeto aprovado", 1, 7200, 6800, 8100, None, None, 3),
    (3, "Caixa d'água instalada", "", 1, 1200, 1350, None, None, None, 4),
    (4, "Fundação", "Mesmo projeto estrutural para os 3", 1, 14000, 16500, 13200, 1, None, 4),
    (4, "Impermeabilização da base", "", 1, 1600, 1900, None, None, None, 4),
    (5, "Estrutura de madeira, montada (por m²)", "", 30, 1400, 1550, 1320, None, None, 5),
    (5, "Cobertura com telha e manta (por m²)", "", 42, 210, 240, None, None, None, 5),
    (5, "Deck de madeira (por m²)", "", 12, 650, 720, 600, None, None, 6),
    (6, "Instalação elétrica", "", 1, 7500, 8200, None, None, None, 6),
    (6, "Instalação hidráulica", "", 1, 6800, 7400, 6500, None, None, 6),
    (6, "Aquecedor de água instalado", "", 1, 2400, 2650, None, None, None, 6),
    (7, "Janelas e portas", "A 2 inclui instalação", 1, 13500, 15800, 12900, 2, None, 6),
    (7, "Piso (por m²)", "", 30, 120, 135, 110, None, None, 7),
    (7, "Revestimento do banheiro (por m²)", "", 8, 140, 165, None, None, None, 7),
    (7, "Louças e metais do banheiro", "", 1, 3200, 2900, 3500, None, None, 7),
    (7, "Pintura e verniz", "", 1, 4200, 3900, None, None, None, 7),
    (8, "Cama com colchão", "", 1, 3800, 4200, 3500, None, None, 8),
    (8, "Sofá ou poltronas", "", 1, 2600, 3100, None, None, None, 8),
    (8, "Armários da cozinha", "", 1, 6500, 7200, 5900, None, None, 8),
    (8, "Geladeira e cooktop", "", 1, 3400, 3700, None, None, None, 8),
    (8, "Climatização (ar ou lareira)", "", 1, 4500, None, None, None, None, 8),
    (8, "Mesa, cadeiras e criados-mudos", "", 1, 2200, 2500, None, None, None, 8),
    (9, "Jogos de cama e banho", "3 jogos completos", 3, 650, 720, 600, None, None, 9),
    (9, "Utensílios de cozinha", "", 1, 1500, 1700, None, None, None, 9),
    (9, "Decoração e iluminação", "", 1, 3500, 4000, None, None, None, 9),
    (9, "Cortinas", "", 1, None, None, None, None, None, 9),
    (10, "Fotos profissionais", "", 1, 1800, 2200, 1500, None, None, 10),
    (10, "Sinalização e placa", "", 1, 900, 1100, None, None, None, 10),
    (10, "Seguro do primeiro ano", "", 1, 1900, 2100, None, None, None, 10),
    (10, "Amenidades iniciais", "", 1, 600, 700, None, None, None, 10),
    (10, "Hidromassagem externa", "Fora desta fase", 0, 18000, None, None, None, None, None),
]
NL, L0 = 80, 12          # 80 linhas de itens, a partir da linha 12 da aba Orçamento
NMES = 12
