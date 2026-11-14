"""Fonte única das listas e do exemplo fictício da Ferramenta 12 (Checklist de Fotos e Comodidades do Anúncio)."""
SIM_NAO = ["Sim", "Não"]
STATUS = ["Falta tirar", "Tirada", "Aprovada", "Publicada"]
# Lista de fotos sugerida: (ambiente, o que mostrar, obrigatória)
FOTOS = [
    ("Capa", "A melhor vista do lugar, de dia, com luz natural", "Sim"),
    ("Capa", "Fachada ou entrada, mostrando como é chegar", "Sim"),
    ("Sala", "Sala inteira, do canto, mostrando o espaço", "Sim"),
    ("Sala", "Detalhe que diferencia (lareira, vista, sofá)", "Não"),
    ("Cozinha", "Cozinha inteira, bancada limpa", "Sim"),
    ("Cozinha", "Utensílios e eletros principais", "Não"),
    ("Quarto 1", "Cama arrumada, do canto do quarto", "Sim"),
    ("Quarto 1", "Armário ou espaço para malas", "Não"),
    ("Quarto 2", "Cama arrumada, do canto do quarto", "Não"),
    ("Banheiro", "Banheiro inteiro, toalhas dobradas", "Sim"),
    ("Banheiro", "Chuveiro ou banheira", "Não"),
    ("Área externa", "Área externa, deck, varanda ou jardim", "Sim"),
    ("Área externa", "Churrasqueira, piscina ou hidro (se houver)", "Não"),
    ("Comodidades", "Mesa de trabalho e Wi-Fi (se anunciar)", "Não"),
    ("Comodidades", "Vaga de estacionamento (se anunciar)", "Não"),
    ("Entorno", "Vista ou paisagem ao redor", "Não"),
    ("Entorno", "Caminho de acesso, se for de terra ou subida", "Não"),
    ("Noite", "O lugar com as luzes acesas", "Não"),
]
# Comodidades: (comodidade, categoria, precisa de foto?)
COMODIDADES = [
    ("Wi-Fi", "Essenciais", "Não"), ("Roupa de cama", "Essenciais", "Não"), ("Toalhas", "Essenciais", "Não"),
    ("Itens básicos de banho", "Essenciais", "Não"), ("Água quente", "Essenciais", "Não"), ("Ar-condicionado", "Conforto", "Sim"),
    ("Aquecedor", "Conforto", "Sim"), ("Ventilador", "Conforto", "Não"), ("TV", "Conforto", "Sim"),
    ("Cozinha completa", "Cozinha", "Sim"), ("Geladeira", "Cozinha", "Não"), ("Micro-ondas", "Cozinha", "Não"),
    ("Cafeteira", "Cozinha", "Não"), ("Utensílios de cozinha", "Cozinha", "Não"), ("Máquina de lavar", "Serviços", "Não"),
    ("Ferro de passar", "Serviços", "Não"), ("Secador de cabelo", "Serviços", "Não"), ("Mesa de trabalho", "Trabalho", "Sim"),
    ("Estacionamento gratuito", "Lazer e acesso", "Sim"), ("Churrasqueira", "Lazer e acesso", "Sim"), ("Piscina", "Lazer e acesso", "Sim"),
    ("Banheira ou hidromassagem", "Lazer e acesso", "Sim"), ("Lareira", "Lazer e acesso", "Sim"), ("Varanda ou deck", "Lazer e acesso", "Sim"),
    ("Aceita animais", "Regras", "Não"), ("Entrada autônoma", "Regras", "Não"), ("Detector de fumaça", "Segurança", "Não"),
    ("Extintor de incêndio", "Segurança", "Não"), ("Kit de primeiros socorros", "Segurança", "Não"),
]
# Exemplo fictício (chalé). Fotos: índice -> (situação, ordem)
EX_FOTOS = {0: ("Publicada", 1), 1: ("Publicada", 2), 2: ("Aprovada", 3), 3: ("Tirada", None), 4: ("Aprovada", 4), 5: ("Falta tirar", None),
            6: ("Publicada", 5), 7: ("Falta tirar", None), 9: ("Tirada", 6), 10: ("Aprovada", 6), 11: ("Falta tirar", None),
            12: ("Aprovada", 7), 15: ("Publicada", 8), 17: ("Tirada", None)}
EX_FOTOS_EXCLUIR = {8, 13, 14, 16}   # o chalé não tem quarto 2, mesa de trabalho, vaga anunciada nem acesso de terra: linhas apagadas
# Comodidades: nome -> (existe, marcada, tem foto)
EX_COM = {"Wi-Fi": ("Sim", "Sim", "Não"), "Roupa de cama": ("Sim", "Sim", "Não"), "Toalhas": ("Sim", "Sim", "Não"),
          "Itens básicos de banho": ("Sim", "Sim", "Não"), "Água quente": ("Sim", "Sim", "Não"), "Ar-condicionado": ("Não", "Sim", "Não"),
          "Aquecedor": ("Sim", "Sim", "Não"), "Ventilador": ("Sim", "Não", "Não"), "TV": ("Sim", "Sim", "Sim"),
          "Cozinha completa": ("Sim", "Sim", "Sim"), "Geladeira": ("Sim", "Sim", "Não"), "Micro-ondas": ("Sim", "Sim", "Não"),
          "Cafeteira": ("Sim", "Não", "Não"), "Utensílios de cozinha": ("Sim", "Sim", "Sim"), "Máquina de lavar": ("Não", "Não", "Não"),
          "Ferro de passar": ("Não", "Não", "Não"), "Secador de cabelo": ("Sim", "Sim", "Não"), "Mesa de trabalho": ("Não", "Não", "Não"),
          "Estacionamento gratuito": ("Sim", "Sim", "Não"), "Churrasqueira": ("Sim", "Sim", "Sim"), "Piscina": ("Não", "Não", "Não"),
          "Banheira ou hidromassagem": ("Sim", "Sim", "Sim"), "Lareira": ("Sim", "Sim", "Não"), "Varanda ou deck": ("Sim", "Sim", "Sim"),
          "Aceita animais": ("Não", "Não", "Não"), "Entrada autônoma": ("Sim", "Sim", "Não"), "Detector de fumaça": ("Sim", "Não", "Não"),
          "Extintor de incêndio": ("Sim", "Sim", "Não"), "Kit de primeiros socorros": (None, None, None)}
