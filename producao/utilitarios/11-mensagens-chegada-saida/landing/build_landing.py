"""Gera landing/dist/clickmax.html da Ferramenta 11, reaproveitando o estilo da página da Ferramenta 17.
Uso: python3 -I landing/build_landing.py"""
import pathlib, html
A = pathlib.Path(__file__).resolve().parent
ESTILO_DE = A.parents[1] / "17-checklist-limpeza/landing/build_landing.py"
src = ESTILO_DE.read_text()
estilo = src[src.index('<link href='):src.index('</style>') + len('</style>')].replace("{{", "{").replace("}}", "}")
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
PRONTA = ("Paulo, seja bem-vindo(a)! O acesso é por fechadura com senha na porta principal. O código desta reserva é 4821. "
          "Wi-Fi: rede RecantoExemplo, senha senha-ficticia-123. Não é permitido fumar dentro da unidade. Silêncio depois das 22h. "
          "O check-out é até as 11h. Marta (fictícia), Recanto Exemplo.")
FALTA = PRONTA.replace("senha senha-ficticia-123", "senha [PREENCHA: Wi-Fi: senha]")
def tela(status, txt, ok):
    cor = "#C8E6C0" if ok else "#F4C7C3"
    t = html.escape(txt).replace("[PREENCHA: Wi-Fi: senha]", '<b style="color:#040605;background:#F4C7C3">[PREENCHA: Wi-Fi: senha]</b>')
    return (f'<figure style="margin:0"><div style="background:#fff;border-radius:10px;overflow:hidden"><div style="background:#1B2117;padding:10px">'
            f'<span style="color:#C9B37E;font-size:11px;letter-spacing:.12em">M04 · BOAS-VINDAS · EXEMPLO FICTÍCIO</span></div>'
            f'<div style="background:{cor};padding:10px;font-weight:700;font-size:13px"><span style="color:#040605">{status}</span></div>'
            f'<div style="padding:12px"><div style="background:#E7F3E2;border-radius:10px 10px 10px 2px;padding:10px;font-size:13px;line-height:1.45"><span style="color:#1B2117">{t}</span></div></div></div>'
            f'<figcaption>{"Ficha completa: pronta para copiar." if ok else "Senha do Wi-Fi vazia: a planilha avisa e não inventa."}</figcaption></figure>')
etapas = [("M01", "Confirmação da reserva", "logo após confirmar"), ("M02", "Endereço e acesso", "2 dias antes"), ("M03", "Bom dia da entrada", "no dia da entrada"),
          ("M04", "Boas-vindas, acesso e Wi-Fi", "na chegada"), ("M05", "Apoio durante a estadia", "manhã seguinte"), ("M06", "Lembrete da saída", "na véspera"),
          ("M07", "Dia da saída", "manhã da saída"), ("M08", "Agradecimento e avaliação", "depois da saída"), ("M09", "Chegada fora do horário", "resposta"), ("M10", "Problema na estadia", "resposta")]
lis = "".join(f'<li><b style="color:#C9B37E">{a}</b> {b} <span style="color:#A39E8E">· {c}</span></li>' for a, b, c in etapas)
corpo = f"""
<div class="zl">
<section class="hero gut" data-cx-section="hero">
<div class="col"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion" style="height:28px;margin-bottom:40px">
<span class="eyebrow">Ferramenta 11 · Zion Hospitality Business</span>
<h1>As mesmas perguntas, toda reserva. <em>As respostas já prontas.</em></h1>
<p style="font-size:20px;color:#FEF5F0">Aprenda o passo a passo para enviar, no momento certo, as mensagens de confirmação, acesso, chegada, apoio durante a estadia e saída, com as informações da sua hospedagem.</p>
<span class="micro" style="color:#C9B37E;font-size:15px;margin:0 0 22px;letter-spacing:.02em">Para Airbnb, casas, apartamentos, pousadas e glampings.</span><a class="btn" href="#oferta" data-cx-cta>Quero o meu kit</a><span class="micro">Planilha + modelos + guia · R$ 19 · pagamento único</span></div>
</section>
<section class="gut" data-cx-section="problem"><div class="col"><span class="eyebrow">O problema</span>
<h2>"Qual é a senha do <em>Wi-Fi</em>?"</h2>
<p>Endereço, horário, acesso, senha, regras, saída. Escrever tudo de novo a cada reserva toma tempo, e um dado esquecido vira ligação na hora da chegada.</p>
<ul class="lista"><li>Cada mensagem sai de um jeito, dependendo do dia.</li><li>A senha ou o horário mudam e a mensagem antiga fica errada.</li><li>Ninguém lembra de mandar o lembrete da saída na véspera.</li></ul></div></section>
<section class="gut" data-cx-section="solution"><div class="col"><span class="eyebrow">Como funciona</span>
<h2>Preencha uma vez. <em>Copie a cada reserva.</em></h2>
<p>Você preenche a ficha da hospedagem uma vez. A cada reserva, digita o nome do hóspede e as datas. A planilha monta as 10 mensagens, mostra o dia de enviar cada uma e avisa quando falta alguma informação.</p>
<div class="demo">{tela("Pronta para copiar", PRONTA, True)}{tela("Falta: Wi-Fi: senha", FALTA, False)}</div>
<p style="font-size:14px;color:#A39E8E">Trecho da mensagem M04 montada pela planilha no arquivo de exemplo (dados fictícios).</p>
<ul class="lista">{lis}</ul>
<p>A jornada parte dos scripts de atendimento usados nas unidades da Zion, generalizados para qualquer hospedagem.</p>
<figure style="margin:18px 0 0"><img src="{BASE}assets/operacoes/op07.webp" alt="Unidade da Zion Bubble Glamping" style="width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:6px;display:block"><figcaption style="font-size:13px;color:#A39E8E;margin-top:6px">Foto real · unidade da Zion Bubble Glamping, onde esses scripts são usados.</figcaption></figure></div></section>
<section class="gut" data-cx-section="offer" id="oferta"><div class="col"><span class="eyebrow">O que você recebe</span>
<img class="foto cm-image" src="{BASE}p/adbc67069af26ae0/kit-mensagens-11/capa.jpg" alt="Capa do produto: Kit de Mensagens de Chegada e Saída" data-cx-image-slot="offer" data-cx-image-hint="Foto real da Zion, sem pessoas" data-cx-image-kind="brand">
<div class="caixa"><ul class="lista" style="margin-top:0"><li>Planilha em branco: ficha, 10 mensagens montadas e datas de envio</li><li>Exemplo preenchido (dados fictícios)</li><li>Modelos em PDF para copiar à mão</li><li>Guia "Aprenda o passo a passo", com exercícios e critérios de conferência</li></ul>
<div class="preco">R$ 19</div><p style="margin-top:8px">Pagamento único, Pix ou cartão. Acesso aos arquivos depois do pagamento confirmado. Funciona no Excel, Google Sheets e LibreOffice.</p>
<div data-cx-checkout></div>
<p style="font-size:14px;color:#A39E8E">Reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></div></section>
<section class="gut" data-cx-section="faq"><div class="col"><span class="eyebrow">Perguntas frequentes</span>
<details><summary>Envia as mensagens sozinho?</summary><p>Não. Você copia e cola no WhatsApp ou na plataforma. Se a plataforma tiver mensagens rápidas ou programadas, pode colar lá.</p></details>
<details><summary>Funciona no celular?</summary><p>Sim, pelo app do Google Sheets ou do Excel. Preencher a ficha é mais confortável no computador.</p></details>
<details><summary>Posso mudar os textos?</summary><p>Pode. Edite depois de colar, sem mudar datas, horários, senha e endereço.</p></details>
<details><summary>E se eu esquecer um dado?</summary><p>A mensagem mostra [PREENCHA] no lugar e não aparece como pronta.</p></details>
<details><summary>Pede avaliação 5 estrelas?</summary><p>Não. Pede uma avaliação honesta, sem oferecer nada em troca. Confira também as regras da sua plataforma.</p></details>
<details><summary>Para quem não é?</summary><p>Para quem procura envio automático ou integração com as plataformas.</p></details></div></section>
<section class="gut" data-cx-section="cta" style="text-align:center"><div class="col"><h2>Cada mensagem <em>no dia certo</em>.</h2>
<a class="btn" href="#oferta" data-cx-cta>Quero o meu kit</a><span class="micro">Material educativo. Não garante avaliações, reservas nem ocupação.</span></div></section>
</div>"""
(A / "dist").mkdir(exist_ok=True); (A / "dist/clickmax.html").write_text(estilo + corpo); print(len(estilo + corpo))
