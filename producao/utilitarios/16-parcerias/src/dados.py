"""Fonte única das listas e do exemplo fictício da Ferramenta 16 (Kit Operacional de Parcerias)."""
TIPOS = ["Restaurante", "Café ou padaria", "Guia ou passeio", "Spa ou bem-estar", "Transporte", "Loja ou produtor local", "Outro"]
CONTRA = ["% sobre o valor", "Valor fixo por indicação", "Troca ou cortesia", "Nenhuma"]
SIM_NAO = ["Sim", "Não"]
EX_HOJE = "2026-11-20"
# (parceiro, tipo, contato, o que oferece, benefício ao hóspede, contrapartida, valor, acordo escrito, revisar em)
EX_PARC = [
    ("Restaurante Sabor da Serra (fictício)", "Restaurante", "(00) 90000-0001", "Jantar com menu regional", "Sobremesa como cortesia", "% sobre o valor", 0.10, "Sim", "2027-03-01"),
    ("Trilhas do Vale (fictício)", "Guia ou passeio", "(00) 90000-0002", "Trilha guiada de meio dia", "10% de desconto", "Valor fixo por indicação", 25, "Sim", "2026-11-15"),
    ("Spa Bem-Estar (fictício)", "Spa ou bem-estar", "(00) 90000-0003", "Massagem relaxante", "Horário prioritário", "% sobre o valor", 0.15, "Não", None),
    ("Transfer Rápido (fictício)", "Transporte", "(00) 90000-0004", "Transfer do aeroporto", "Água e mapa da região", "Troca ou cortesia", None, "Sim", "2027-01-10"),
    ("Café da Praça (fictício)", "Café ou padaria", "(00) 90000-0005", "Café colonial", "Brinde de boas-vindas", "Nenhuma", None, "Sim", None),
]
# (data, parceiro, código da reserva, valor gasto, confirmada, recebido)
EX_IND = [
    ("2026-11-02", "Restaurante Sabor da Serra (fictício)", "R1023", 380, "Sim", "Sim"),
    ("2026-11-05", "Restaurante Sabor da Serra (fictício)", "R1027", 260, "Sim", "Não"),
    ("2026-11-08", "Trilhas do Vale (fictício)", "R1027", None, "Sim", "Não"),
    ("2026-11-09", "Trilhas do Vale (fictício)", "R1031", None, "Não", None),
    ("2026-11-10", "Spa Bem-Estar (fictício)", "R1031", 300, "Sim", "Não"),
    ("2026-11-12", "Transfer Rápido (fictício)", "R1035", None, "Sim", None),
    ("2026-11-14", "Restaurante Sabor da Serra (fictício)", "R1038", None, "Não", None),
    ("2026-11-15", "Pizzaria Nova (fictícia)", "R1040", 120, "Sim", None),
    ("2026-11-16", "Café da Praça (fictício)", "R1041", None, "Sim", None),
    ("2026-11-18", "Trilhas do Vale (fictício)", "R1042", None, "Sim", "Sim"),
]
