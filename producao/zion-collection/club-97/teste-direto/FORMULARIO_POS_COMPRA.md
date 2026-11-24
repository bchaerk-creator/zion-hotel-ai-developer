# Formulário DEPOIS da compra (as 9 perguntas restantes)

Rascunho local, 24/11/2026. Criar no ClickMax com `forms_create` só com "aprovado" de Bruno. Os campos de destino são os "Forms Meta" que já existem (chaves em `campos_inscricao.json`). Sem promessa, sem preço, sem reunião.

## Texto de abertura
**Conte um pouco mais sobre o seu terreno para a Zion te conhecer.**
São perguntas rápidas, de múltipla escolha, e levam cerca de 3 minutos. Quanto mais você responder, melhor a Zion entende a sua área. Avaliamos cada ideia, cada região e cada terreno.

## Campos, na ordem

| # | Rótulo | Tipo | Opções | Campo de destino |
|---|---|---|---|---|
| 1 | Você possui: | Escolha única | Terreno em área turística · Área rural ou natural · Hotel ou pousada que deseja expandir · Projeto turístico em desenvolvimento · Já tenho um empreendimento e quero um parceiro | `perfil_area` |
| 2 | Qual a localização do terreno ou projeto? | Texto curto (cidade e estado) | livre, só cidade e estado | `localizacao` |
| 3 | Qual o tamanho aproximado da área? | Escolha única | Até 5.000 m² · 5.000 m² a 20.000 m² · 20.000 m² a 50.000 m² · Mais de 50.000 m² | `area` |
| 4 | Qual o objetivo do projeto? | Escolha única | a conferir com o Meta (as opções não estão nos arquivos) | `objetivo_projeto_meta` |
| 5 | Qual infraestrutura existe hoje no terreno? | Escolha múltipla | a conferir com o Meta | `infraestrutura_meta` |
| 6 | Como está a documentação da área? | Escolha única | Escritura ou matrícula em dia · Só contrato ou posse · Ainda não tenho | `documentacao_meta` |
| 7 | Qual o valor estimado da sua área hoje? | Escolha única | Até R$ 500 mil · De R$ 500 mil a R$ 2 milhões · De R$ 2 milhões a R$ 5 milhões · Acima de R$ 5 milhões | `valor_area_meta` |
| 8 | O que impediu você de desenvolver o terreno até hoje? | Escolha única | a conferir com o Meta | `impedimento_meta` |
| 9 | Você sabe como apresentar o seu projeto a um possível investidor? | Escolha única | Sim · Mais ou menos · Não (sugestão, conferir com o Meta) | `apresentacao_investidor_meta` |

As 3 perguntas da mini-ficha (`falta_papel_meta`, `investimento`, `operador`) não se repetem aqui. Se a mini-ficha for pulada por algum motivo, o formulário pós-compra as pede no fim (campos 10 a 12, mesmas opções).

Para os campos marcados "a conferir com o Meta": abrir o formulário do Meta e copiar o texto exato das opções, para bater com a base de leads. Não inventei opções.

## Texto de agradecimento
**Recebemos as suas respostas. Obrigado!**
A Zion vai conhecer o seu terreno com carinho. O seu acesso à plataforma já está no seu e-mail: comece pelos vídeos e siga os formulários. Se precisar de ajuda, fale com a gente no WhatsApp +55 48 6137-1061.
