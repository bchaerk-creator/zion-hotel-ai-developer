# Formulário Meta · "Diagnóstico do terreno" v2 · gatilhos na voz do lead (10/11/2026)

Pedido do Bruno: as opções do formulário precisam ser as frases que o lead diria. Base: 444 respostas únicas (12/08 a 10/11): 63% dizem dinheiro ou sócio, 27% "não sei por onde começar", 18% "será que o terreno serve", 13% medo de errar.

Regra: formulário NOVO no Meta (não alterar o atual, que alimenta a sincronização hora a hora). Nome sugerido: "Land Bank | Diagnóstico do terreno v2 · gatilhos". Depois de criado, a sincronização passa a aceitar os dois nomes.

## Pergunta 1 (obrigatória, uma opção) · "Qual dessas frases é a sua hoje?"
| Código | Opção (texto exato) | Dor | Rota |
|---|---|---|---|
| CAPITAL | Tenho o terreno, mas não tenho o capital para desenvolver o projeto | capital | Zaya · vídeo "Falta o capital" → clube R$ 97 |
| INVESTIDOR | Quero saber como trazer um investidor para o meu projeto | capital/sócio | Zaya · vídeo "Quero um parceiro" → clube → reunião |
| PARCEIRO | Quero um parceiro para desenvolver comigo e não sei como atraí-lo | sócio | Zaya · vídeo "Quero um parceiro" → clube → reunião |
| SOZINHO | Quero fazer sozinho, mas não sei por onde começar | começar | Zaya · vídeo "Por onde começar" → clube |
| SERVE | Não sei se o meu terreno serve para hospedagem | potencial | Zaya · diagnóstico → clube |
| MEDO | Tenho medo de errar e perder dinheiro depois de pronto | medo | Zaya · vídeo "Medo de errar" → clube |
| OPERADOR | Já tenho uma hospedagem e quero expandir | operador | Reunião direta (operador para operador) |

## Pergunta 2 (obrigatória) · "Hoje, para estruturar o projeto, você tem:"
| Opção | Leitura |
|---|---|
| Recurso próprio para começar | tem dinheiro → prioridade 1, reunião |
| Uma parte, e preciso completar com sócio ou crédito | alavancar → clube + reunião |
| Só o terreno: a ideia é a terra atrair quem entra com o dinheiro | sem capital → clube |

## Pergunta 3 · "A documentação da área está:"
Escritura ou matrícula em dia · Só contrato ou posse · Ainda não tenho · (define a segunda trava; posse = regularizar antes de sócio)

## Pergunta 4 · "O investimento que você imagina para o projeto:"
Até R$ 150 mil · R$ 150 a 400 mil · R$ 400 mil a 1 milhão · R$ 1 a 3 milhões · Acima de R$ 3 milhões

## Pergunta 5 (texto curto) · "Cidade e estado do terreno"

Nome, e-mail e WhatsApp: campos nativos. Cinco perguntas no máximo, para não cair a taxa de conclusão.

## Como os gatilhos aparecem no anúncio (mesma frase, três lugares)
- Card 1 do carrossel e primeira linha do texto: a frase da opção (ex.: "Tenho o terreno, mas não tenho o capital?").
- Opção do formulário: a mesma frase, para o lead se reconhecer.
- Primeira mensagem da Zaya: "Você contou que [frase]".

## O que muda no ClickMax (só com "aprovado")
- Custom field novo "Gatilho (Forms Meta)" recebendo o código da pergunta 1.
- Zaya: abrir a conversa pelo gatilho (um parágrafo por código) e aplicar a tag DOR | <código>.
- Pipeline "Mentoria Zion": as etapas "Dor · ..." já existem (Sem capital, Quer mentoria, Quer parceiro, Não sabe por onde começar); criar "Dor · Terreno serve?" e "Dor · Medo de errar".
- Sincronização hora a hora: aceitar form_name contendo "Diagnóstico do terreno" (já cobre o v2) e mapear a pergunta 1 para o campo novo.
