# Onboarding proposto · Mini Mentoria de Estruturação Zion

Agente: FUNNEL · 25/11/2026. **Somente proposta.** A turma `087479a3…` e o portal `3ef7a340…` têm compradores ativos e **não foram alterados**. Base: `JORNADA_ENTREGA_MM47.md` (seções 2 e 3, leitura das 3 lições do módulo Onboarding em 25/11). Marcação: **[E]**, **[NC]**.

## 1. O que está lá hoje [E]

| Lição | Problema |
|---|---|
| 1 · "Bem-vindo à plataforma Zion Collection" (vídeo `plataforma-v02.mp4`) | O vídeo, segundo a verificação do CONVERSION, tem quadros com "Land Bank" e "receber investimentos" [NC: o FUNNEL não assistiu]. O nome "Zion Collection" não é o do produto comprado |
| 2 · "Monte o seu dossiê inicial" | Manda "enviar as páginas do seu dossiê para a Zion conhecer o seu projeto": o aluno entende que a Zion recebe e avalia |
| 3 · "Suporte" | Ok [NC: se o chat é monitorado] |

## 2. Texto final proposto da lição nova "Leia primeiro" (primeira lição do módulo Onboarding)

Título: **Leia primeiro: o que você comprou e por onde começar**

> **Você está na plataforma da Mini Mentoria de Estruturação Zion.**
> Esta é uma formação digital autônoma. Você estuda no seu ritmo, durante 12 meses, e monta o Dossiê do seu projeto passo a passo.
>
> **O que você tem aqui**
> 9 módulos e 70 aulas e materiais: aulas gravadas, fichas "Faça agora", e-books por pilar, 2 planilhas de cálculo em branco, o Kit do Investidor (modelos para você preencher), um kit de prompts e o Dossiê, que você gera em PDF no final.
>
> **O que não está incluído**
> Reunião, atendimento individual e consultoria. Calculadoras e simuladores também não fazem parte. Não prometemos investimento, parceria, ocupação, renda ou valorização: o que você leva é o conhecimento e o seu Dossiê.
>
> **Como você entra**
> Use sempre o **mesmo e-mail da compra**. No primeiro acesso você não precisa ter criado senha antes: siga as instruções da tela de entrada. Se pedir um código, ele chega por e-mail. Se o e-mail de acesso não chegar, olhe a caixa de spam e fale com o suporte.
>
> **Por onde começar, em 4 passos**
> 1. Assista ao vídeo de boas-vindas (a próxima aula).
> 2. Abra o módulo "Marco Zero" e leia "Comece aqui · Como usar o curso".
> 3. Faça o seu diagnóstico de partida (ficha "Faça agora").
> 4. Siga os Pilares 1 a 7, na ordem. Em cada um: aula, material e a ficha "Faça agora".
>
> **Seu Dossiê é seu**
> Todas as fichas ficam com você. O Dossiê serve para você organizar o projeto e, se quiser, apresentá-lo a potenciais parceiros e investidores. A Zion não recebe nem avalia o seu Dossiê por esta formação.
>
> **Ajuda e reembolso**
> Dúvida de acesso ou de uso? Use a aula "Suporte" ou o WhatsApp +55 48 6137-1061. Se a formação não for para você, peça o reembolso em até 7 dias da compra, pelo mesmo canal.

[NC] "Se pedir um código": o passo exato do login nunca foi visto (login bloqueado neste ambiente); confirmar na compra de teste e ajustar a frase.
[NC] "A Zion não recebe nem avalia o seu Dossiê": verdadeiro para a oferta de R$ 47 segundo a descrição ("sem reunião e sem atendimento individual"); Bruno decide se mantém o cadastro opcional no banco de áreas (a Zion avalia caso a caso, sem garantia). Se mantiver, acrescentar: "O cadastro do terreno no banco de áreas da Zion é opcional, fora desta formação, a Zion avalia cada caso e não há garantia de resposta, parceria ou investimento".

## 3. Texto proposto para a descrição da lição "Monte o seu dossiê inicial"

> Responda ao diagnóstico, veja o resultado e guarde a página 0 do seu Dossiê. Tudo fica com você, no seu ritmo. Esta lição não envia nada para a Zion.

## 4. Roteiro curto da aula 1 regravada (vídeo de 60 a 90 s)

Tom: voz "nós", direto, sem promessa. Imagem: telas reais da plataforma (`docs/zion-collection/club/telas/`), sem texto sobre foto, sem pessoas apresentadas como clientes, **sem** "Land Bank", "receber investimentos", sócio ou banco de áreas.

| Tempo | Fala | Imagem |
|---|---|---|
| 0:00 a 0:10 | "Bem-vindo à Mini Mentoria de Estruturação Zion. Você tem acesso por 12 meses e estuda no seu ritmo." | Tela de entrada da plataforma com os módulos |
| 0:10 a 0:30 | "Aqui você aprende o passo a passo para estruturar o seu projeto de hospedagem: aulas gravadas, fichas Faça agora, e-books, planilhas em branco, modelos e um kit de prompts." | Passeio pelos módulos, abrir uma ficha "Faça agora" |
| 0:30 a 0:45 | "No final, cada ficha vira uma página do seu Dossiê, que você gera em PDF. O Dossiê é seu, para organizar o projeto e, se quiser, apresentar a potenciais parceiros e investidores." | Tela do Dossiê e do PDF |
| 0:45 a 1:00 | "Para ser claro: aqui não há reunião nem atendimento individual, e não prometemos investimento nem parceria. O que você leva é conhecimento e o seu material." | Cartela simples com a frase (fundo musgo, sem foto) |
| 1:00 a 1:15 | "Comece pelo módulo Marco Zero, em Comece aqui. Depois siga os Pilares 1 a 7. Se tiver dúvida, use a aula Suporte. E o reembolso em até 7 dias está sempre disponível." | Marco Zero, depois a lista de pilares |

Gravação: [NC] quem grava (voz humana ou narração de IA com aviso); não apresentar pessoa como cliente ou equipe sem autorização.

## 5. Como aplicar (com "aprovado" de Bruno; nada feito)

1. Criar a lição nova "Leia primeiro" como **primeira** do módulo Onboarding (`lessons_create`; sem aviso de portal, que dispararia e-mail em massa para todos os membros, inclusive os antigos).
2. Trocar a descrição da lição 2 (`lessons_update`).
3. Substituir o vídeo da lição 1 pelo regravado (a lição só muda no arquivo de vídeo). Até lá, **ocultar** a lição 1 antiga (`lessons_toggle_enabled`) é a opção reversível.
4. Renomear a turma "(R$ 97)" (`classrooms_update`), conforme `JORNADA_ENTREGA_MM47.md`. Acessos permanecem.
5. Reversão: reabilitar a lição 1 e apagar a nova; nenhuma matrícula é alterada.
6. Verificar na compra de teste de Bruno, no celular.
