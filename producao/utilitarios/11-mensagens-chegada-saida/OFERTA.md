# Ferramenta 11 · Kit de Mensagens de Chegada e Saída

Status: arquivos prontos e testados. Nada foi publicado, ativado ou anunciado.

**ClickMax (rascunhos, 06/11/2026):** produto `99a12f38-fff2-43b7-845d-0b56ad7604a0`; oferta `fad5df5a-49fa-442e-aed7-c08cf2f6f92f` (R$ 19, checkout `X4mTsfhUtb`, incompleta: faltam `deliverables` e `sellerStatus`); página `545010c0-a48c-4555-9b73-d501dac3c6a7` em `/kit-mensagens` (rascunho).
Catálogo: `producao/catalogo/CATALOGO.md` (público B · anfitriões e pequenas hospedagens). Também entra nos futuros e-books E05 e E07 e continua à venda separada.

## 1. Tarefa concreta
A cada reserva, enviar as mensagens de confirmação, endereço e acesso, chegada, apoio, saída e agradecimento no dia certo, com as informações corretas da hospedagem, sem reescrever tudo e sem esquecer dados.

**Dor observada (fontes, consultadas em 06/11/2026; itens E5 e E6 do Mapa de Oportunidades):** modelos de mensagem por etapa da jornada são procurados e oferecidos grátis por ferramentas ([Hostfully](https://www.hostfully.com/pt-br/blog/modelos-de-mensagens-do-airbnb-10-scripts-para-cada-etapa-da-jornada-do-hospede/), [Stays](https://stays.net/blog/mensagem-para-hospede-no-airbnb/)); a comunidade do Airbnb discute mensagens programadas e a conversa no WhatsApp ([Comunidade Airbnb](https://community.withairbnb.com/t5/Receber-h%C3%B3spedes/Mensagens-programadas/m-p/1755254)).
**Risco:** há muito modelo grátis. A diferença do kit é montar as mensagens com os dados da hospedagem e da reserva, dar a data de envio e nunca inventar o que falta.
**Base real Zion:** Scripts de Atendimento WhatsApp e Manual de Hospitalidade (Notion, Bíblia Operacional), generalizados. Ficaram de fora, por cautela: levar a conversa da plataforma para outro canal e pedir "5 estrelas".

## 2. Promessa
"Aprenda o passo a passo para enviar, no momento certo, as mensagens de confirmação, acesso, chegada, apoio durante a estadia e saída, com as informações da sua hospedagem."
- **Tempo para começar a usar:** cerca de 15 minutos para a ficha; depois, menos de 1 minuto por reserva.
- **Resultado externo:** avaliações e reservas dependem de muitos fatores. O kit não promete isso.

## 3. Entregáveis (em `dist/`)
| # | Arquivo | O que é |
|---|---|---|
| 1 | `Kit-Mensagens-Zion-EM-BRANCO.xlsx` | Abas Comece aqui, Ficha (hospedagem + reserva), Mensagens (10 textos montados, data de envio e situação) e Modelos |
| 2 | `Kit-Mensagens-Zion-EXEMPLO.xlsx` | Hospedagem e reserva fictícias, 10 de 10 mensagens prontas |
| 3 | `Mensagens-Modelo.pdf` | Os 10 modelos com campos entre colchetes, para copiar à mão (2 páginas) |
| 4 | `Guia-Aprenda-o-Passo-a-Passo.pdf` | Guia de 7 páginas: 4 passos, 2 exercícios, critérios, checklist de conclusão, limitações |
| 5 | `demonstracao/demo-pronta.png` e `demo-falta.png` | Demonstração: a mesma mensagem pronta e com a senha do Wi-Fi faltando |
| 6 | `Ferramenta11-Kit-Mensagens-Zion.zip` | ZIP do produto (itens 1 a 4 + LEIA-ME) |

As 10 mensagens: M01 confirmação · M02 endereço e acesso (2 dias antes) · M03 bom dia do dia da entrada · M04 boas-vindas com acesso e Wi-Fi · M05 apoio (manhã seguinte; "Pule" em estadia de 1 noite) · M06 lembrete da saída (véspera) · M07 dia da saída · M08 agradecimento e pedido de avaliação honesta · M09 resposta a chegada fora do horário · M10 resposta a problema durante a estadia.

### Regras da ferramenta
- Campo obrigatório vazio → a mensagem mostra `[PREENCHA: campo]` e a situação vira "Falta: …". Nada é inventado.
- Campo opcional vazio → a frase inteira sai da mensagem.
- Datas de envio calculadas pela entrada e saída; saída igual ou antes da entrada → "Confira as datas".
- Datas escritas sem a função TEXTO (que muda com o idioma do Excel); textos sem quebra de linha, para colar sem aspas.

## 4. Demonstração de uso (roteiro do vídeo de 20 s)
1. (0–6 s) Aba Ficha: digita o nome do hóspede e as datas.
2. (6–12 s) Aba Mensagens: as datas de envio aparecem; a M04 está "Pronta para copiar".
3. (12–17 s) Apaga a senha do Wi-Fi: a M04 mostra `[PREENCHA: Wi-Fi: senha]` em vermelho.
4. (17–20 s) Texto: "Ela não inventa. Ela avisa o que falta."

## 5. Critérios para conferir o resultado
Ficha com todos os obrigatórios; 10 de 10 prontas numa reserva de teste; datas de envio conferidas; nenhuma mensagem enviada com [PREENCHA]; primeira reserva real atendida com M01 a M08 nas datas indicadas.

## 6. Limitações e dependências
- Monta textos; não envia nem se conecta ao WhatsApp ou às plataformas.
- Regras de cada plataforma sobre mensagens, contato externo e avaliações devem ser conferidas pelo anfitrião.
- Português, uma reserva por vez.
- Testado no LibreOffice. **Não testado** no Excel e no Google Sheets reais, nem no celular.

## 7. Testes executados
`python3 -I tests/test_planilha.py dist` → **26 de 26 verificações passaram**. Os textos recalculados no LibreOffice foram comparados, caractere por caractere, com uma montagem independente em Python em 6 cenários (exemplo, completo, só obrigatórios, senha faltando, aspas e texto longo, vazio). Também verificados: datas de envio, estadia de 1 noite, datas invertidas, contagem de prontas, nenhuma célula com erro em 8 arquivos e maior mensagem com 770 caracteres. Revisão visual do guia, dos modelos e da demonstração (a capa trocou de foto por ter uma pessoa).

## 8. Copy comercial
- **Título:** As mesmas perguntas, toda reserva. As respostas já prontas.
- **Subtítulo:** Preencha uma vez a ficha da sua hospedagem. A cada reserva, as 10 mensagens da chegada à saída aparecem prontas, com o nome do hóspede e o dia de enviar cada uma.
- **Botão:** Quero o meu kit
- **O problema:** "qual é o endereço?", "qual é a senha do Wi-Fi?", "até que horas é o check-out?". Escrever tudo de novo a cada reserva toma tempo, e um dado esquecido vira ligação na hora da chegada.
- **A solução:** uma planilha que monta as mensagens com os seus dados, diz quando enviar cada uma e avisa quando falta alguma informação, em vez de inventar.
- **O que você recebe:** planilha em branco, exemplo preenchido, modelos em PDF para copiar à mão e guia "Aprenda o passo a passo".
- **De onde vem a jornada:** dos scripts de atendimento usados nas unidades da Zion, generalizados. *(Usar só com autorização de Bruno.)*
- **Para quem é:** anfitriões, pousadas, glampings e pequenos hotéis. **Não é para:** quem procura envio automático ou integração com as plataformas.
- **Preço:** R$ 19, pagamento único, Pix ou cartão. Reembolso em 7 dias.

## 9. Perguntas frequentes
- **Envia as mensagens sozinho?** Não. Você copia e cola no WhatsApp ou na plataforma. Se a plataforma tiver mensagens rápidas ou programadas, pode colar lá.
- **Funciona no celular?** Sim, pelo app do Google Sheets ou do Excel. A ficha é mais confortável no computador.
- **Posso mudar os textos?** Pode. Edite depois de colar, sem mudar datas, horários, senha e endereço.
- **E se eu esquecer um dado?** A mensagem mostra [PREENCHA] e não aparece como pronta.
- **Tem em inglês?** Não, por enquanto só em português.
- **É vendido junto com outro produto?** É vendido sozinho. Se entrar num pacote ou e-book, a página vai dizer que também é vendido separadamente.

## 10. Três conceitos de anúncio (Meta, 1080×1350, botão "Saiba mais")
Destino: `https://infoprodutos-zion.clickmax.space/kit-mensagens?utm_source=meta&utm_medium=paid&utm_campaign=ferramenta11&utm_content=<criativo>`
1. **As perguntas de sempre (c11a).** Arte: três balões "Qual o endereço?", "Qual a senha do Wi-Fi?", "Até que horas é o check-out?". Primeira linha: "Responda antes de perguntarem." Chamada: VER O KIT.
2. **Ela não inventa (c11b).** Arte: as duas telas de `dist/demonstracao` lado a lado. Primeira linha: "Faltou um dado? A mensagem avisa, em vez de inventar." Chamada: QUERO MINHAS MENSAGENS.
3. **Calendário da reserva (c11c).** Arte: linha do tempo de M01 a M08 com as datas do exemplo. Primeira linha: "Da confirmação à avaliação, cada mensagem no dia certo." Chamada: APRENDER O PASSO A PASSO.
Regras: sem promessa de avaliações ou reservas; dados fictícios identificados; fotos reais sem pessoas.

## 11. Preço proposto para teste: R$ 19
Mesmo degrau das ferramentas 01 e 17. Concorre com modelos grátis: o valor está na montagem automática, nas datas e na regra de não inventar. Medir custo por venda contra preço menos taxas e impostos.

## 12. Custos de uso e manutenção conhecidos
Comprador: zero. Por venda: taxa do checkout, impostos, reembolsos. Entrega por arquivo, sem servidor. Manutenção: revisar se as plataformas mudarem as regras de mensagens.

## 13. Instruções de entrega (ClickMax)
Mesmo padrão da Ferramenta 17 (projeto Infoprodutos Zion, pagamento único, Pix e cartão, `ZIONACADEMY`, +55 48 6137-1061, reembolso 7 dias). Bruno sobe o ZIP em Produtos → oferta → "Cadastrar E-Books, PDFs ou Arquivos Digitais". Mensagem de acesso: "Seu kit chegou. Comece pelo Guia-Aprenda-o-Passo-a-Passo.pdf e depois preencha a ficha da planilha EM-BRANCO. Dúvidas: +55 48 6137-1061." Conferir o caminho completo: pagamento confirmado → e-mail de acesso → download. Plano B: Hotmart.

## 14. Código-fonte e execução
```
python3 -I src/build_planilha.py dist     # planilhas (mensagens em src/mensagens.py)
python3 -I tests/test_planilha.py dist    # 26 verificações no LibreOffice
python3 -I src/build_docs.py dist build && node src/render.js build dist   # guia, modelos, demonstração
bash src/empacotar.sh                     # ZIP
python3 -I landing/build_landing.py       # página do ClickMax
```
