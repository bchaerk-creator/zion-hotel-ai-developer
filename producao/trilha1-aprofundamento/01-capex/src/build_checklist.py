"""Gera o HTML do «Checklist da página 6A» (2 páginas A4), no visual do e-book do Pilar 6 (Playfair Display + Inter,
paleta da Trilha 1, a caixa «Faça agora» como molde). Conteúdo: PLANO.md v2, seção 5.6, em sete blocos.
Sem percentual e sem preço. Aviso educativo no fim.
Saída: src/checklist/checklist.html. Depois:
  node src/render.js src/checklist/checklist.html ../../../docs/trilha1/materiais/Pilar-6A-CAPEX-checklist.pdf --min 2 --max 2
Uso: python3 -I src/build_checklist.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from estilo import fontes_css, CORES, BASE, AVISO

OUT = pathlib.Path(__file__).resolve().parent / "checklist"; OUT.mkdir(exist_ok=True)


def grupo(n, titulo, itens, nota="", cls=""):
    return (f'<div class="g {cls}"><div class="gt"><span>{n}</span><h3>{titulo}</h3></div>' + (f'<p class="nota">{nota}</p>' if nota else "")
            + '<ul class="chk">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul></div>")


P1 = ('<div class="k">Trilha 1 · Pilar 6 · Aprofundamento 6A</div>'
      '<h1>Checklist da página 6A: <i>antes de pedir cotação e antes de fechar o número</i></h1>'
      '<p class="deck">Marque cada item quando ele estiver feito, por escrito. Use junto com a ficha «Faça agora · O seu CAPEX» e com o e-book do aprofundamento 6A.</p><div class="regua"></div>'
      + grupo(1, "Antes de pedir cotação", [
          "<b>As perguntas do terreno:</b> distância até o ponto de energia (a concessionária informa)",
          "Água: rede, poço ou nascente; vazão; precisa de outorga?",
          "O solo pede fundação especial?",
          "Um caminhão chega até as unidades em dia de chuva?",
          "Declividade do terreno e prazo das licenças",
          "<b>O mesmo pacote para todos</b> os fornecedores: projeto, memorial e quantidades",
          "<b>A especificação escrita:</b> material, medidas, quantidade, frete, instalação, retirada de entulho, prazo e garantia",
          "Pedi a lista do que <b>não inclui</b>, por escrito"])
      + grupo(2, "Ao receber as propostas", [
          "Três propostas com a mesma especificação",
          "Data anotada em cada proposta; validade de 90 dias conferida (passou, refaço)",
          "Na estrutura pronta (bolha, domo, cabana pré-fabricada): frete, fundação e montagem confirmados por escrito",
          "Escolhi a menor só onde o escopo é igual",
          "Lancei cada linha na ficha com a origem: cotação, estimativa ou em branco"])
      + grupo(3, "Por parte, o que costuma ficar de fora", [
          "Infraestrutura comum dimensionada para o projeto completo do Pilar 5 (Parte 2)",
          "Áreas comuns e de apoio, com área e custo do metro quadrado (Parte 3)",
          "Unidade-modelo completa, item por item (Parte 4)",
          "Três jogos de roupa por cama, e o enxoval numa linha só (Parte 5)",
          "Pré-abertura: licença de funcionamento, fotos, lançamento, treinamento, seguro, abertura de teste (Parte 6)",
          "Reserva do imprevisto com a regra de uso nas quatro linhas: para quê, quem autoriza, como se registra, quando se confere (Parte 7)",
          "Capital de giro ao lado, somado no investimento total; terreno anotado à parte, sem somar"],
          nota="Era o que a página 6 deixava à parte, ou não tinha linha."))

P2 = (grupo(4, "Pergunte ao seu engenheiro, sem número", [
          "O preço inclui mão de obra, encargos, administração e lucro (BDI, benefícios e despesas indiretas)?",
          "Quanto o frete e a montagem acrescentam neste terreno?",
          "Como o preço pode mudar até a compra (reajuste)?",
          "A rede está dimensionada para quantas unidades?",
          "Quem assina a responsabilidade técnica (ART, anotação de responsabilidade técnica, ou RRT, registro de responsabilidade técnica)?"])
      + grupo(5, "Pergunte ao seu contador (e ao advogado, na forma de entrada do terreno)", [
          "Custos de aquisição do terreno: escritura, imposto de transmissão (ITBI, imposto sobre a transmissão de bens imóveis), registro, certidões",
          "Impostos sobre a obra e sobre a compra de equipamentos",
          "Compra, permuta, sociedade ou arrendamento do terreno: o que muda?"])
      + grupo(6, "Pergunte à concessionária e à prefeitura", [
          "Onde fica o ponto de energia, e qual a tensão disponível?",
          "Quais licenças o projeto precisa, e quanto custa cada uma?"])
      + grupo(7, "Depois da 6A", [
          "Salvei o PDF da página 6A na pasta Meu Dossiê, ao lado da página 6",
          "Refiz a página 6 campo a campo, com o quadro «Como levar para a página 6», <b>digitando 0 onde for zero</b> (em branco, a ficha do Pilar 6 usa a referência)",
          "Se prefiro planilha: passei as partes para a Planilha 1 · Orçamento de Abertura e conferi o Resumo, linha TOTAL",
          "Colei o CAPEX na Planilha 2 · Estudo de Massas e Viabilidade, aba Investimento, célula B5, com o terreno em zero na B6",
          "Fiz a sensibilidade do Mapa e segui para o Pilar 7"], cls="fim7")
      + '<div class="anot"><span class="k">Anotações · o que ainda falta cotar, e a quem pedir</span><div class="ln"></div><div class="ln"></div><div class="ln"></div></div>'
      + f'<p class="aviso">{AVISO} Esta lista não traz preço nem percentual: os números saem das propostas escritas.</p>')

EXTRA = """
@page{size:A4;margin:0}
.pg{width:210mm;height:297mm;padding:17mm 19mm 14mm;position:relative;break-after:page;overflow:hidden}
.pg:last-child{break-after:auto}
h1{font-size:21pt;line-height:1.16;margin:2mm 0 2.4mm;max-width:165mm}
.deck{font-family:'Playfair Display',serif;font-style:italic;font-size:10.6pt;line-height:1.5;color:var(--texto2);margin:0;max-width:160mm}
.regua{width:21mm;height:1.6px;background:var(--ouro-l);margin:4mm 0 4mm}
.g{background:var(--caixa);border:1px solid var(--bege);border-left:3px solid var(--ouro);border-radius:1.5mm;padding:3.4mm 4.6mm 2mm;margin:0 0 4mm}
.gt{display:flex;align-items:center;gap:2.6mm;margin-bottom:1.6mm}
.gt span{flex:none;width:7mm;height:7mm;border-radius:50%;background:var(--verde);color:var(--ouro);font-family:'Playfair Display',serif;font-size:11pt;display:flex;align-items:center;justify-content:center}
.gt h3{font-size:14pt;margin:0}
.nota{font-size:7.6pt;color:var(--texto2);margin:-.6mm 0 1.4mm 9.6mm}
.chk{list-style:none;padding-left:0;margin:0}
.chk li{position:relative;padding-left:6.4mm;margin-bottom:1.9mm;font-size:9.3pt;line-height:1.45}
.chk li:before{content:"";position:absolute;left:0;top:.5mm;width:3.4mm;height:3.4mm;border:1.2px solid var(--verde);border-radius:.7mm;background:#fff}
.fim7{background:var(--escuro);border-color:var(--escuro);color:#fff}
.fim7 .gt span{background:var(--ouro);color:var(--verde)} .fim7 h3{color:#fff}
.fim7 .chk li{color:#F2EFE6} .fim7 .chk li:before{border-color:var(--ouro);background:transparent}
.anot{border:1px dashed var(--ouro-p);border-radius:1.5mm;padding:3mm 4.4mm 1mm;margin-top:1mm}
.anot .k{display:block;margin-bottom:1mm}
.ln{border-bottom:1px solid var(--linha2);height:8.5mm}
.aviso{font-size:7.2pt;line-height:1.5;color:var(--texto2);border-top:1px solid var(--linha2);padding-top:2.6mm;margin-top:4mm}
"""
corpo = "".join(f'<section class="pg">{c}</section>\n' for c in (P1, P2))
html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Checklist da página 6A · Aprofundamento 6A · CAPEX</title>'
        f"<style>{fontes_css(OUT)}{CORES}{BASE}{EXTRA}</style></head><body>{corpo}</body></html>")
texto = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
texto = re.sub(r"<[^>]+>", " ", texto)
assert "—" not in texto and "–" not in texto, "travessão"
assert "%" not in texto and "R$" not in texto, "o checklist não leva percentual nem preço"
for proibido in ("Helena", "Ribeirão", "Bloco", "aluno", "membro", "Ferramenta 05", "Calculadora de Implantação"):
    assert proibido not in texto, proibido
(OUT / "checklist.html").write_text(html, encoding="utf-8")
print("ok", OUT / "checklist.html")
