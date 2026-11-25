# Pacote para o ChatGPT v3 · Funil híbrido · Mini Mentoria de Estruturação Zion (R$ 47)

Substitui `PACOTE_PARA_CHATGPT_v2.md` (v2 vira histórico; os fatos e as peças de venda continuam valendo). **Sem execução:** nada foi enviado ao Meta. Subir ou ativar qualquer anúncio exige "aprovado" de Bruno; criar sempre **pausado**. URLs públicas abrem depois do deploy do GitHub Pages. Budget proposto (hipótese a validar, ver `10-trafego`): teto R$ 60/dia = captação R$ 30 + venda quente R$ 15 + venda fria R$ 15.

## 1. Dados fixos (iguais à v2)
Produto único: **Mini Mentoria de Estruturação Zion**, R$ 47, pagamento único, sem mensalidade, Pix ou cartão à vista, 12 meses, 9 módulos e 70 aulas e materiais, reembolso em 7 dias. Venda: destino `https://infoprodutos-zion.clickmax.space/mini-mentoria` (sem `#pagar`), botão **Saiba mais**, primeira linha "Acesse a plataforma por R$ 47". UTM de venda: `PADRAO_UTM.md` (`utm_campaign=mm47`). Nunca `/inscricao`, `/inscricao-47`, `/inscricao-curta`, `/parceiro-zion`.

## 2. CAMINHO A · CAPTAÇÃO (nova, `docs/ads/captacao-p0/`)
Mensagem única: **cadastro gratuito**; **existem formações pagas, incluindo a Mini Mentoria R$ 47**; sem reunião, consultoria, avaliação do terreno, investimento ou parceria garantidos. Destino: **formulário nativo NOVO** (`FORMULARIO_CAPTACAO_TEXTOS.md`; criar no Gerenciador, com consentimentos separados e opcionais). Botão: **Cadastre-se**. UTM: `utm_campaign=captacao`, `utm_content=<id>` (tags em `manifesto.json`).
| id | Peça | Arquivo | Título | Hook preservado |
|---|---|---|---|---|
| capt-c-carrossel-c | Carrossel C v-captação (7 cartões) | `docs/ads/captacao-p0/capt-c-carrossel-c-1..7.png` | Cadastro gratuito: estruture o projeto | "Você tem um terreno em um destino turístico, mas não tem capital...?" |
| capt-v02-dono-terreno | Vídeo 02 Dono de Terreno (mudo, texto na tela; ou regravar o roteiro) | fora do repositório (scratchpad; Bruno hospeda) | Dono de terreno? Comece pelo projeto | "Ei, você, dono de terreno!" |
| capt-v01-terreno-capital | Vídeo 01 Terreno Capital (idem) | fora do repositório | Terreno parado? Comece estruturando | "Você aí, dono de terreno." |
Textos: `docs/ads/captacao-p0/COPIES.md`. Roteiros de gravação e tabelas "atual | problema | novo": `CAPTACAO_CORRIGIDA.md`.
**Pré-condições antes de ligar a captação (todas dependem de Bruno):**
1. Pausar os 3 anúncios de R$ 270 e os 2 "FORM 47" (texto promete reunião/equipe/taxa) e **não** reaproveitar os formulários antigos (não editáveis).
2. Pausar o fluxo `bc86b069`, que hoje envia o modelo `clube_plataforma_d0` ("O acesso custa R$ 97", banco de áreas, botão `/inscricao`); só reativar com o modelo substituto aprovado pelo Meta (`MENSAGENS_TRANSICAO_E_EDUCACAO.md`).
3. Criar o formulário novo; conferir no Gerenciador se a caixa de consentimento pode ser opcional [NC].
4. Confirmar o piso "formação paga a partir de R$47" (há ferramentas de R$ 19 e Arsenal R$ 27 no catálogo) [NC].
5. Não subir lista de leads antigos como público (ver `10-trafego/LGPD_BASE_LEGAL_E_PUBLICOS.md`).

## 3. CAMINHO A · VENDA QUENTE (remarketing: leads cadastrados e visitantes, **excluídos compradores**). Máx. 6
`mm47f3-c08-oferta-47` · `mm47p0-n02-dossie-passeio` · `mm47p0-n06-entregaveis-numeros` · `mm47p0-n07-para-quem-e` · `mm47p0-n03-exemplo-ficticio` · `mm47f3-c09-objecoes`. Arquivos em `docs/ads/mm47-fase03/` (c08, c09) e `docs/ads/mm47-p0/` (n02, n03, n06, n07). Textos: `COPIES_P0.md` §E (remarketing) e `COPIES.md` de cada pasta.

## 4. CAMINHO B · VENDA FRIA (Brasil amplo, excluindo leads e compradores quando possível). Máx. 6
`mm47p0-vp0-a3-saiba-o-custo` · `mm47p0-vp0-a1-dor-direta` · `mm47f3-c03-custo-escondido` · `mm47f3-c06-obra-ultimo-passo` · `mm47p0-vp0-carrossel-c-narrativa` · `mm47f3-c10-obra-ou-estrutura`. Arquivos em `docs/ads/mm47-p0/` (a3, a1, carrossel c) e `docs/ads/mm47-fase03/` (c03, c06, c10). Opcional como 7º: vídeo mudo `vp0-v02-passeio-mm47-sem-audio.mp4` (fora do repositório).

## 5. NÃO USAR (inclui tudo da v2 §3, mais)
- Os 3 anúncios de captação R$ 270 no ar (Vídeo 01, Vídeo 02, Carrossel C originais), os 2 "FORM 47" e os formulários "inscrição" e "Direto low".
- Vídeos originais com o áudio ("agende a tua sessão de consultoria", "investimentos em destinos turísticos", bubbles à venda, "setor que mais cresce"): só as versões mudas `capt-*` ou regravação de Bruno.
- Telas da plataforma `agendar`, `mapa`, `raiox`, `implantacao`; aula 1 do Onboarding (Land Bank).

## 6. Antes de ligar (depende de Bruno): ver `CAPTACAO_CORRIGIDA.md` §6 (ordem de execução, quem executa, reversão).
