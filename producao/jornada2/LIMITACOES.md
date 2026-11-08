# Jornada 2 · Limitações conhecidas e proposta de persistência (ZAIOS)

## 1. O que o membro consegue fazer sozinho hoje
- Responder a ficha, ver o resultado em cinco partes, ajustar a ação, baixar o PDF, voltar depois e continuar de onde parou (no mesmo aparelho e navegador).
- Fechar o mês na planilha (Excel, Google Sheets ou LibreOffice) e guardar o histórico mês a mês.
- Ver, na página de ferramentas da jornada, quais fichas já fez (marcação "Feita" lida do próprio aparelho).

## 2. Limitações
| Limitação | Efeito | Por quê |
|---|---|---|
| As respostas ficam só no `localStorage` do navegador | Trocou de celular ou limpou o navegador: perdeu o diagnóstico (fica só o PDF baixado). A equipe Zion não vê o resultado. | Mesmo mecanismo da Trilha 1, mantido por decisão do comando 01. Não há servidor. |
| O ClickMax não hospeda formulário interativo dentro da aula | A ficha abre por link externo (aba Materiais ou botão), como na Trilha 1. | Tipos de aula do ClickMax: vídeo, texto, documento, link, banner. |
| O progresso da aula no ClickMax é "assistida ou não" | O critério de conclusão do Marco Zero (ação com prazo + PDF) vive na ficha, não no ClickMax. | O ClickMax não recebe dados da ficha. |
| Nenhum envio de dados pessoais | Diferente das fichas da Trilha 1 (que enviam a página do Dossiê ao Land Bank), a ficha de Gestão não envia nada. | Não há consentimento nem finalidade definidos para dados de gestão; o comando pede não mexer no Land Bank. |
| A narração dos vídeos é sintética | Voz neural em português; Bruno pode regravar com o roteiro. | Produção sem câmera. |
| A planilha não prevê nem compara com o mercado | Só calcula o que o membro lança. | Regra "sem invenção". |
| Fontes: RevPAR e ADR não definidos nas fontes Zion | Usamos "diária média" e "receita por noite disponível" com definição-padrão, dita como tal. | Mapa de fontes. |

## 3. Proposta de persistência para o ZAIOS (prioridade 1 do plano mestre)
1. **Um endpoint de resultados** (`POST /resultados`) que recebe `{membro, jornada, modulo, ficha, versao, estado, resultado, concluido, quando}`; o `estado` é o mesmo objeto que hoje vai ao `localStorage`.
2. **Identidade do membro** pelo e-mail da área de membros (já pedido na ficha), com consentimento explícito no primeiro envio ("guardar o meu diagnóstico na minha conta Zion") e aviso de privacidade.
3. **Na ficha**, um botão "Guardar na minha conta" ao lado de "Baixar PDF"; sem rede, continua funcionando só no aparelho (modo atual). Ao abrir em outro aparelho, "Recuperar o meu diagnóstico" pelo e-mail + código enviado por WhatsApp (template já aprovado no ClickMax pode ser reaproveitado).
4. **Consolidação**: uma página por membro com as páginas do Plano de Gestão (0 a 7), o estado de cada critério de conclusão e o PDF final montado no servidor.
5. **Acompanhamento Zion 360°**: a equipe Zion vê os entregáveis por marco (semanas 2, 6 e 12) e deixa um comentário por página; o membro recebe aviso no WhatsApp. Nenhuma visão da equipe sobre quem não contratou o acompanhamento.
6. **Compatibilidade**: a chave `zion-t2-marco-zero` e o formato do estado já estão prontos para esse envio (campos `nome`, `email`, `hospedagem`, `situacao`, `quem`, `cinco`, `areas`, `rotina`, `tempo`, `saida`, `acao`, `prazo`, `pdf`). A lógica em `src/logic.js` roda igual no servidor (Node) para recalcular a nota.
