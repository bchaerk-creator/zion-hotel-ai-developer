"""Fonte única das listas e do exemplo fictício da Ferramenta 22 (Planner de Campanhas para Períodos de Baixa Procura)."""
TIPOS = ["Estadia longa", "Última hora", "Pacote com experiência", "Público da região", "Data ou tema especial", "Hóspedes que já vieram", "Outro"]
CANAIS = ["Plataforma de reservas", "Instagram", "WhatsApp", "E-mail", "Parceiros locais", "Outro"]
SITUACOES = ["Ideia", "Preparando", "No ar", "Encerrada"]
# Base do exemplo: unidades, diária normal, piso, taxas e impostos (fração), custo variável por estadia, meta de ocupação (fração)
EX_BASE = dict(unidades=3, diaria=420, piso=300, taxa=0.18, custo=120, meta=0.5)
# Períodos: (nome, início, último dia, noites já reservadas)
EX_PER = [("Março depois do Carnaval", "2027-03-08", "2027-03-25", 12),
          ("Semanas de abril", "2027-04-05", "2027-04-16", 20),
          ("Maio, dias úteis", "2027-05-03", "2027-05-28", 25),
          ("Começo de junho", "2027-06-01", "2027-06-10", 6)]
# Campanhas: (período, tipo, desconto, estadia mínima, canal, começa, termina, responsável, situação, noites vendidas)
EX_CAMP = [("Março depois do Carnaval", "Estadia longa", 0.15, 3, "Plataforma de reservas", "2027-02-15", "2027-03-25", "Ana (fictícia)", "Preparando", None),
           ("Março depois do Carnaval", "Público da região", 0.10, 2, "Instagram", "2027-02-20", "2027-03-20", "Ana (fictícia)", "Ideia", None),
           ("Maio, dias úteis", "Última hora", 0.35, 1, "Plataforma de reservas", "2027-04-26", "2027-05-28", "Ana (fictícia)", "Ideia", None),
           ("Maio, dias úteis", "Pacote com experiência", 0, 2, "WhatsApp", "2027-04-10", "2027-05-28", "Rui (fictício)", "No ar", 8),
           ("Semanas de abril", "Data ou tema especial", 0.05, 2, "E-mail", "2027-04-20", "2027-04-30", "Rui (fictício)", "Ideia", None),
           ("Maio, dias úteis", "Hóspedes que já vieram", 0.10, 2, "E-mail", "2027-04-15", "2027-05-28", "Rui (fictício)", "No ar", 6)]
