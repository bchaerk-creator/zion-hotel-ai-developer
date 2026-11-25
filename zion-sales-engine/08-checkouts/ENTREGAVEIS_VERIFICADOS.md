# Entregáveis verificados · Mini Mentoria de Estruturação Zion (R$ 47)

Agente: ZION CONVERSION · 25/11/2026 · ordem P0 de coerência comercial. Verificação **por leitura** (nenhuma escrita) no ClickMax. [E] evidência, [H] hipótese, [NC] não confirmado.
Fontes lidas: `offers_get 0c71eeba…`, `products_get cbbb5fb1…`, `portals_get 3ef7a340…`, `classrooms_details 087479a3…` (conteúdo `79d3e792…`, 9 módulos, 70 aulas lidas uma a uma), arquivos do repositório em `docs/trilha1/`.
Regra: nenhum texto de venda afirma algo que não esteja na coluna "texto permitido".

## 1. Tabela de verificação
| Item | Anunciado onde | Existe? | Evidência | Texto permitido |
|---|---|---|---|---|
| Nome do produto | oferta, produto, páginas | Hoje oferta e produto se chamam "Mini Mentoria de Estruturação" (sem "Zion") [E] | `offers_get` name; `products_get` name | "Mini Mentoria de Estruturação Zion" nas páginas; o nome exato único no checkout depende de renomear a oferta (ver CHECKOUT_LIMPO_MM47.md) |
| Preço R$ 47 | tudo | Sim [E] | `originalPrice 4700`, `newPrice` null, BRL | "R$47" / "R$ 47" |
| Pagamento único, sem mensalidade | tudo | Sim [E] | `paymentConfig.recurrence` null, `isRecurrent` false | "pagamento único, sem mensalidade" |
| Pix e cartão | oferta, checkout | Sim [E]; cartão só à vista (1x); boleto desligado | `pix.active` true; `credit.active` true `installments` 1; `boleto.active` false | "Pix ou cartão de crédito à vista" (não dizer "parcelado" nem "boleto") |
| Acesso de 12 meses | oferta | Sim [E] | `accessTime` 12 `month` no conteúdo `79d3e792…`; `defaultAccessDuration` 12 | "acesso por 12 meses" |
| Garantia 7 dias | oferta | Sim [E] | `limitToRefund` 7 | "reembolso em até 7 dias, como prevê o Código de Defesa do Consumidor" |
| 9 módulos | oferta | Sim [E] | Onboarding, Marco Zero, Pilares 1 a 7 = 9 | "9 módulos" |
| 70 aulas e materiais | oferta | Sim [E], 70 itens, todos `enabled` | 3+10+8+8+8+9+8+8+8 = 70 | "70 aulas e materiais" (nunca "70 aulas em vídeo": só 26 são vídeo) |
| Aulas gravadas | oferta | Sim [E] | 26 itens do tipo `video` (16 vídeos numerados, 1 extra do Pilar 4, 8 tutoriais, 1 boas-vindas) | "aulas gravadas" |
| Aulas interativas | páginas | Sim [E] | 9 itens "Aula interativa" (links em `docs/trilha1/apresentacao/`) | "aulas interativas com exercícios" |
| Fichas "Faça agora" | oferta | Sim [E] | 10 itens "Faça agora" (diagnóstico, 7 fichas, Dossiê) | "fichas interativas 'Faça agora'" |
| E-books por pilar | oferta | Sim [E] | 8 itens "E-book" (Marco Zero + Pilares 1 a 7, PDF) + 5 "Aprofundamento · E-book completo" (Pilares 1 a 5) | "e-books por pilar" |
| Aulas em slides | (novo) | Sim [E] | 5 "Aprofundamento · Aula de 40 slides" (Pilares 1 a 5) | "aulas em slides de aprofundamento (Pilares 1 a 5)" |
| 2 planilhas de cálculo em branco | oferta | Sim [E] | lição `d3ae8d55` (Orçamento de Abertura, EM-BRANCO.xlsx) e `05c0bdc1` (Estudo de Massas e Viabilidade, EM-BRANCO.xlsx); ambos os arquivos existem em `docs/trilha1/materiais/planilhas/` | "2 planilhas de cálculo em branco, para você preencher" |
| Kit do Investidor (modelos) | oferta | Sim [E] | lição `78a3f24f`, seis peças: teaser, one-pager, pitch, masterplan de viabilidade, plano conceitual, marca; guia em `docs/trilha1/materiais/kit-investidor/` | "Kit do Investidor: guia e modelos para montar suas peças de apresentação" |
| Kit de prompts | oferta | Sim [E] | lição `83e4db3a`, "nove comandos prontos" para ChatGPT ou Claude | "kit com 9 comandos prontos para usar com IA (ChatGPT ou Claude, o comprador usa a sua própria conta)" |
| Dossiê de Desenvolvimento (cada ficha vira uma página; PDF no final) | oferta | Sim [E] | lições "Faça agora · Dossiê" (`01ced15d`), "Monte o seu dossiê inicial" (`b12e98f3`); descrições citam páginas 0 a 7 e PDF | "cada ficha vira uma página do seu Dossiê; no final você gera o PDF" |
| Tutoriais em vídeo das fichas | (novo) | Sim [E] | 8 itens "Tutorial em vídeo" | "tutoriais em vídeo de como preencher cada ficha" |
| Chat de suporte | oferta | Sim [E], link de chat dentro da plataforma | lição `c1fc7088` | "suporte dentro da plataforma e pelo WhatsApp" (WhatsApp: `supportPhone` da oferta e `supportUrl` do portal) |
| Acesso sem criar senha no 1º acesso | páginas | Sim [E] | `firstAccessWithoutPass` true, `allowSimplePass` true | "primeiro acesso sem criar senha" |
| **E-mail com o acesso** | obrigado, páginas | **[NC]**: o fluxo de boas-vindas está em rascunho e o ciclo compra aprovada → acesso nunca foi provado para a oferta de R$ 47 | oferta tem 1 entrega `internal_membership` (portal + turma corretos) [E]; envio de e-mail não verificado | "o acesso é liberado com o e-mail da compra" (funciona nos dois casos); NÃO escrever "você receberá um e-mail" |
| Calculadoras / simuladores | oferta antiga | **Não como produto da turma.** Há aulas e fichas dentro da plataforma que citam "equalize no simulador" (Pilares 1 e 2, 4 a 7, nas lições `0481b040`, `d159ed5d`, `182d507a`, `9895ce66`, `b94b3b56` e nas aulas interativas); é um recurso interno da ficha, ainda não confirmado funcionando na prática [H, o código existe em `docs/trilha1/pilar4..7`] | descrições das lições; `docs/trilha1/` | **Não afirmar** "calculadoras" nem "simuladores" como entregável. Se Bruno testar e aprovar, texto possível: "nas fichas você ajusta os números e vê o efeito" |
| Mentor de IA da Zion nas fichas | (não anunciado) | Citado nas descrições das lições [E-descrição], funcionamento não testado [NC] | lições "Faça agora" | Não usar nas páginas de venda |
| Cadastro do terreno no banco de áreas | páginas | Existe como lição opcional (formulário externo no Airtable) [E] | lição `6a3d7c71` | só como opcional, em um lugar discreto, "a Zion avalia cada caso; sem garantia". Não é entregável do produto e não aparece no bloco de oferta |
| Reunião, atendimento individual, consultoria | — | **Não existe** | `offers_get` description: "Sem acompanhamento individual e sem reunião" | só em negação |
| Investimento, parceria, sócio, rede de investidores | — | **Não é entregável** | idem | só como "possibilidade sujeita à análise, não garantia" ou, preferivelmente, "preparar para apresentar a potenciais parceiros e investidores" |
| Certificado | — | Não (`issueCertificate` false) [E] | conteúdo `79d3e792…` | não mencionar |
| Comunidade, mentoria ao vivo | — | Não [E] | nenhuma lição ou módulo | não mencionar |

## 2. O que NÃO pode ser afirmado
1. Calculadoras, simuladores, ferramentas de cálculo online (só as 2 planilhas em branco, e o "simulador" interno das fichas está como [H]).
2. "Receberá um e-mail com o acesso" até Bruno testar o fluxo (o texto seguro é "acesso liberado com o e-mail da compra").
3. Reunião, ligação, conversa, atendimento, consultoria, avaliação do projeto pela equipe, "nossa equipe entrará em contato".
4. Receber investimentos, virar sócio, parceiro garantido, rede de investidores, retorno, ocupação ou renda.
5. "Inscrição", "taxa de inscrição", "cadastro" como produto.
6. "70 aulas em vídeo", "parcelamento", "boleto", "certificado", "comunidade".
7. "Mentor de IA" e "gera diagnóstico com IA" como promessa de venda (descrito nas lições, não testado por este agente).

## 3. Achados fora do texto de venda (ação de Bruno, nada foi alterado)
- **Lição 1 do Onboarding ("Bem-vindo à plataforma", `plataforma-v02.mp4`)** é o mesmo vídeo cujos quadros, segundo a auditoria do CREATIVE, mostram "Zion Land Bank" e "receber investimentos na sua área". Está dentro do produto que o comprador recebe: incoerência de entrega. Sugestão: regravar conforme `06-criativos/ROTEIRO_VSL.md` ou ocultar a lição (`lessons_toggle_enabled`, com "aprovado").
- **Nome da turma "Plataforma de estruturação (R$ 97)"** (`087479a3…`) e título do conteúdo "Plataforma de estruturação Zion Collection": o nome interno com "R$ 97" pode aparecer ao aluno na área de membros [NC]. Sugestão: renomear a turma (`classrooms_update`, "aprovado"); os acessos dos compradores de R$ 97 permanecem.
- **Aulas dizem "enviar ao banco de áreas da Zion"** em várias descrições: é opcional e já está com "a Zion avalia cada caso". Manter, mas nunca como benefício de venda.
- **Descrição da oferta (1000 caracteres)** já está coerente (sem reunião, parceria como possibilidade, 12 meses, reembolso 7 dias, kits como modelos).
- O e-mail de suporte da oferta é dado pessoal e não foi copiado para este repositório.
- `offers_get` mostra `thumbnail` = `product-placeholder.png` e `checkoutTitle` null: o checkout tende a mostrar o nome da oferta com imagem genérica.

## 4. Reversão
Somente leitura: nada a reverter.
