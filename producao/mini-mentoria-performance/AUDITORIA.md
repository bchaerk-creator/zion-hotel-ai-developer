# Auditoria do pacote Zion_Performance_47.zip (25/11/2026)

Lido por inteiro: `COMANDO_MESTRE.md`, `formularios.json` (70 perguntas), `roteiros_7_aulas.md`, `landing.md`, `criativos.md`, `videos_comerciais.md`, `prototipo.html`, 7 e-books e 7 capas em PDF. Cópia dos textos em `fontes/`.

## O que aproveitei
Estrutura de 7 pilares × 10 perguntas, escala (2/1/0/não sei/não se aplica), regra de pontuação, jornada, regras de rastreamento e de testes, textos dos 7 criativos (49 copies), estrutura da landing.

## Problemas encontrados (e o que fiz)
1. **E-books com texto repetido:** cada guia de 33 páginas repete as mesmas frases genéricas ("Passo 1: reúna a informação…") em todas as perguntas. → Reescritos: 7 guias de 34 páginas com por que importa, passo a passo, exemplo fictício conferido, erro comum, critério 0/1/2 e verificação.
2. **Capas só tipográficas e sem foto:** → capas com foto real da Zion, logo oficial sem distorção, linha "Para Airbnb, casas, apartamentos, pousadas e glampings".
3. **Roteiros das aulas** usam o mesmo molde nas 7 aulas, grafias como "adr", "revpar", "zion" minúsculas e "Na próxima etapa" sem etapa seguinte. → Usados só como roteiro em texto na plataforma, sem alterar; revisão de texto e gravação ficam para Bruno.
4. **`formularios.json` não tem calculadoras, pesos nem campos numéricos.** → Criei as 7 calculadoras e a metadata (`src/meta.json`: impacto, esforço, item crítico). **Pesos iguais, faixas 40/70, impacto e esforço são hipóteses minhas, a validar com a equipe.**
5. **`prototipo.html`** não trata "não sei" nem cobertura. → Não reaproveitado (serviu só de referência).
6. **`landing.md` afirma "sete aulas gravadas"** e deixa prazo de acesso e suporte em branco. → A página diz "7 aulas guiadas" (os vídeos não existem). Assumi **12 meses de acesso** (padrão das outras ofertas) e suporte pelo WhatsApp da conta: **Bruno confirma**.
7. **Gancho × conteúdo nos criativos:** "Quer expandir, mas não tem capital?" leva a "cada tarefa tem responsável?"; "Por que seu concorrente cobra mais?" leva a "simule a chegada". Mantido como veio; sinalizado em `anuncios/COPIES.md`.
8. **"Campeões":** as composições campeãs são por custo por lead, não por venda. Nada afirma venda campeã.
9. **Persistência "por usuário autenticado":** uma página estática não tem login. → Os dados ficam no aparelho, em um perfil por nome, com cópia de segurança. Persistência no servidor depende de backend (pendência).
10. **Convite à Zion:** não há endpoint para receber o dossiê. → O convite abre o WhatsApp com mensagem sem dados; o envio é manual, com consentimento desmarcado por padrão.
11. **Sobreposição de nome e preço:** existe a Mini Mentoria de Estruturação (R$ 47, terreno). Público e promessa são diferentes (hospedagem em operação), mas o nome e o preço se parecem: a Bela e o Meta podem confundir os dois. Nada foi alterado.
12. **Vídeos comerciais (`videos_comerciais.md`):** só roteiros; não produzidos.
