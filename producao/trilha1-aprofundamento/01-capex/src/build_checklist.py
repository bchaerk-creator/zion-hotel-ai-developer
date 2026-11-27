"""Gera o HTML do "Checklist do CAPEX" (2 páginas A4): antes de pedir cotação, ao receber cotações e antes de fechar o número,
com as perguntas para engenheiro, arquiteto, contador, concessionária e prefeitura. Sem percentual e sem preço (PLANO.md 5.5).
Saída: src/checklist/checklist.html. Depois: node src/render.js src/checklist/checklist.html docs/trilha1/materiais/CAPEX-Checklist.pdf
Uso: python3 -I src/build_checklist.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from estilo import css, rel, BRAND, RODAPE

OUT = pathlib.Path(__file__).resolve().parent / "checklist"; OUT.mkdir(exist_ok=True)
logo = rel(BRAND / "zion-logo-escuro.png", OUT)


def grupo(titulo, itens, nota=""):
    return (f'<div class="g"><h3>{titulo}</h3>' + (f'<p class="nota">{nota}</p>' if nota else "")
            + '<ul class="chk">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul></div>")


P1 = (f'<div class="topo"><img src="{logo}" alt="Zion Hotel Group"><div class="k">Trilha 1 · Pilar 6 · Aprofundamento · CAPEX</div></div>'
      '<h2>Checklist <i>do CAPEX</i></h2><p class="lead">Antes de pedir cotação, ao receber as propostas e antes de fechar o número. Marque cada item quando ele estiver feito, por escrito.</p>'
      '<div class="etapa"><span>1</span>Antes de pedir cotação</div>'
      + grupo("As perguntas do terreno", [
          "Distância até o ponto de energia e tipo de rede (a concessionária informa)",
          "Água: rede, poço ou nascente; vazão; precisa de outorga?",
          "O solo pede fundação especial?",
          "Um caminhão chega até as unidades em dia de chuva?",
          "Declividade do terreno",
          "Prazo das licenças"])
      + grupo("O pacote e a especificação", [
          "O mesmo pacote para todos os fornecedores: projeto, memorial descritivo e quantidades",
          "Especificação escrita: material, medidas, quantidade, frete, instalação, retirada de entulho, prazo e garantia",
          "Pedido de orçamento aberto por etapa, e não só o valor fechado",
          "Pedido da lista do que <b>não inclui</b>, por escrito",
          "Rede pensada para o projeto completo: escrevi para quantas unidades ela será dimensionada"])
      + '<div class="etapa"><span>2</span>Ao receber as cotações</div>'
      + grupo("Antes de comparar", [
          "Três propostas com a mesma especificação",
          "Cada proposta traz a lista do que não inclui",
          "Data anotada em cada proposta; as que passaram de 90 dias foram refeitas",
          "Estrutura pronta (bolha, domo, cabana pré-fabricada): frete, fundação e montagem confirmados por escrito",
          "Escolhi a menor só onde o escopo é igual",
          "Lancei cada proposta na ficha, com a origem: cotação, estimativa ou em branco"])
      + '<div class="box linha" style="margin-top:4mm"><span class="k">Anotações · o que ainda falta cotar e a quem pedir</span><div class="campo"></div><div class="campo"></div></div>')

P2 = ('<div class="etapa" style="margin-top:0"><span>3</span>Antes de fechar o número</div>'
      + grupo("O que costuma ficar de fora", [
          "Áreas comuns e de apoio (lavanderia, recepção, cozinha, deck comum, trilhas, casa de máquinas)",
          "Infraestrutura dimensionada para o projeto completo, com as ligações de cada unidade da fase",
          "Unidade-modelo completa no mobiliário",
          "Três jogos de roupa por cama no enxoval",
          "Pré-abertura: licença de funcionamento, fotos e site, lançamento, treinamento, seguro do primeiro ano, abertura de teste",
          "Reserva do imprevisto maior que zero, com a regra de uso nas quatro linhas: para quê, quem autoriza, como se registra, quando se confere",
          "Capital de giro à parte, somado no investimento total",
          "Terreno anotado ao lado, com valor e forma de entrada, sem somar",
          "Cada item numa linha só: o enxoval não está também na cotação do mobiliário",
          "Linhas sem número ficaram em branco, com nome, e não com um valor inventado"])
      + '<div class="cols">'
      + grupo("Pergunte ao engenheiro", [
          "O preço inclui mão de obra, encargos, administração e lucro (BDI, benefícios e despesas indiretas)?",
          "Quanto o frete e a montagem acrescentam neste terreno?",
          "Como o preço pode mudar até a compra (reajuste)?",
          "A rede está dimensionada para quantas unidades?",
          "Quem assina a responsabilidade técnica (ART, anotação de responsabilidade técnica)?"])
      + grupo("Pergunte ao arquiteto", [
          "Quais projetos a prefeitura vai pedir, e em que ordem?",
          "O memorial descritivo está pronto para pedir três cotações comparáveis?",
          "Quem assina o registro de responsabilidade técnica (RRT)?"])
      + grupo("Pergunte ao contador (e ao advogado, na entrada do terreno)", [
          "Custos de aquisição do terreno: escritura, imposto de transmissão (ITBI), registro, certidões",
          "Impostos sobre a obra e a compra de equipamentos",
          "Compra, permuta, sociedade ou arrendamento do terreno: o que muda?"])
      + grupo("Pergunte à concessionária e à prefeitura", [
          "Onde fica o ponto de energia e qual a tensão disponível?",
          "Quais licenças o projeto precisa, quanto custam e quanto tempo levam?"])
      + "</div>"
      + '<div class="box escuro" style="margin-top:3mm"><span class="k">Depois do checklist</span><p style="margin:0">Atualize a ficha <b>Faça agora · O meu CAPEX</b>, baixe a página 6A de novo e leve os números para a página 6 do Pilar 6.</p></div>')

EXTRA = """
.topo{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--areia);padding-bottom:3mm;margin-bottom:4mm}
.topo img{height:9mm}
h2{font-size:30pt}
.etapa{display:flex;align-items:center;gap:3mm;background:var(--musgo);color:var(--creme);font-family:Titulo,serif;font-size:16pt;padding:2mm 4mm;border-radius:2mm;margin:4mm 0 2mm}
.etapa span{display:inline-flex;width:8mm;height:8mm;border-radius:50%;background:var(--ouro);color:var(--musgo);align-items:center;justify-content:center;font-size:13pt;font-weight:700}
.g h3{font-size:13pt;margin:2.5mm 0 1.2mm;color:var(--terra)}
.chk{margin:0 0 1mm} .chk li{margin-bottom:1.2mm;font-size:10pt}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:0 7mm}
.cols .chk li{font-size:9.3pt}
.nota{font-size:9pt;color:var(--cinza)}
"""
corpo = ""
for i, c in enumerate([P1, P2], 1):
    corpo += f'<section class="pg"><div class="in">{c}</div><div class="rod"><span>{RODAPE}</span><span class="p">Checklist do CAPEX · {i}/2</span></div></section>\n'
html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Checklist do CAPEX · Trilha 1 · Pilar 6</title><style>{css(OUT)}{EXTRA}</style></head><body>{corpo}</body></html>')
texto = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
texto = re.sub(r"<[^>]+>", " ", texto)
assert "—" not in texto and " – " not in texto, "travessão"
assert "%" not in texto and "R$" not in texto, "o checklist não leva percentual nem preço"
(OUT / "checklist.html").write_text(html, encoding="utf-8")
print("ok", OUT / "checklist.html")
