#!/usr/bin/env python3
"""Página de agradecimento da Mini Mentoria (R$ 47). Rascunho /obrigado-mini-mentoria. Uso: python3 -I build.py
Sem formulário (a receita 'thank-you' do importador proíbe captura): o convite ao cadastro do terreno aponta para a aula dentro da plataforma."""
from pathlib import Path
BASE = "https://bchaerk-creator.github.io/zion-hotel-ai-developer/"
PLAT = "https://zion-plataforma.clickmax.space"
CSS = """
*{box-sizing:border-box}html body{margin:0;background:#0d1512;color:#fef5f0;font-family:'Jost',sans-serif;font-size:17px;font-weight:300;line-height:1.6}
.w{max-width:680px;margin:0 auto;padding:0 20px}.sec{padding:44px 0}.creme{background:#fef5f0;color:#1b2117}.escuro{background:#0d1512;color:#fef5f0}
.topo{padding:20px 0;border-bottom:1px solid #c9b37e40}.topo img{height:34px;width:auto;display:block}
h1,h2{font-family:'Cormorant Garamond',serif;font-weight:500;line-height:1.1;margin:0}h1{font-size:40px}h2{font-size:30px}
.escuro h1,.escuro h2{color:#fef5f0!important}.creme h1,.creme h2{color:#1b2117!important}
p{margin:14px 0 0}.escuro p,.escuro li{color:#fef5f0}.creme p,.creme li{color:#1b2117}
p.k{font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;margin:0 0 14px;color:#c9b37e}.creme p.k{color:#8b714e}
.btn{display:flex;align-items:center;justify-content:center;min-height:54px;margin-top:22px;padding:12px 24px;border-radius:999px;background:#c9b37e;color:#1b2117;text-decoration:none;font-weight:500;letter-spacing:.05em;text-align:center}
ol.passos{list-style:none;margin:18px 0 0;padding:0}ol.passos li{margin:0 0 10px;padding:12px 14px;border:1px solid #8b714e59;border-radius:12px;background:#fff}
ol.passos li b{font-weight:600}.nota{font-size:14px}footer{background:#0d1512;padding:26px 0 44px;font-size:12.5px}footer p{color:#ded6bf;margin:0 0 8px}
@media(min-width:820px){h1{font-size:54px}h2{font-size:38px}.sec{padding:64px 0}.btn{width:fit-content;min-width:340px}}
"""
HTML = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mini Mentoria de Estruturação | Obrigado</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,500&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<div class="escuro"><div class="w topo"><img src="{BASE}brand/zion-logo-claro.png" alt="Zion Hotel Group International" width="170" height="34"></div></div>
<section data-cx-section="confirmation" class="sec escuro"><div class="w"><p class="k">Mini Mentoria de Estruturação</p>
<h1>Pagamento recebido. Bem-vindo.</h1>
<p>Você adquiriu a Mini Mentoria de Estruturação, uma formação digital com acesso por 12 meses.</p>
<p><b>Como acessar:</b> o acesso é liberado para o e-mail usado na compra. Você entra com esse e-mail; o primeiro acesso é sem criar senha. Se não conseguir entrar, fale com a gente pelo WhatsApp no fim desta página.</p>
<a class="btn" href="{PLAT}" data-cx-cta>ENTRAR NA PLATAFORMA</a></div></section>
<section data-cx-section="next-step" class="sec creme"><div class="w"><p class="k">Por onde começar</p>
<h2>Comece pelo Marco Zero.</h2>
<ol class="passos"><li><b>1.</b> Entre na plataforma e abra o módulo <b>Comece aqui</b>.</li>
<li><b>2.</b> Siga para o <b>Marco Zero</b>: a visão da jornada e o seu diagnóstico prévio.</li>
<li><b>3.</b> Depois, avance pelos sete pilares, na ordem. Em cada etapa: assista, preencha a ficha e monte a página do seu Dossiê. No final, gere o PDF.</li></ol>
<p class="nota">Material educativo. Não há reunião nem atendimento individual.</p>
<p class="k" style="margin-top:30px">Opcional</p>
<p>No Pilar 7 há a aula para cadastrar o seu terreno no banco de áreas da Zion. É opcional: a Zion avalia cada caso, e o cadastro não garante parceria nem investimento.</p></div></section>
<section data-cx-section="support" class="sec escuro"><div class="w"><h2>Precisa de ajuda?</h2>
<p>Fale com a gente pelo WhatsApp +55 48 6137-1061. Se quiser pedir reembolso, você tem 7 dias, como prevê o Código de Defesa do Consumidor.</p></div></section>
<footer><div class="w"><p>Zion Hotel Group International · Conteúdo educacional. Resultados dependem do contexto e da execução.</p></div></footer>
</body></html>
"""
Path(__file__).with_name("index.html").write_text(HTML, encoding="utf-8")
print(len(HTML), "bytes; span:", HTML.count("<span"), "script:", HTML.count("<script"))
