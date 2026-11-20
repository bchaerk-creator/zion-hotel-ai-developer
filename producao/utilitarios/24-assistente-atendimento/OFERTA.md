# Ferramenta 24 · Assistente de IA para Atendimento

Status: arquivos prontos e testados. **Oferta enviada para aprovação em 20/11/2026** na rodada diária automática. A página fica em rascunho até a oferta estar ativa.

**ClickMax:**
- produto `1dfce039-31a8-4266-b3be-9f212bb568ee`;
- oferta `8ea1c87b-3309-475c-85e4-2764d3a7fbac` (R$ 19, checkout `VSiwxpwGew`), com status `pending` desde 20/11 às 04h56 UTC e sem erro de sincronização;
- página `abfff20b-a876-4f2d-9e8e-5e915d1e2586` em `/assistente-atendimento` (rascunho).

Entrega: 4 arquivos e a página de acesso, em `docs/p/adbc67069af26ae0/assistente-24/`, ligados à oferta.

**Por que a 24 nesta rodada:**
- 01, 21, E08, 25, 26 e 27 aguardam decisão de Bruno, e E05 e E06 aguardam os PDFs A01 a A10.
- A 09 repetiria quase tudo da Ferramenta 01.
- A 24 é a última ferramenta do público B que ainda não existe.

**Sobreposição verificada:**
- A Ferramenta 11 traz mensagens prontas de chegada e saída. A 24 monta e testa a instrução de um assistente que responde perguntas livres.
- Os prompts da Jornada 2 revisam materiais do membro; não atendem hóspedes.
- A 21 (mensagens de reservas) segue parada.

Não há alegação de que o kit vem da rotina das unidades da Zion. Os números de emergência citados são os nacionais: SAMU 192, Bombeiros 193 e Polícia 190.

## 1. Tarefa concreta
Dar a um assistente de IA uma instrução que só use as informações da hospedagem, diga "vou confirmar" quando não souber, não prometa nada e não passe senhas. Depois, testar o assistente antes do primeiro hóspede.
- **Evidência:** item 24 do Catálogo ("testar respostas com informação faltando"). Nenhuma pesquisa de mercado e nenhum número externo.

## 2. Promessa
"Aprenda o passo a passo para montar e testar as instruções de um assistente de IA que responde hóspedes só com as informações da sua hospedagem, sem inventar e sem prometer o que você não autorizou."
- Tempo para começar: cerca de 15 minutos para a ficha e 15 minutos para os 12 testes.
- Nenhuma instrução garante que a IA nunca erre.

## 3. Entregáveis
| Arquivo | O que é |
|---|---|
| `Assistente-Atendimento-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Ficha (17 campos, 8 obrigatórios), Instrução (montada) e Teste (12 perguntas) |
| `Assistente-Atendimento-Zion-EXEMPLO.xlsx` | "Casa do Ipê" (fictícia), com estacionamento e café vazios de propósito, e o resultado real do teste: 12 de 12 |
| `Roteiro-de-Teste.pdf` | As 12 perguntas e o que conferir em cada uma (1 página) |
| `Guia-Aprenda-o-Passo-a-Passo.pdf` | 7 páginas: ficha, instrução, 8 regras, teste, exercícios, critérios e limitações |
| `demonstracao/` | Telas da Ficha e do Teste |
| `Ferramenta24-Assistente-Atendimento-Zion.zip` | Pacote completo |

### Regras da planilha
**Situação da ficha:**
- "Faltam N campo(s) obrigatório(s)";
- "Tire senhas e códigos da ficha", se algum campo tiver "senha:", "código:" ou "codigo:", sem diferença entre maiúsculas e minúsculas;
- "Pronta para copiar".

**Instrução:**
- papel e tom;
- as 8 regras fixas (a 8ª, de emergência, leva o contato do anfitrião);
- as informações da ficha: campo obrigatório vazio aparece como [PREENCHA], e campo opcional vazio fica de fora.

**Teste:** para cada pergunta ligada a um campo, a planilha mostra "Responde com a ficha: …" ou, se o campo estiver vazio, "Não inventa: diz que vai confirmar". As perguntas 9 a 12 (desconto, senha, piscina inexistente, emergência) têm o comportamento esperado fixo.

**O que fazer agora**, na ordem:
1. Complete a ficha antes de testar
2. Faça os N testes que faltam
3. Ajuste a ficha e refaça os que falharam
4. Pronto: o assistente passou nos 12 testes

## 4. Testes
**Planilha:** `python3 -I tests/test_planilha.py dist` → **21 de 21**.
- **O que é comparado** com uma montagem independente em Python: situação da ficha, campos faltando, as 27 linhas da instrução, o comportamento esperado de cada pergunta, as contagens e a leitura.
- **Cenários:** o exemplo, a versão em branco, 8 aleatórios (inclusive com senha escrita em maiúsculas), ficha completa, só os obrigatórios, sem o contato, senha escrita, texto longo com espaços e ficha vazia.
- Nenhuma célula com erro em 16 arquivos.

**Assistente de IA real:** a instrução do exemplo foi dada a um agente de IA novo (modelo Claude Haiku), sem outro contexto. Ele respondeu às 12 perguntas em conversas separadas: **12 de 12 passaram.**
- Estacionamento, café e piscina receberam "vou confirmar".
- Não deu desconto nem passou senha ou código.
- Na emergência, indicou SAMU 192, Bombeiros 193 e Polícia 190, e depois o anfitrião.

Respostas registradas em `tests/TESTE_IA_2026-11-20.md`. Limite: um modelo e uma rodada; o comprador refaz o teste no assistente dele.

Revisão visual do guia, do roteiro, das telas, da capa e da página no celular (390 px, sem rolagem lateral).

**Não testado:** ChatGPT, Gemini e ferramentas de mensagens; Excel e Google Sheets reais; compra no checkout.

## 5. Copy (ECROI)
- **Espelhamento:** "E se a IA inventar uma piscina que você não tem?"
- **Colapso de crença:** "é só colar umas linhas no ChatGPT". Ela responde rápido, às vezes rápido demais.
- **Reencadramento:** de confiar no assistente para testar o assistente.
- **Inevitabilidade:** ficha sem senhas + regras fixas + 12 testes = menos surpresas antes do primeiro hóspede.
- **Resultado educacional:** você aprende a dizer ao assistente o que ele pode e não pode dizer, e a conferir antes de usar.

Botão: "Quero montar o meu" · R$ 19, pagamento único, reembolso em 7 dias.

## 6. Perguntas frequentes
- Serve para qualquer assistente que aceite instruções.
- Não garante que a IA nunca erre.
- Não se conecta a plataformas.
- Não precisa programar.
- Funciona no celular.

## 7. Três anúncios
Formato 1080×1350, botão "Saiba mais", `utm_campaign=ferramenta24`.
1. **c24a · Piscina:** "E se a IA inventar uma piscina que você não tem?" + tela do Teste (dados fictícios). Primeira linha: "Teste o seu assistente antes do primeiro hóspede."
2. **c24b · Senha:** "O código do cofre não é resposta automática." Primeira linha: "Ficha que trava se encontrar senha."
3. **c24c · Vou confirmar:** tela da Ficha. Primeira linha: "Quando não sabe, ele diz que vai confirmar."

## 8. Preço, custos e entrega
- **Preço:** R$ 19.
- **Custos por venda:** taxa do checkout, impostos e reembolsos.
- **Entrega:** 4 arquivos e a página de acesso. Manutenção baixa: revisar as regras se os assistentes mudarem muito.
- **Indicadores:** visitas à página, conversão do checkout, reembolsos e custo por venda (quando houver anúncio aprovado).

## 9. Execução
```
python3 -I src/build_planilha.py dist && python3 -I tests/test_planilha.py dist
python3 -I src/build_docs.py dist build && node src/render.js build dist && node src/render.js build dist
bash src/empacotar.sh && python3 -I landing/build_landing.py
```

## Envio para aprovação
20/11/2026, rodada diária:
- os 4 arquivos e a página de acesso foram conferidos no ar (status 200) e ligados à oferta;
- `offers_get_incomplete_reason` voltou vazio;
- a oferta foi enviada para aprovação e está `pending`, sem erro de sincronização.
