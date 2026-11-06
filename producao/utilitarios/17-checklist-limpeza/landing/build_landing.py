"""Gera landing/dist/clickmax.html da Ferramenta 17. Fotos reais pelo endereço público do site Zion;
telas de demonstração embutidas (webp). Uso: python3 -I landing/build_landing.py"""
import pathlib
A = pathlib.Path(__file__).resolve().parent; P = A.parent
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
LIN = ["Limpar box, vidros e espelho", "Repor toalhas limpas", "Testar luzes e tomadas", "Testar o chuveiro (água quente)", "Conferir o Wi-Fi"]
def tela(status, ok):
    cor = "#C8E6C0" if ok else "#F4C7C3"
    linhas = "".join(f'<div style="display:flex;justify-content:space-between;gap:6px;padding:7px 10px;border-top:1px solid #DED6BF;font-size:12px"><span style="color:#1B2117">{l}</span><span style="color:#1B2117;background:{"#F4C7C3" if (l.startswith("Testar o chuveiro") and not ok) else "#C8E6C0"};padding:0 6px;border-radius:4px;font-weight:600">{"PENDENTE" if (l.startswith("Testar o chuveiro") and not ok) else "OK"}</span></div>' for l in LIN)
    leg = "Depois do conserto e da nova conferência: liberada." if ok else "Chuveiro reprovado na conferência: a unidade fica bloqueada."
    return f'<figure style="margin:0"><div style="background:#fff;border-radius:10px;overflow:hidden"><div style="background:#1B2117;padding:10px"><span style="color:#C9B37E;font-size:11px;letter-spacing:.12em">CABANA 2 · EXEMPLO FICTÍCIO</span></div><div style="background:{cor};padding:10px;font-weight:700;font-size:13px"><span style="color:#040605">{status}</span></div>{linhas}</div><figcaption>{leg}</figcaption></figure>'

UTM = "?utm_source=meta&utm_medium=paid&utm_campaign=ferramenta17"
html = f"""<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Jost:wght@400;500;600&display=swap" rel="stylesheet">
<style>
.zl{{--preto:#040605;--musgo:#1B2117;--creme:#FEF5F0;--areia:#DED6BF;--terra:#8B714E;--champ:#C9B37E;--muted:#A39E8E;--linha:rgba(222,214,191,.16);
background:#040605;color:#FEF5F0;font-family:"Jost",Arial,sans-serif;font-size:17px;line-height:1.6;overflow-x:hidden}}
.zl *{{box-sizing:border-box}} body{{margin:0;background:#040605}}
.zl .gut{{padding-left:20px;padding-right:20px}} .zl .col{{max-width:640px;margin:0 auto}} .zl section{{padding-block:72px}}
.zl h1,.zl h2,.zl h3{{font-family:"Cormorant Garamond",Georgia,serif;font-weight:400;line-height:1.05;margin:0 0 18px;color:#FEF5F0}}
.zl h1{{font-size:clamp(44px,10vw,84px)}} .zl h2{{font-size:clamp(34px,7vw,54px)}} .zl h3{{font-size:26px}}
.zl h1 em,.zl h2 em{{color:#C9B37E;font-style:italic}}
.zl p,.zl li{{color:#DED6BF;font-family:"Jost",Arial,sans-serif}} .zl span{{color:inherit}}
.zl .eyebrow{{display:block;font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:#C9B37E;margin-bottom:18px;font-weight:500}}
.zl .btn{{display:inline-block;background:#C9B37E;color:#040605;font-weight:600;text-decoration:none;padding:18px 30px;border-radius:2px;letter-spacing:.08em;text-transform:uppercase;font-size:15px}}
.zl .micro{{display:block;font-size:13px;color:#A39E8E;margin-top:12px}}
.zl .hero{{position:relative;min-height:78vh;background:radial-gradient(circle at 80% 20%,#2c3524 0%,#1B2117 50%,#040605 100%);display:flex;align-items:flex-end;padding-block:110px 64px}}
.zl .hero img.bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}

.zl .hero .col{{position:relative;z-index:1;width:100%}} .zl .credito{{position:absolute;right:20px;bottom:12px;z-index:1;font-size:11px;color:#A39E8E}}
.zl .lista{{list-style:none;padding:0;margin:24px 0}} .zl .lista li{{padding:14px 0;border-top:1px solid rgba(222,214,191,.16);color:#FEF5F0}}
.zl .demo{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:26px 0}} .zl .demo img{{width:100%;border-radius:10px;display:block}}
.zl .demo figcaption{{font-size:13px;color:#A39E8E;margin-top:6px}}
.zl .caixa{{background:#1B2117;border:1px solid rgba(201,179,126,.35);border-radius:6px;padding:26px}}
.zl .preco{{font-family:"Cormorant Garamond",serif;font-size:64px;color:#C9B37E;line-height:1}}
.zl details{{border-top:1px solid rgba(222,214,191,.16);padding:14px 0}} .zl summary{{cursor:pointer;color:#FEF5F0;font-weight:500}}
.zl .foto{{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:6px;margin-bottom:20px}}
@media (max-width:420px){{.zl .demo{{grid-template-columns:1fr}}}}
</style>
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow">Ferramenta 17 · Zion Hospitality Business</span>
<h1>Sua unidade está <em>mesmo</em> pronta para o próximo hóspede?</h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para limpar, conferir e liberar cada unidade com o mesmo padrão, sabendo quem fez, quem conferiu e o que ficou pendente.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o meu checklist</a><span class="micro">Planilha + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow">O problema</span>
<h2>Quem limpou não viu. <em>Quem chega vê.</em></h2>
<p>A limpeza parece feita, mas o chuveiro está frio, o ralo ficou com cabelo ou faltou papel. Sem um padrão escrito e uma conferência, cada troca de hóspede depende da memória de alguém.</p>
<ul class="lista"><li>A equipe nova não sabe a ordem nem o que é inegociável.</li><li>Ninguém confere com o olhar de quem vai chegar.</li><li>O que ficou para depois se perde no grupo de mensagens.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow">Como funciona</span>
<h2>Só aparece <em>liberada</em> quando o obrigatório foi feito e aprovado.</h2>
<p>Uma planilha pronta com 33 itens em 8 ambientes, que você ajusta à sua unidade. Quem limpa marca o que fez. Quem confere aprova ou reprova, usando o critério escrito em cada linha. A planilha mostra a situação da troca e guarda as pendências e o histórico.</p>
<div class="demo">{tela("NÃO LIBERAR: 1 item obrigatório pendente", False)}{tela("LIBERADA PARA O PRÓXIMO HÓSPEDE", True)}</div>
<p style="font-size:14px;color:#A39E8E">Trecho da tela da planilha, com os resultados que ela calcula no arquivo de exemplo (dados fictícios).</p>
<ul class="lista"><li><b style="color:#C9B37E">1.</b> Ajuste o modelo: apague, acrescente, marque o que é obrigatório.</li><li><b style="color:#C9B37E">2.</b> Defina quem limpa e quem confere (ou confira sozinho).</li><li><b style="color:#C9B37E">3.</b> Marque a troca item por item.</li><li><b style="color:#C9B37E">4.</b> Libere só com a situação verde.</li><li><b style="color:#C9B37E">5.</b> Registre pendências e o histórico.</li></ul>
<p>A sequência do modelo parte da rotina de troca usada nas unidades da Zion, generalizada para qualquer hospedagem.</p>
<figure style="margin:18px 0 0"><img src="{BASE}assets/operacoes/op12.webp" alt="Unidade da Zion Bubble Glamping" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block"><figcaption style="font-size:13px;color:#A39E8E;margin-top:6px">Foto real · unidade da Zion Bubble Glamping, onde essa rotina de troca é usada.</figcaption></figure></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/checklist-17/capa.jpg" alt="Capa do produto: Checklist de Limpeza, Inspeção e Liberação" data-cx-image-slot="offer" data-cx-image-hint="Foto real da Zion, sem pessoas" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco com o modelo de 33 itens pronto para ajustar</li><li>Exemplo preenchido (dados fictícios)</li><li>Checklist para imprimir, com assinaturas</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel. Para ajustar o modelo pela primeira vez, o computador é mais confortável.</p></details>
<details><summary>Trabalho sozinho. Serve?</summary><p>Serve. Você marca que confere o próprio trabalho e faz a conferência depois de terminar tudo.</p></details>
<details><summary>Minha unidade tem itens diferentes.</summary><p>O modelo é editável: apague, acrescente e marque o que é obrigatório.</p></details>
<details><summary>Diz quais produtos de limpeza usar?</summary><p>Não. Produtos e proteção são definidos pelo responsável, seguindo o rótulo.</p></details>
<details><summary>Garante nota 5 nas avaliações?</summary><p>Não. Ajuda a não esquecer etapas e a conferir. A avaliação depende de muitos fatores.</p></details>
<details><summary>Para quem não é?</summary><p>Para quem procura um aplicativo com notificações e sincronização automática.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Libere com <em>critério</em>, não com pressa.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o meu checklist</a><span class="micro">Material educativo. Não garante avaliações, reservas nem ocupação.</span></div></section>
</div>"""
(A/"dist").mkdir(exist_ok=True); (A/"dist/clickmax.html").write_text(html); print(len(html))
