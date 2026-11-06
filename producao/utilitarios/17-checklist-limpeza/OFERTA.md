# Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação

Status: arquivos prontos e testados. Nada foi publicado, ativado ou anunciado.

**ClickMax (rascunhos, 06/11/2026):** produto `9545b75a-1599-4032-bc2e-c2a4a8d3f20f`; oferta `08ad22e8-9f9a-4244-856f-1bca05234924` (R$ 19, checkout `uB0Db7Gpg4`, status incompleta: faltam `deliverables` e `sellerStatus`); página `023476bb-0ea7-41b2-ba99-73c62a5aa94c` em `/checklist-limpeza` (rascunho, não publicada). Fonte da página: `landing/build_landing.py` → `landing/dist/clickmax.html`.
Catálogo: `producao/catalogo/CATALOGO.md` (público B · gestores, equipes e anfitriões). Também entra no futuro e-book E08 e continua à venda separada.

## 1. Tarefa concreta
Na troca de hóspede, limpar a unidade sempre na mesma sequência, conferir com critérios que outra pessoa consegue verificar e **só liberar** quando todo item obrigatório estiver feito e aprovado, deixando registrado quem fez, quem conferiu e o que ficou pendente.

**Dor observada (fonte):** padronizar o status do quarto, ter checklist por tipo de limpeza e reinspecionar são práticas recomendadas em governança ([SiteMinder](https://www.siteminder.com/pt/r/housekeeping-na-hotelaria/), [SafetyCulture](https://safetyculture.com/library/hospitality/fo-sa-047-check-list-de-check-out-governanca-xbej9nnwqubmo8h5), consultados em 06/11/2026, item E7 do Mapa de Oportunidades). **Base real Zion:** sequência de 21 passos do Manual de Governança e Limpeza (Notion, Bíblia Operacional Zion), generalizada.
**Hipótese (sem fonte):** avaliações baixas por limpeza e retrabalho com equipe nova são frequentes entre pequenas hospedagens. Não temos número sobre isso.

## 2. Promessa
"Aprenda o passo a passo para limpar, conferir e liberar cada unidade com o mesmo padrão, sabendo quem fez, quem conferiu e o que ficou pendente."
- **Tempo para começar a usar:** cerca de 20 minutos para ajustar o modelo; depois, a própria troca.
- **Resultado externo:** melhores avaliações dependem da execução e de outros fatores. A ferramenta não promete isso.

## 3. Entregáveis (todos em `dist/`)
| # | Arquivo | O que é |
|---|---|---|
| 1 | `Checklist-Limpeza-Zion-EM-BRANCO.xlsx` | Arquivo utilizável: modelo-padrão de 33 itens em 8 ambientes, abas Comece aqui, Ajustes, Modelo, Troca, Pendências e Histórico |
| 2 | `Checklist-Limpeza-Zion-EXEMPLO.xlsx` | Exemplo preenchido (pessoas e unidades fictícias) |
| 3 | `Checklist-Imprimivel.pdf` | Versão em papel, 2 páginas, com assinaturas |
| 4 | `Guia-Aprenda-o-Passo-a-Passo.pdf` | Guia de 8 páginas: 5 passos, 3 exercícios, critérios de conferência, checklist de conclusão, limitações |
| 5 | `demonstracao/demo-bloqueada.png` e `demo-liberada.png` | Demonstração de uso (tela de celular), com os valores calculados pela própria planilha |
| 6 | `Ferramenta17-Checklist-Limpeza-Zion.zip` | ZIP exclusivo do produto (itens 1 a 4 + LEIA-ME) |

### Regras da ferramenta
- Item obrigatório só está resolvido com Execução = Feito **e** Conferência = Aprovado. "Não se aplica" em obrigatório conta como pendente.
- Item opcional não feito ou reprovado fica em "Atenção" e não bloqueia.
- Ajuste "Exigir conferente diferente" (padrão Sim): bloqueia se o mesmo nome aparece nos dois campos (ignora maiúsculas e espaços). Com "Não", quem trabalha sozinho confere o próprio trabalho.
- Pendências: Resolvida, Aberta, Sem prazo ou Atrasada (prazo menor que a data de referência; em branco = hoje).

## 4. Demonstração de uso (roteiro do vídeo de 20 s, a gravar no celular)
1. (0–5 s) Aba Troca do exemplo: dedo rola a lista; topo vermelho "NÃO LIBERAR: 1 item obrigatório pendente".
2. (5–12 s) Zoom na linha do chuveiro: Conferência "Reprovado", Situação "PENDENTE".
3. (12–18 s) Troca para "Aprovado": o topo fica verde "LIBERADA PARA O PRÓXIMO HÓSPEDE".
4. (18–20 s) Texto: "Só libera quando o obrigatório está feito e conferido."
As imagens estáticas desse antes e depois já estão em `dist/demonstracao/`.

## 5. Critérios para conferir o resultado (comprador)
Modelo sem itens inexistentes e com critério verificável em cada obrigatório; cabeçalho completo; todas as linhas marcadas; liberação só com "LIBERADA"; toda pendência com responsável e prazo; uma linha de Histórico por troca. Detalhes na página 8 do guia.

## 6. Limitações e dependências
- Organiza e registra; a qualidade da limpeza depende de quem executa e confere.
- Não substitui normas sanitárias, de segurança, de piscinas e equipamentos, nem orientações de fabricantes. Não prescreve produtos.
- Uma troca por aba; o Histórico depende de o usuário copiar o resultado.
- Precisa de Excel, Google Sheets ou LibreOffice (no celular, app do Google Sheets ou Excel). Listas suspensas e cores funcionam nos três; foi testado no LibreOffice.

## 7. Testes executados
- `python3 -I tests/test_planilha.py dist` → **31 de 31 verificações passaram** (recalculado no LibreOffice e comparado com uma regra independente em Python): exemplo, versão em branco, cabeçalho incompleto, mesma pessoa, anfitrião sozinho, "Não se aplica" em obrigatório, modelo sem obrigatórios, item novo com linhas vazias no meio, horários invertidos, pendências (resolvida, atrasada, sem prazo), histórico e tempo médio, 8 cenários aleatórios e nenhuma célula com erro em 18 arquivos.
- Guia e checklist imprimível: revisão visual página a página (uma tabela que invadia o rodapé foi corrigida).
- **Não testado:** abertura no Excel e no Google Sheets reais (não há acesso aqui) e uso em celular de verdade. Pendência para Bruno: abrir o arquivo de exemplo no Google Sheets e no app do celular.

## 8. Copy comercial
- **Título:** Sua unidade está mesmo pronta para o próximo hóspede?
- **Subtítulo:** Um checklist de limpeza e inspeção que separa quem faz de quem confere e só mostra "liberada" quando tudo o que é obrigatório foi feito e aprovado.
- **Botão:** Quero o meu checklist
- **O problema:** a limpeza parece feita, mas o chuveiro está frio, o ralo ficou com cabelo ou faltou papel. Quem limpou não viu, e quem chega vê. Sem um padrão escrito e uma conferência, cada troca depende da memória de alguém.
- **A solução:** uma planilha pronta com 33 itens em 8 ambientes, que você ajusta à sua unidade. Quem limpa marca o que fez. Quem confere aprova ou reprova. A planilha mostra se a unidade pode ser liberada e guarda as pendências e o histórico.
- **O que você recebe:** planilha em branco com o modelo pronto, exemplo preenchido, versão para imprimir e guia "Aprenda o passo a passo" com exercícios.
- **De onde vem a sequência:** da rotina de troca usada nas unidades da Zion, generalizada para qualquer hospedagem. *(Usar só com autorização de Bruno.)*
- **Para quem é:** pousadas, glampings, pequenos hotéis e anfitriões, com equipe ou sozinhos. **Não é para:** quem procura um sistema com aplicativo e notificações.
- **Preço:** R$ 19, pagamento único, Pix ou cartão. Acesso ao arquivo após o pagamento confirmado. Reembolso em 7 dias.

## 9. Perguntas frequentes
- **Funciona no celular?** Sim, pelo app do Google Sheets ou do Excel. Para preencher o modelo pela primeira vez, o computador é mais confortável.
- **Trabalho sozinho. Serve?** Serve. Na aba Ajustes, marque "Não" em "Exigir conferente diferente" e faça a conferência depois de terminar.
- **Minha unidade tem itens diferentes.** O modelo é editável: apague, acrescente e marque o que é obrigatório.
- **Diz quais produtos usar?** Não. Produtos e proteção são definidos pelo responsável, seguindo o rótulo.
- **Garante nota 5?** Não. Ajuda a não esquecer etapas e a conferir; a avaliação depende de muitos fatores.
- **É vendida junto com outro produto?** Ela é vendida sozinha. Se entrar em um pacote ou e-book, a página vai dizer que também é vendida separadamente.

## 10. Três conceitos de anúncio (Meta, 1080×1350, botão "Saiba mais")
Destino: `https://infoprodutos-zion.clickmax.space/checklist-limpeza?utm_source=meta&utm_medium=paid&utm_campaign=ferramenta17&utm_content=<criativo>`
1. **Antes e depois (c17a).** Arte: as duas telas de `dist/demonstracao` lado a lado, "NÃO LIBERAR" e "LIBERADA". Primeira linha: "Só libere a unidade quando o obrigatório estiver feito e conferido." Chamada na arte: VER O CHECKLIST.
2. **O detalhe que o hóspede vê (c17b).** Arte: foto real sem pessoas (op04, banheira) com "Quem limpou não viu. Quem chega vê." Primeira linha: "Um checklist que separa quem faz de quem confere." Chamada: QUERO PADRONIZAR A LIMPEZA.
3. **Equipe nova (c17c).** Arte: lista de 8 ambientes com marcações. Primeira linha: "Equipe nova? Entregue a sequência e o critério de cada item." Chamada: APRENDER O PASSO A PASSO.
Regras: sem promessa de avaliações ou reservas; dados fictícios identificados; fotos reais da Zion identificadas, nunca imagem gerada como real.

## 11. Preço proposto para teste: R$ 19
- Degrau de entrada da escada (ferramentas R$ 19 → Arsenal R$ 27 → Trilhas), igual à Ferramenta 01.
- Alternativa a testar depois: R$ 27 para "versão equipe", só se houver algo a mais de verdade (por exemplo, treino do primeiro turno). Não criar preço "de".
- Num ticket de R$ 19, taxas do checkout e impostos pesam proporcionalmente mais e o custo do anúncio por venda pode passar do preço. Medir custo por venda contra preço menos taxas e impostos.

## 12. Custos de uso e manutenção conhecidos
- **Comprador:** zero (Excel, Google Sheets ou LibreOffice gratuito).
- **Por venda:** taxa do checkout (ClickMax ou Hotmart), impostos e reembolsos.
- **Entrega:** arquivo anexado à oferta, sem servidor.
- **Manutenção:** baixa. Revisar o modelo se surgirem dúvidas recorrentes no suporte.

## 13. Instruções de entrega (ClickMax)
Projeto **Infoprodutos Zion** `8d1152a4-4490-4666-bcb5-582b75c82660`. Padrão: pagamento único, Pix e cartão à vista, `softDescriptor` ZIONACADEMY, `supportPhone` +55 48 6137-1061, reembolso 7 dias.
1. Produto e oferta novos "Ferramenta 17 · Checklist de Limpeza, Inspeção e Liberação", R$ 19.
2. Entrega por arquivo: Bruno sobe o ZIP em Produtos → oferta → "Cadastrar E-Books, PDFs ou Arquivos Digitais" (ou `offers_add_file_delivery` com URL pública, se Bruno autorizar publicar o ZIP).
3. Página: molde `producao/academy01/landing/`, com `data-cx-section`, `data-cx-cta` e `<div data-cx-checkout></div>`; spans com cor explícita.
4. Mensagem de acesso: "Seu checklist chegou. Comece pelo arquivo Guia-Aprenda-o-Passo-a-Passo.pdf e depois abra a planilha EM-BRANCO. Dúvidas: +55 48 6137-1061."
5. Conferir o caminho completo: pagamento confirmado → e-mail de acesso → download do ZIP. Tag isolada não comprova entrega.
6. Enviar para aprovação só com `offers_get_incomplete_reason` vazio. Com o vendedor em análise, nenhum checkout vende.
Plano B: Hotmart, com o mesmo ZIP.

## 14. Código-fonte e execução
```
python3 -I src/build_planilha.py dist         # gera as duas planilhas
python3 -I tests/test_planilha.py dist        # 31 verificações no LibreOffice
python3 -I src/build_docs.py dist build       # HTML do guia, imprimível e demo (valores recalculados)
node src/render.js build dist                 # PDF e PNG (Playwright)
bash src/empacotar.sh                         # ZIP do produto
```
