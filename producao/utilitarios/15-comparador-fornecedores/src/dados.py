"""Fonte única dos critérios, listas e do exemplo fictício da Ferramenta 15 (Comparador de Fornecedores)."""
# (critério, o que mede, peso padrão 0 a 5). Preço e prazo são calculados; os outros quatro são notas de 1 a 5.
CRITERIOS = [
    ("Preço", "Custo por unidade comparável (calculado pela planilha)", 5),
    ("Prazo de entrega", "Dias entre o pedido e a entrega (calculado pela planilha)", 3),
    ("Qualidade", "O produto ou serviço atende à especificação? (nota 1 a 5)", 4),
    ("Atendimento", "Responde rápido e resolve problemas? (nota 1 a 5)", 3),
    ("Condições de pagamento", "Prazo para pagar, Pix, boleto, nota fiscal (nota 1 a 5)", 2),
    ("Confiabilidade", "Entrega no dia combinado, sem faltar item? (nota 1 a 5)", 4),
]
UNIDADES = ["kg", "L", "rolo", "peça", "unidade", "pacote", "serviço", "mês"]
SUGESTOES = ["Lavanderia de enxoval", "Produtos de limpeza", "Papel higiênico e papel toalha", "Amenities (sabonete, xampu)",
             "Café e itens do café da manhã", "Gás", "Manutenção da piscina ou hidromassagem", "Jardinagem", "Dedetização", "Internet"]
# Exemplo fictício: (necessidade, unidade comparável, consumo por mês, especificação)
EX_NEC = [
    ("Lavanderia de enxoval", "kg", 320, "Lavar, secar e passar; coleta duas vezes por semana"),
    ("Detergente multiuso", "L", 12, "Concentrado, uso geral"),
    ("Papel higiênico folha dupla", "rolo", 240, "Folha dupla, 30 m"),
    ("Sabonete líquido", "L", 8, "Neutro, para refil"),
    ("Café em grãos", "kg", 6, "Torra média"),
]
# (necessidade, fornecedor, embalagem, qtd na embalagem, preço da embalagem, frete por pedido, pedido mínimo, prazo, qualidade, atendimento, pagamento, confiabilidade)
EX_COT = [
    ("Lavanderia de enxoval", "Lavanderia Alfa (fictícia)", "kg lavado", 1, 9.5, None, 20, 2, 4, 4, 4, 3),
    ("Lavanderia de enxoval", "Lavanderia Beta (fictícia)", "kg lavado", 1, 8.2, 60, 30, 3, 3, 3, 3, 3),
    ("Lavanderia de enxoval", "Lavanderia Gama (fictícia)", "kg lavado", 1, 10.9, None, 15, 1, 5, 5, 4, 5),
    ("Detergente multiuso", "Distribuidora Norte (fictícia)", "galão 5 L", 5, 42, 25, 4, 5, 4, 3, 4, 4),
    ("Detergente multiuso", "Mercado Centro (fictício)", "frasco 1 L", 1, 11.9, None, None, 0, 3, 3, 5, 4),
    ("Detergente multiuso", "Atacado Sul (fictício)", "galão 5 L", 5, 36.5, 35, 6, 7, 4, 2, 3, 3),
    ("Papel higiênico folha dupla", "Atacado Sul (fictício)", "fardo 64 rolos", 64, 105, 35, 2, 7, 4, 3, 3, 3),
    ("Papel higiênico folha dupla", "Distribuidora Norte (fictícia)", "fardo 64 rolos", 64, 119, None, 1, 3, 4, 4, 4, 4),
    ("Papel higiênico folha dupla", "Mercado Centro (fictício)", "pacote 12 rolos", 12, 26.9, None, None, 0, 4, 3, 5, 4),
    ("Sabonete líquido", "Distribuidora Norte (fictícia)", "galão 5 L", 5, 48, 25, 2, 5, 4, 4, 4, 4),
    ("Sabonete líquido", "Fornecedor Leste (fictício)", "galão 5 L", 5, 39, None, 1, 10, 3, 2, None, 3),
    ("Sabonete líquido", "Atacado Sul (fictício)", "galão 5 L", 5, 41, 35, 2, 7, 7, 3, 3, 3),
    ("Café em grãos", "Torrefação Serra (fictícia)", "pacote 1 kg", 1, 78, None, 3, 4, 5, 5, 4, 5),
    ("Café em grãos", "Mercado Centro (fictício)", "pacote 500 g", 0.5, 34.9, None, None, 0, 3, 3, 5, 4),
]
