"""Gera o HTML do «Checklist da página 6B · antes de mostrar a conta a alguém» (2 páginas A4), no visual do e-book do Pilar 6
e da 6A (Playfair Display + Inter, paleta da Trilha 1, a caixa «Faça agora» como molde). Conteúdo: PLANO.md, seção 5.6, em sete blocos.
Sem percentual e sem preço. Aviso educativo no fim.
Saída: src/checklist/checklist.html. Depois:
  node src/render.js src/checklist/checklist.html ../../../docs/trilha1/materiais/Pilar-6B-Viabilidade-checklist.pdf --min 2 --max 2
Uso: python3 -I src/build_checklist.py"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from estilo import fontes_css, CORES, BASE, AVISO

OUT = pathlib.Path(__file__).resolve().parent / "checklist"; OUT.mkdir(exist_ok=True)


def grupo(n, titulo, itens, nota="", cls=""):
    return (f'<div class="g {cls}"><div class="gt"><span>{n}</span><h3>{titulo}</h3></div>' + (f'<p class="nota">{nota}</p>' if nota else "")
            + '<ul class="chk">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul></div>")


P1 = ('<div class="k">Trilha 1 · Pilar 6 · Aprofundamento 6B</div>'
      '<h1>Checklist da página 6B: <i>antes de mostrar a conta a alguém</i></h1>'
      '<p class="deck">Marque cada item quando ele estiver feito, por escrito. Use junto com a ficha «Faça agora · A sua conta» e com o e-book do aprofundamento 6B.</p><div class="regua"></div>'
      + grupo(1, "Receita", [
          "A diária é a <b>diária média do ano</b>, não a de alta nem a do anúncio",
          "A ocupação é a <b>soma dos doze meses dividida por 12</b>, não a média dos patamares",
          "A rampa do primeiro ano começa no <b>mês de abertura</b>",
          "Outras receitas entram por captura × ticket, cada uma com o seu custo, fora da base",
          "A taxa de limpeza cobrada à parte do hóspede ficou fora da receita de hospedagem"])
      + grupo(2, "Deduções", [
          "O imposto sobre a receita tem a <b>resposta do contador</b>, com data e nome; sem ela, a linha está em branco, com nome",
          "A comissão está separada: parte das noites vendidas pela plataforma × comissão por reserva",
          "A taxa do cartão nas vendas diretas está na conta",
          "O cancelamento e o não comparecimento estão nas deduções",
          "A comissão <b>não está também</b> nos custos de cada noite"])
      + grupo(3, "Custos", [
          "Custos de cada noite e de cada estadia separados (a estadia dividida pela estadia média)",
          "Custos de cada mês com 13º, férias, encargos, seguro, taxas e licenças <b>em duodécimos</b>",
          "Manutenção preventiva na lista",
          "O meu trabalho está na conta: horas por semana × o valor-hora que eu pagaria a alguém",
          "Cada linha tem origem: cotação, estimativa ou em branco"])
      + grupo(4, "Pergunte ao seu contador", [
          "«Qual é o regime mais adequado para o meu caso, e qual imposto incide sobre a receita de hospedagem e sobre as outras receitas, com que alíquota efetiva?»",
          "«Em que ponto do crescimento (fase dois, fase três) essa resposta muda?»",
          "«Quais encargos incidem sobre a minha retirada e sobre o salário da pessoa local?»",
          "«Imposto sobre o lucro e distribuição ao sócio: como entram?»"],
          nota="Anote a data e o nome de quem respondeu."))

P2 = (grupo(5, "Pergunte ao seu advogado, se houver", [
          "Contratos de gestão, arrendamento do terreno ou sociedade: o que cada um muda no degrau 5?"])
      + grupo(6, "Antes de decidir", [
          "A reserva de reposição está na conta (reserva ou depreciação, nunca as duas)",
          "O tempo de volta foi calculado sobre <b>o que sobra</b>, em escada, com o primeiro ano de rampa",
          "O colchão foi conferido no pior mês do primeiro ano",
          "O terreno está ao lado, com a razão escrita",
          "A taxa do meu dinheiro foi escrita <b>antes</b> de ver o resultado",
          "O critério para parar está escrito"])
      + grupo(7, "Depois da 6B", [
          "Salvei o PDF da página 6B na pasta Meu Dossiê, ao lado das páginas 6 e 6A",
          "Refiz a página 6 com a margem aberta: digitei a margem e os meses de giro do quadro «Como levar para a página 6»",
          "Preenchi a Planilha 2 · Estudo de Massas e Viabilidade pelo quadro célula a célula",
          "Levei a decisão (avançar, ajustar ou redesenhar) e o critério para parar ao Pilar 7"], cls="fim7")
      + '<div class="anot"><span class="k">Anotações · o que ainda falta perguntar, e a quem</span><div class="ln"></div><div class="ln"></div><div class="ln"></div><div class="ln"></div><div class="ln"></div><div class="ln"></div></div>'
      + f'<p class="aviso">{AVISO} Esta lista não traz preço nem percentual: os números saem da sua lista, do seu extrato e da resposta do seu contador.</p>')

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
html = (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Checklist da página 6B · Aprofundamento 6B · Viabilidade</title>'
        f"<style>{fontes_css(OUT)}{CORES}{BASE}{EXTRA}</style></head><body>{corpo}</body></html>")
texto = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
texto = re.sub(r"<[^>]+>", " ", texto)
assert "—" not in texto and "–" not in texto, "travessão"
assert "%" not in texto and "R$" not in texto and "por cento" not in texto, "o checklist não leva percentual nem preço"
for proibido in ("Helena", "Ribeirão", "Bloco", "aluno", "membro", "Ferramenta 01", "Ferramenta 10"):
    assert proibido not in texto, proibido
(OUT / "checklist.html").write_text(html, encoding="utf-8")
print("ok", OUT / "checklist.html")
