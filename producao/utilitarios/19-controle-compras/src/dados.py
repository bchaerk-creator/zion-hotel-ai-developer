"""Fonte única das categorias, listas e do exemplo fictício da Ferramenta 19 (Controle de Compras e Consumo Interno)."""
# (categoria, exemplos) — o comprador ajusta. Orçamento mensal fica em branco na versão em branco.
CATEGORIAS = [
    ("Limpeza", "detergente, desinfetante, panos, sacos de lixo"),
    ("Amenities", "sabonete, xampu, papel higiênico, kits de banho"),
    ("Enxoval", "lençóis, toalhas, fronhas (reposição)"),
    ("Café e cortesias", "café, chá, água, itens de boas-vindas"),
    ("Lavanderia", "serviço terceirizado ou produtos de lavagem"),
    ("Manutenção e reparos", "lâmpadas, peças, pequenos consertos"),
    ("Consumo da equipe", "café, água e lanches da equipe"),
    ("Escritório e outros", "impressão, material de escritório, outros"),
]
PAGAMENTOS = ["Pix", "Cartão de crédito", "Cartão de débito", "Boleto", "Dinheiro", "Transferência"]
# Exemplo fictício: orçamento mensal por categoria
EX_ORC = {"Limpeza": 450, "Amenities": 600, "Enxoval": 300, "Café e cortesias": 350, "Lavanderia": 1800,
          "Manutenção e reparos": 400, "Consumo da equipe": 150, "Escritório e outros": 100}
EX_MES, EX_NOITES = "2026-11-15", 68
# (data, categoria, descrição, fornecedor, unidade, valor, pagamento, comprovante)
EX_COMPRAS = [
    ("2026-10-03", "Limpeza", "Detergente e desinfetante", "Distribuidora Norte (fictícia)", None, 186.40, "Pix", "Sim"),
    ("2026-10-05", "Amenities", "Papel higiênico (2 fardos)", "Atacado Sul (fictício)", None, 245.00, "Boleto", "Sim"),
    ("2026-10-08", "Lavanderia", "Lavanderia da 1ª quinzena", "Lavanderia Alfa (fictícia)", None, 820.00, "Pix", "Sim"),
    ("2026-10-12", "Café e cortesias", "Café em grãos e chás", "Torrefação Serra (fictícia)", None, 156.00, "Cartão de crédito", "Sim"),
    ("2026-10-20", "Manutenção e reparos", "Lâmpadas e resistência do chuveiro", "Loja de materiais (fictícia)", "Chalé 2", 132.90, "Cartão de débito", "Não"),
    ("2026-10-23", "Lavanderia", "Lavanderia da 2ª quinzena", "Lavanderia Alfa (fictícia)", None, 790.00, "Pix", "Sim"),
    ("2026-10-28", "Consumo da equipe", "Café e água da equipe", "Mercado Centro (fictício)", None, 64.50, "Dinheiro", "Não"),
    ("2026-11-02", "Limpeza", "Detergente, desinfetante e panos", "Distribuidora Norte (fictícia)", None, 214.80, "Pix", "Sim"),
    ("2026-11-03", "Amenities", "Sabonete líquido e xampu (galões)", "Distribuidora Norte (fictícia)", None, 318.00, "Pix", "Sim"),
    ("2026-11-04", "Café e cortesias", "Café em grãos", "Torrefação Serra (fictícia)", None, 234.00, "Cartão de crédito", "Sim"),
    ("2026-11-06", "Enxoval", "6 toalhas de banho (reposição)", "Loja de enxoval (fictícia)", None, 270.00, "Cartão de crédito", "Sim"),
    ("2026-11-07", "Lavanderia", "Lavanderia da 1ª quinzena", "Lavanderia Alfa (fictícia)", None, 912.00, "Pix", "Sim"),
    ("2026-11-09", "Manutenção e reparos", "Sifão e vedação da pia", "Loja de materiais (fictícia)", "Chalé 1", 88.50, "Dinheiro", "Não"),
    ("2026-11-10", "Amenities", "Papel higiênico (fardo)", "Atacado Sul (fictício)", None, 140.00, "Boleto", "Sim"),
    ("2026-11-11", "Consumo da equipe", "Lanche do treinamento", "Padaria (fictícia)", None, 96.00, "Pix", "Sim"),
    ("2026-11-12", "Café e cortesias", "Chás, água e boas-vindas", "Mercado Centro (fictício)", None, 118.70, "Cartão de débito", "Sim"),
    ("2026-11-13", "Manutenção e reparos", "Chuveiro novo", "Loja de materiais (fictícia)", "Chalé 3", 219.00, "Cartão de crédito", "Sim"),
    ("2026-11-14", "Limpeza", "Sacos de lixo e luvas", "Mercado Centro (fictício)", None, 72.30, "Cartão de débito", "Sim"),
    ("2026-11-14", "Consumo da equipe", "Café e água da equipe", "Mercado Centro (fictício)", None, 58.40, "Dinheiro", "Não"),
    ("2026-11-15", "Jardinagem", "Adubo e mudas", "Floricultura (fictícia)", None, 95.00, "Pix", "Sim"),
    (None, "Escritório e outros", "Impressão de cardápios", "Gráfica (fictícia)", None, 45.00, "Pix", "Sim"),
]
