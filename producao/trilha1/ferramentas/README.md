# Ferramentas da Trilha 1 · especificação para o Claude Code

A Trilha 1 tem **cinco ferramentas**, uma por ponto de decisão. Cada uma é uma página do app **Zion Exercícios**: o aluno responde, a página faz as contas na hora, a inteligência artificial (quando ligada) lê as respostas, e o aluno baixa a página do Dossiê em PDF.

| Link curto | Ferramenta | Quando aparece | Junta as especificações | Página do Dossiê |
|---|---|---|---|---|
| `[domínio do app]/1-1` | Marco Zero · O seu diagnóstico prévio | fim do Marco Zero | `aula-01.json` | Página 0 · A ficha de entrada |
| `[domínio do app]/etapa-1` | Etapa 1 · Território e mercado | fim da Aula 1 | `aula-02.json` + `aula-03.json` | Dossiê 1 · Território e mercado |
| `[domínio do app]/etapa-2` | Etapa 2 · Desenhar o negócio | fim da Aula 3 | `aula-04.json` + `aula-05.json` + `aula-06.json` | Dossiê 2 · Produto, modelo e masterplan |
| `[domínio do app]/etapa-3` | Etapa 3 · Estruturar o capital | fim da Aula 5 | `aula-07.json` + `aula-08.json` + `aula-09.json` + `aula-10.json` | Dossiê 3 · CAPEX, receita, viabilidade e capital |
| `[domínio do app]/dossie-final` | Dossiê final | Aula 6 | `aula-12.json` + as respostas salvas das etapas | Dossiê final · capa e diagnóstico completo |

O antigo `aula-11.json` (lançamento) NÃO entra: o lançamento passou para a Trilha 2.

## O que já existe
- `aula-NN.json`: os campos, as contas (`calculos`), as regras de veredito, o prompt da IA (`prompt_ia`), a página do Dossiê e as pendências de cada antiga aula. Leia `README-especificacoes-antigas.md` (o formato e a lista de decisões pendentes do Bruno).
- `ts/`: as contas já programadas em TypeScript, sem dependência, com testes (dentro de `ts/`: `npx tsx --test tests/*.test.ts`, 29 testes). `ts/index.ts` exporta `calculadoras["1-1"…"1-12"]`.

## Como montar cada ferramenta de etapa
1. **Juntar as antigas páginas em uma**, em seções na ordem da tabela (ex.: Etapa 1 = seção Território, depois seção Mercado). Campos repetidos entre páginas viram um só (mesmo `id` ou mesma pergunta). Meta: até 30 campos por etapa; se passar, mantenha os que alimentam alguma conta ou o veredito e mova o resto para "opcional".
2. **Contas:** rode as calculadoras de cada antiga aula com as respostas da etapa (`calculadoras["1-2"]` e `calculadoras["1-3"]` na Etapa 1, e assim por diante) e mostre os resultados por seção.
3. **Nota e leitura**, como ensinam as aulas: "Não sei" vale zero; primeiro os alertas (toda nota zero ou um), depois a soma, depois a decisão; não existe nota de corte; nota sem evidência não vale.
4. **Veredito da etapa:** o mais cauteloso entre os vereditos das antigas páginas (ordem pausar > testar > ajustar > avançar), e o aluno escreve o critério para parar.
5. **IA (opcional, ligada por configuração):** junte os `prompt_ia` das páginas da etapa num só prompt de sistema; a IA recebe `{"respostas": {...}, "calculos": {...}}` e devolve só JSON `{resumo, pontos_fortes[], ponto_fragil, veredito, criterio_para_parar, proxima_acao{acao, responsavel, prazo, evidencia}, perguntas_em_aberto[]}`. Ela pode ser mais cautelosa que o veredito das contas, nunca mais otimista. Sem IA, a página mostra as contas, os alertas e o veredito sugerido, e funciona igual.
6. **PDF do Dossiê:** um botão "Baixar o meu Dossiê" gera o PDF da página (capa com o nome da etapa, respostas, contas, alertas, ponto mais frágil, veredito, critério para parar, compromisso de 7 dias e o rodapé). Identidade: verde `#16261C`, creme `#F5F1E8`, dourado `#E0BE5E`, Playfair Display nos títulos e Inter no texto.
7. **Dossiê final:** lê as respostas salvas das três etapas (no navegador do aluno ou no banco, se houver) e monta o Dossiê completo, com o veredito pela página mais fraca (`aula-12.json`).

## Rodapé de todas as páginas
"Leitura do método, não promessa. Conteúdo educacional. Não é oferta de investimento nem promessa de renda, retorno, ocupação, crédito ou sociedade."

## Hospedagem e dados
- Versão 1 (pode publicar já, depois de aprovada): app estático (por exemplo Vite + React + TypeScript), respostas salvas no navegador do aluno, contas e PDF no próprio navegador, sem IA. Pode ser hospedado onde o Bruno tiver conta (Vercel, Netlify, Cloudflare Pages) ou recriado no Lovable a partir deste código.
- Versão 2 (com IA): uma função de servidor que chama a API da Anthropic. A chave fica numa variável de ambiente do serviço de hospedagem, configurada pelo Bruno. Nunca no código, nunca no navegador, nunca numa conversa.
- Captura de leads no ClickMax: se o Bruno quiser, cada envio também vai para um formulário ou webhook do ClickMax. Pergunte antes e peça o endereço a ele.
- Nada é publicado, ligado a domínio ou conectado a conta sem aprovação expressa do Bruno.

## Pendências do Bruno que afetam as ferramentas
- O domínio do app (troca `[domínio do app]` em todo lugar).
- As decisões listadas em `README-especificacoes-antigas.md` ("O que precisa de decisão do Bruno"), menos as do lançamento (Aula 11), que saiu.
- As antigas páginas falam em "Ordem Zion" com quatro etapas e numeram as aulas de 1 a 12: ajuste os textos para a jornada de três etapas e a numeração nova (Marco Zero e Aulas 1 a 6).
