# -*- coding: utf-8 -*-
"""ZG-RFQ-002 · LISTA DE FORNECEDORES PARA COTAÇÃO · Florianópolis e região (SC).
Lista de prospecção montada por pesquisa na web (setembro de 2026): serralherias / estruturas metálicas e calandra (lote 2),
galvanização a fogo, lonas / toldos / tendas / tensoestruturas (lote 3), vidraçarias e esquadrias (lote 3), matéria-prima.
Nenhum fornecedor foi contatado; capacidade, contatos e preços a confirmar. Sem preços. Saída: 06_LOTES/ZG-RFQ-002_Fornecedores_SC.html/.md"""
import os, html
from build_tecnico import CSS as BASE_CSS
from svgkit import zion_mark_html, zion_logo_html

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_DIR = os.path.join(ROOT, "06_LOTES"); os.makedirs(OUT_DIR, exist_ok=True)
DOC = "ZG-RFQ-002"; REV = "REV 00 — PROSPECÇÃO"; DATE = "18/09/2026"
def esc(s): return html.escape(str(s))

# (empresa, cidade, o que faz / por que interessa, site ou fonte, lote, prioridade)
SERRALHERIAS = [
    ("Serralheria SJ", "São José", "Estruturas metálicas; atende Florianópolis, Palhoça, São José e Biguaçu. Perfil de serralheria de estruturas: primeira rodada para os arcos, luvas e chapas.", "serralheriasj.com.br", "2", "A"),
    ("JD Serralheria", "Grande Florianópolis (Florianópolis, São José, Palhoça)", "Estruturas metálicas com vigas W / I, treliças, tubos metálicos, mezaninos. Porte para fabricar a grelha do piso (lote 1) e a estrutura (lote 2).", "jdserralheria.com.br", "1 · 2", "A"),
    ("Stillo Serralheria", "Palhoça / Florianópolis", "Serralheria e estruturas metálicas.", "stilloserralheria.com", "2", "B"),
    ("Lotus Estruturas Metálicas e Serralheria", "Florianópolis", "Estruturas metálicas, coberturas, escadas, portões; serralheria de projeto.", "lotusmetalica.com.br", "2", "B"),
    ("Metalporto Metalúrgica", "Palhoça (desde 1998)", "Corte, dobra, torno e solda; comércio de chapas. Indicada para chapas de base, luvas, talões e cabeçotes (peças de chapa do lote 1 e 2), em paralelo à serralheria dos tubos.", "metalportometalurgica.com.br", "1 · 2", "A"),
    ("Metalgalvano Estruturas Metálicas", "Araquari (BR-280, km 26) · 170 km de Florianópolis", "Projeto, fabricação e montagem de estruturas metálicas com galvanização a fogo própria, pintura a pó, jateamento e corte CNC. Um só fornecedor para ferro + galvanização: candidato natural para a série (10 a 100 unidades).", "metalgalvano.com.br", "2", "A"),
    ("RC Serralheria Ferro e Inox", "Grande Florianópolis", "35 anos de serralheria em ferro e inox (listagem Guia Fácil). Confirmar porte e calandra.", "guiafacil.com (Serralherias · Florianópolis)", "2", "C"),
    ("Serralheria Lucas", "São José", "Estruturas metálicas, portões, escadas (listagem). Confirmar porte.", "guiafacil.com (Serralherias · Florianópolis)", "2", "C"),
    ("Guild Industrial", "Florianópolis", "Corte a laser, dobra de chapas e perfis, projetos especiais. Alternativa para chapas e conectores de precisão.", "guildindustrial.com.br", "2", "B"),
]
CALANDRA = [
    ("RPS Indústrias", "Sorocaba / SP · atende Santa Catarina", "Serviço de calandragem de tubos e perfis (inclusive perfis W). Opção se nenhuma serralheria local tiver calandra de tubos Ø60,3 com raio variável: calandrar em SP e soldar / montar em SC.", "rpsindustrias.com.br", "2", "B"),
    ("Caldeiraria da Gama", "São Paulo / SP", "Calandragem de tubos, fabricação de curvas em tubo. Referência de serviço de calandra terceirizado.", "caldeirariadagama.com.br", "2", "C"),
]
GALVANIZACAO = [
    ("Galvanização Raitz", "Joinville", "Galvanização a fogo desde 1989, zinco SHG 99,995 %, ISO 9001:2015. Galvanizador de referência em SC para as peças do lote 1 e 2 (arcos, grelha, estacas).", "galvanizacaoraitz.com.br", "1 · 2", "A"),
    ("Brazinc", "Araucária / PR · atende Joinville, Florianópolis, Blumenau, Itajaí, São José, Palhoça", "Galvanização a fogo e zincagem de tubos e estruturas, com logística para SC.", "brazinc.com.br", "1 · 2", "B"),
    ("Metalgalvano", "Araquari", "Galvanização própria (ver serralherias).", "metalgalvano.com.br", "2", "A"),
]
TUBOS = [
    ("Quality Tubos", "Florianópolis / SC (distribuidor desde 2010)", "Tubos e conexões galvanizadas; um dos maiores distribuidores do Brasil. Fornece o tubo Ø60,3 / Ø48,3 / Ø114,3 e perfis U ao serralheiro.", "qualitytubos.com.br", "1 · 2", "B"),
    ("VTK Tubos", "atende Florianópolis", "Tubos de aço galvanizado (distribuição).", "vtktubos.com.br", "2", "C"),
    ("Golin Tubos", "Santa Catarina", "Tubos de aço quadrado, retangular e redondo, industrial e galvanizado; peças e serviços.", "golin.com.br", "2", "C"),
]
LONAS_LOCAL = [
    ("SC Lonas", "Grande Florianópolis (desde 2009)", "Toldos e coberturas sob medida; fabrica tendas piramidais 5 x 5, 6 x 6 e 10 x 10 em lona. Perfil de confeccionista com corte e solda de lona: candidata à lona externa e ao forro (com padrões DXF da Zion).", "sclonas.com.br · @_sclonas", "3", "A"),
    ("Primeira Linha Toldos", "Florianópolis · atende toda a Grande Florianópolis", "Fabricação e instalação de todos os tipos de toldos, coberturas e sombreamentos.", "primeiralinhatoldos.com.br", "3", "A"),
    ("Zandoná Coberturas", "Palhoça · atende Florianópolis, São José, Biguaçu, Gov. Celso Ramos, Santo Amaro e Tijucas", "Toldos, coberturas e pergolados há mais de 20 anos.", "zandonacoberturas.com.br", "3", "A"),
    ("Tendas Floripa", "Palhoça", "Venda e locação de tendas (sanfonadas, piramidais, chapéu de bruxa); oficina própria com serralheria, costura, corte e solda de lonas. Interessante por juntar ferro e lona no mesmo fornecedor para protótipo.", "tendasfloripa.com.br", "2 · 3", "A"),
    ("Classe-A Toldos e Coberturas", "Palhoça (Rua Adelino Martins, 20 · Bela Vista)", "Fabrica, vende e instala coberturas em lona e policarbonato e pergolados.", "@classeatoldos · anunciepalhoca.com.br", "3", "B"),
    ("SM Tendas e Coberturas", "Grande Florianópolis", "Tendas com calhas, ferragem alumínio, lona branca blackout ou lona cristal (transparente): referência para os painéis de cristal da variante Sensorial.", "smtendasecoberturas.com.br", "3", "B"),
    ("Toldos 2001 / Tradição Toldos", "Palhoça", "Toldos, coberturas e cortinas há mais de 30 anos na Grande Florianópolis.", "facebook.com (Tradição Toldos)", "3", "B"),
    ("Metal Toldos e Coberturas", "Barreiros · São José", "Toldos e coberturas · (48) 3246-2798 (listagem GoldLinks).", "goldlinks.com.br", "3", "B"),
    ("Tendas Catarinense · Tendas Palhoça", "Palhoça", "Tendas para eventos (venda / locação); confirmar fabricação própria.", "facebook.com", "3", "C"),
    ("Lonasville", "SC (confirmar cidade)", "Lonas, toldos, capas, tendas, coberturas e acessórios.", "lonasville.com.br", "3", "C"),
    ("Tendas Amaral", "Itajaí · atende Joinville, Balneário Camboriú, Florianópolis", "Tendas para eventos (locação); confirmar oficina de lona.", "tendasamaral.com.br", "3", "C"),
    ("Tenda Forte Eventos", "Brusque · atende Itajaí, Blumenau, Joinville, Criciúma", "Estruturas e tendas para eventos (11 anos); confirmar fabricação.", "tendaforteeventos.com", "3", "C"),
]
TENSO = [
    ("Alucober", "atua em SC (executou a cobertura retrátil do Mercado Público de Florianópolis)", "Coberturas tensionadas e retráteis com membrana Serge Ferrari Précontraint; engenharia de cobertura. Candidata ao projeto executivo da membrana (form-finding, compensação) e à instalação.", "alucober.com.br", "3", "A"),
    ("Pistelli Pelz Tensoestruturas", "SP · atua no Brasil e no exterior (40 anos)", "Projeto executivo de membrana, fabricação e instalação em PVC, PTFE e ETFE. Referência nacional para a lona do Casulo / Safari se o confeccionista local não fizer form-finding.", "estruturas.arq.br", "3", "A"),
    ("Formatto Coberturas Especiais", "Brasil (15 anos)", "Tensoestruturas: concepção, projeto, fabricação e instalação.", "formatto.ind.br", "3", "B"),
    ("Tensomembrana", "Brasil", "Coberturas tensionadas em membrana.", "tensomembrana.com.br", "3", "B"),
    ("Artflex Coberturas", "Brasil", "Membrana tensionada e tensoestruturas.", "artflexcoberturas.com.br", "3", "B"),
    ("Saltus", "Brasil", "Cobertura em membrana tensionada.", "saltus.com.br", "3", "C"),
    ("Tensor Estruturas", "Fortaleza / CE", "Tensoestruturas com engenheiros de estruturas metálicas (30 anos). Longe; referência de método.", "tensorestruturas.com", "3", "C"),
]
FABRICAS_TENDA = [
    ("Top Flex", "Brasil (fábrica própria, 13 anos, Copa 2014)", "Fábrica de tendas e lonas; venda e locação em todo o país.", "topflex.com.br", "3", "B"),
    ("Camp Tendas", "Brasil", "Fábrica de tendas em poliéster e lonas plásticas.", "camptendas.com.br", "3", "B"),
    ("Fábrica das Tendas", "Brasil", "Venda, locação e fabricação de tendas; conserto de lonas de caminhão (solda de lona).", "fabricadastendas.com.br", "3", "C"),
    ("Domebambu / Wedome Glamping", "Brasil (15 anos)", "Domos geodésicos de bambu com conexões metálicas e coberturas vinílicas para glamping: fornecedor nacional que já confecciona lona para glamping.", "domebambu.com.br", "3", "B"),
    ("JR Tendas", "Brasil", "Fornecedor de lonas para tendas.", "jrtendas.com.br", "3", "C"),
]
TECIDO = [
    ("Sansuy", "Brasil (maior fabricante de lonas PVC do país; loja e distribuidores)", "Laminados de PVC com poliéster de alta tenacidade (Vinilona, Vinigalpão). Tecido nacional para protótipo e forro; para a lona externa PVDF tipo II conferir gramatura 1050 g/m² e laca PVDF.", "sansuy.com.br · lojasansuy.com.br", "3", "A"),
    ("Cipatex", "Cerquilho / SP (desde 1964)", "Laminados sintéticos e lonas de PVC (Toda Carga); líder nacional em revestimentos.", "cipatex.com.br", "3", "B"),
    ("Serge Ferrari (Précontraint)", "França · importado via Alucober e distribuidores", "Membrana compósita de referência mundial para tensoestruturas (PVC/PVDF, 25 anos). Especificação-alvo da lona externa Zion.", "sergeferrari.com", "3", "A"),
    ("Tensoflex", "Brasil · revendedores em SC", "Telas tensionadas com perfis de alumínio: opção para o forro interno (Trevira CS / tela) e detalhes de arremate.", "tensoflex.com.br", "3", "B"),
]
VIDRO = [
    ("FLP Esquadrias", "Florianópolis (Costeira) · atende São José e Palhoça", "Esquadrias de alumínio com acompanhamento de projeto para arquitetos e engenheiros.", "flpesquadrias.com.br", "3", "A"),
    ("Versátil Glass", "São José", "Fábrica de esquadrias de alumínio, fachadas glazing, vidro temperado, linha premium.", "versatilesquadrias.com.br", "3", "A"),
    ("Grupo Imperial Esquadrias", "Florianópolis", "Esquadrias de alumínio, fachadas glazing, brises, guarda-corpos, vidro temperado.", "grupoimperialesquadrias.com", "3", "B"),
    ("Vidraçaria Almeida", "Florianópolis", "Vidraçaria e esquadrias de alumínio.", "vidracariaalmeida.com.br", "3", "C"),
    ("Lâmina Glass", "Grande Florianópolis", "Vidros e espelhos sob medida.", "laminaglass.com.br", "3", "C"),
]
GROUPS = [("LOTE 2 · SERRALHERIAS E ESTRUTURAS METÁLICAS (GRANDE FLORIANÓPOLIS E SC)", SERRALHERIAS, "Precisa ter: calandra de tubos (Ø48,3 a Ø114,3, raio variável) ou parceiro; solda MIG/TIG qualificada; galvanizador parceiro; espaço para fit test de um pórtico (6 x 4,5 m)."),
          ("CALANDRAGEM TERCEIRIZADA (SE FALTAR CALANDRA LOCAL)", CALANDRA, "Calandrar os 9 arcos do Casulo (tabela de geometria ZC-EST-002) fora e soldar / montar em SC; conferir no gabarito ± 5 mm."),
          ("GALVANIZAÇÃO A FOGO (NBR 6323)", GALVANIZACAO, "Peças ≤ 4,80 m (cuba); furos de respiro nos tubos; certificado por lote. Galvanizar depois do fit test."),
          ("TUBOS E PERFIS (MATÉRIA-PRIMA DO SERRALHEIRO)", TUBOS, "ASTM A500 Gr. B / NBR 8261; certificado do aço; Ø60,3 x 3,6 · Ø48,3 x 3,2 · Ø114,3 x 4,5 · U 150 x 60 x 3,0."),
          ("LOTE 3 · LONAS, TOLDOS E TENDAS (GRANDE FLORIANÓPOLIS)", LONAS_LOCAL, "Precisa ter: mesa de corte (ideal CNC) e solda de alta frequência (HF) ou solda quente para PVC 1050 g/m²; experiência com keder; equipe de instalação. A Zion entrega os padrões DXF; o confeccionista aplica a compensação."),
          ("TENSOESTRUTURAS · PROJETO EXECUTIVO DE MEMBRANA E INSTALAÇÃO", TENSO, "Para o form-finding, compensação, laudo biaxial e instalação da lona externa; podem também confeccionar. Usar em paralelo ao confeccionista local (protótipo) ou como fornecedor único da série."),
          ("FÁBRICAS DE TENDAS NACIONAIS (ALTERNATIVA)", FABRICAS_TENDA, "Fabricantes com escala para a série; conferir se aceitam confecção sob padrão (DXF) em tecido especificado pela Zion."),
          ("TECIDO E MEMBRANA (ESPECIFICAÇÃO E COMPRA)", TECIDO, "Lona externa: PVDF tipo II 1050 g/m², ≥ 4.200 / 4.000 N/5 cm, classe B / M2, 10 anos. Forro: Trevira CS 210 g/m². Comprar o rolo e entregar ao confeccionista, ou cotar já incluso."),
          ("VIDROS E ESQUADRIAS (LOTE 3 · VIDRO)", VIDRO, "Insulado low-e 6 + 12 + 6, laminado 8 + 8, curvo laminado (Visor / Anel de Luz / lanterna); contramarcos com ruptura térmica; medição na estrutura montada ± 3 mm.")]

def table(rows):
    th = "<tr><th>Empresa</th><th>Cidade / abrangência</th><th>O que faz · por que interessa</th><th>Site / fonte</th><th>Lote</th><th>Prior.</th></tr>"
    tr = "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td><td>{esc(c)}</td><td class=mono>{esc(d)}</td><td class=num>{esc(e)}</td><td class=num><span class='pr {f}'>{f}</span></td></tr>" for a, b, c, d, e, f in rows)
    return f'<table class="t xsmall">{th}{tr}</table>'

pages = []
def page(body, label, code=""):
    n = len(pages) + 1
    pages.append(f'<section class="page flow"><div class="head"><span>{zion_mark_html("14px", color="#1B2117")} ZION GLAMPING COLLECTION · {DOC} · {REV}</span><span>{esc(code or DOC)}</span><span>{esc(label)}</span></div>{body}<div class="foot"><span>LISTA DE PROSPECÇÃO DE FORNECEDORES · SEM PREÇOS · CONTATOS E CAPACIDADE A CONFIRMAR</span><span></span><span>{DATE} · {n:02d}</span></div></section>')

def build():
    pages.append(f'''<section class="page cover"><div class="coverbox"><div class="brand">{zion_mark_html("13mm", color="#FEF5F0", style="margin-right:6mm")}{zion_logo_html("13mm", color="#FEF5F0")}</div><div class="sub">ZION GLAMPING COLLECTION · ZION GLAMPING STORE · CONTRATAÇÃO POR LOTES</div>
<h1>FORNECEDORES<br>PARA COTAÇÃO</h1><h3>{DOC} · {REV} · {DATE} · FLORIANÓPOLIS, GRANDE FLORIANÓPOLIS E SANTA CATARINA</h3>
<p class="lead">Lista de prospecção para enviar os one-pagers de cotação (ZC / ZS / ZL / ZK-ONE-001) e os documentos de lote: serralherias e estruturas metálicas com calandra (lote 2), galvanização a fogo, empresas de lonas, toldos, tendas e tensoestruturas (lote 3), vidraçarias e esquadrias, e fabricantes de tecido. Montada por pesquisa na web em setembro de 2026 a partir de sites, listagens comerciais e redes sociais das empresas.</p>
<p class="rule">Nenhuma empresa foi contatada nem homologada. Cidade, capacidade (calandra, solda HF, galvanizador), telefone e e-mail devem ser confirmados no site ou por telefone antes do envio do RFQ. Prioridade A = perfil mais próximo do escopo e mais perto de Florianópolis; B = candidato a confirmar; C = listagem sem detalhe. Sem preços.</p></div></section>''')
    intro = '<h2>COMO USAR ESTA LISTA<small>triagem em 3 passos antes do RFQ</small></h2>' + f'''<div class="two"><div>
<h4>1 · TRIAGEM POR TELEFONE (5 MINUTOS)</h4><ol class="num"><li><b>Serralheria (lote 2):</b> "Vocês calandram tubo redondo Ø60 com raio variável (arco elíptico de 6 m de vão)? Soldam MIG/TIG com soldador qualificado? Com quem galvanizam a fogo? Conseguem pré-montar um pórtico de 6 x 4,5 m no pátio?"</li>
<li><b>Lona (lote 3):</b> "Vocês confeccionam lona de PVC 1050 g/m² com solda de alta frequência? Trabalham com keder? Cortam a partir de DXF que a gente manda? Já fizeram cobertura tensionada (não só toldo plano)? Instalam?"</li>
<li><b>Vidro (lote 3):</b> "Fazem vidro insulado low-e e laminado curvo? Contramarco de alumínio com ruptura térmica, anodizado bronze? Medem na obra depois da estrutura montada?"</li></ol>
<h4>2 · ENVIAR O PACOTE</h4><p class="lede">One-pager de cotação do modelo (1 página) + documento completo do lote (PDF) + DXF (peças ou padrões) + XLSX (coordenadas). Pedir retorno em 10 dias, validade 30 dias, impostos destacados, frete até Florianópolis.</p>
<h4>3 · COMPARAR</h4><p class="lede">Lote 2 em R$/kg galvanizado e prazo; lote 3 em R$/m² confeccionado + instalação por dia; vidro em R$/m² por tipo. Registrar tudo no documento interno de orçamento (pasta interno/). Este documento circula sem preços.</p></div>
<div><h4>QUEM COTA O QUÊ</h4><table class="t small"><tr><th>Lote</th><th>Fornecedor-tipo</th><th>Grupos desta lista</th></tr>
<tr><td><b>1 · Deck e infra</b></td><td>Empreiteiro de estacas helicoidais + serralheria (grelha) + carpinteiro de deck</td><td>Serralherias (grelha U 150) · galvanização · tubos</td></tr>
<tr><td><b>2 · Estrutura metálica</b></td><td>Serralheria com calandra + galvanizador</td><td>Serralherias · calandragem · galvanização · tubos</td></tr>
<tr><td><b>3 · Lonas e vidros</b></td><td>Confeccionista de lona (HF) + projetista de membrana + vidraceiro</td><td>Lonas e tendas locais · tensoestruturas · fábricas de tenda · tecido · vidro</td></tr>
<tr><td><b>4 · Mobílias</b></td><td>Marcenaria + FF&amp;E</td><td>(lista separada no sistema de mobiliário ZG-FFE)</td></tr></table>
<h4>ESTRATÉGIA SUGERIDA PARA O PROTÓTIPO DO CASULO</h4><ul class="chk"><li>Ferro: 2 serralherias locais (A) + Metalgalvano (ferro + galvanização) para comparar preço de série.</li><li>Lona: 1 confeccionista local (SC Lonas ou Tendas Floripa) para o forro e o protótipo + 1 especialista em tensoestrutura (Alucober ou Pistelli) para o form-finding e a lona externa.</li><li>Vidro: FLP ou Versátil, medição após o fit test.</li><li>Galvanização: Raitz (Joinville) como padrão da linha.</li></ul></div></div>'''
    page(intro, "Como usar", code=f"{DOC}-00")
    for i, (title, rows, note) in enumerate(GROUPS):
        page(f'<h2>{esc(title)}<small>{len(rows)} empresas · prioridade A / B / C</small></h2><p class="note">{esc(note)}</p>{table(rows)}', title.split(" (")[0].title(), code=f"{DOC}-{i + 1:02d}")
    src = ["guiafacil.com/encontre/serralherias-e-serralheiros/florianopolis/sc", "serralheriasj.com.br", "jdserralheria.com.br", "stilloserralheria.com", "lotusmetalica.com.br", "metalportometalurgica.com.br", "metalgalvano.com.br (Araquari, BR-280 km 26)", "guildindustrial.com.br", "rpsindustrias.com.br", "caldeirariadagama.com.br", "galvanizacaoraitz.com.br", "brazinc.com.br", "qualitytubos.com.br", "vtktubos.com.br", "golin.com.br",
           "sclonas.com.br", "primeiralinhatoldos.com.br", "zandonacoberturas.com.br", "tendasfloripa.com.br", "instagram.com/classeatoldos", "smtendasecoberturas.com.br", "telelistas.net/sc/palhoca/toldos", "goldlinks.com.br (Metal Toldos e Coberturas)", "lonasville.com.br", "tendasamaral.com.br", "tendaforteeventos.com",
           "alucober.com.br (Mercado Público de Florianópolis)", "estruturas.arq.br (Pistelli Pelz)", "formatto.ind.br", "tensomembrana.com.br", "artflexcoberturas.com.br", "saltus.com.br", "tensorestruturas.com", "topflex.com.br", "camptendas.com.br", "fabricadastendas.com.br", "domebambu.com.br", "jrtendas.com.br", "sansuy.com.br", "cipatex.com.br", "tensoflex.com.br/revendedores-tensoflex",
           "flpesquadrias.com.br", "versatilesquadrias.com.br", "grupoimperialesquadrias.com", "vidracariaalmeida.com.br", "laminaglass.com.br"]
    page('<h2>FONTES E PRÓXIMOS PASSOS<small>pesquisa web de 18/09/2026 · ligar antes de enviar</small></h2><div class="two"><div><h4>FONTES CONSULTADAS</h4><ul class="chk">' + "".join(f"<li class=mono>{esc(s)}</li>" for s in src) + '</ul></div><div><h4>PRÓXIMOS PASSOS</h4><ol class="num"><li>Ligar para as empresas de prioridade A e aplicar a triagem da página anterior; anotar telefone, e-mail e responsável.</li><li>Enviar o one-pager de cotação + documento do lote + DXF; agendar visita à oficina (calandra, mesa de solda HF).</li><li>Pedir 1 peça-amostra: um arco A3 calandrado (lote 2) e um painel P2 soldado com keder (lote 3) antes da série.</li><li>Registrar cotações em interno/ e escolher fornecedor do protótipo do Casulo.</li><li>Atualizar esta lista (REV 01) com os contatos confirmados e os descartados.</li></ol><h4>REVISÃO</h4><table class="t small"><tr><th>Rev</th><th>Data</th><th>Descrição</th></tr><tr><td>00</td><td>' + DATE + '</td><td>Lista de prospecção inicial (web); nenhuma empresa contatada</td></tr></table></div></div>', "Fontes e próximos passos", code=f"{DOC}-99")
    css = BASE_CSS + " .mono{font-family:'DM Mono',Menlo,monospace;font-size:6.6px} .pr{display:inline-block;width:12px;height:12px;line-height:12px;border-radius:50%;text-align:center;font-size:7px;font-weight:700;color:#FEF5F0;background:#8B714E} .pr.A{background:#1B2117} .pr.C{background:#B8AE97}"
    doc = f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>ZION · {DOC} · Fornecedores SC</title><style>{css}</style></head><body>{"".join(pages)}</body></html>'
    path = os.path.join(OUT_DIR, f"{DOC}_Fornecedores_SC.html"); open(path, "w", encoding="utf-8").write(doc); print(os.path.relpath(path, ROOT), len(pages), "páginas")
    # markdown
    md = [f"# {DOC} · FORNECEDORES PARA COTAÇÃO · Florianópolis e região · {REV} · {DATE}", "", "Lista de prospecção (pesquisa web, nenhuma empresa contatada). Prioridade A / B / C. Sem preços. Confirmar contatos no site antes do RFQ.", ""]
    for title, rows, note in GROUPS:
        md += [f"## {title}", "", f"_{note}_", "", "| Empresa | Cidade / abrangência | O que faz · por que interessa | Site / fonte | Lote | Prior. |", "|---|---|---|---|---|---|"]
        md += [f"| **{a}** | {b} | {c} | {d} | {e} | {f} |" for a, b, c, d, e, f in rows]
        md.append("")
    open(os.path.join(OUT_DIR, f"{DOC}_Fornecedores_SC.md"), "w", encoding="utf-8").write("\n".join(md))

if __name__ == "__main__":
    build()
