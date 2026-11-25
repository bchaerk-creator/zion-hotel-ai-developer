# Brief editorial · guias aprofundados da Mini Mentoria de Performance Hoteleira (Raio-X da Hospedagem)

Cada módulo (1 a 7) tem um guia. O ZIP original trazia 33 páginas por guia com o mesmo texto genérico repetido em todas as perguntas. O objetivo agora é **aprofundar**: cada pergunta ganha explicação, passo a passo de coleta, exemplo resolvido, erro comum, critério para marcar ausente/parcial/comprovado e verificação.

## Fontes (leia só o seu módulo)
- `fontes/formularios.json` → as 10 perguntas do módulo (campos `question`, `topic`, `procedure`, `evidence`, `action`).
- `fontes/roteiros_7_aulas.md` → roteiro da aula do módulo (tom e ordem).
- `src/meta.json` → calculadora ligada a cada pergunta (`calc`: C1 a C7) e se é item crítico de segurança/legalidade.
- `fontes/COMANDO_MESTRE.md` → regras gerais do produto.

## Público e tom
Donos e gestores de Airbnb, casas, apartamentos, chalés, pousadas e glampings. **Não escreva como se fosse só para glamping ou bubble.** Português brasileiro simples, "você", frases curtas, sem jargão sem explicação. Pense em quem lê no celular.

## Regras inegociáveis
- **Sem invenção:** nenhum número de mercado, pesquisa, benchmark, porcentagem "típica do setor", depoimento, caso real ou resultado. Exemplos numéricos são sempre **dados fictícios** e o texto do exemplo começa com `Dados fictícios:`.
- **Sem promessa** de reservas, ocupação, renda, lucro, investimento ou valorização. Use "pode", "ajuda a", "aprenda o passo a passo para". Nada de "garantido", "aumente", "dobre".
- Não dê parecer jurídico, tributário, sanitário, de engenharia ou de segurança como certeza: indique buscar profissional habilitado/órgão competente quando o tema pedir (itens críticos).
- Não invente nome de lei, norma, órgão ou artigo. Pode dizer "órgão competente", "município", "corpo de bombeiros", "vigilância sanitária", "contador", "advogado".
- Desconhecido **não é zero**: sempre que fizer sentido, lembre de marcar "não sei" e organizar a coleta.
- Fórmulas devem ser exatamente estas (são as das calculadoras do produto):
  - Ocupação = noites vendidas ÷ noites disponíveis (disponíveis = unidades × dias − bloqueios). Acima de 100% indica dado inconsistente.
  - ADR (diária realizada) = receita de hospedagem ÷ noites vendidas.
  - RevPAR = receita de hospedagem ÷ noites disponíveis (= ADR × ocupação).
  - Contribuição por noite = ADR − custo variável por noite vendida (limpeza, insumos, comissões, taxas e outros custos incrementais, rateados por noite).
  - Ocupação de equilíbrio = custos fixos do período ÷ (contribuição por noite × noites disponíveis). Se a contribuição for zero ou negativa, não existe equilíbrio; se passar de 100%, supera a capacidade.
  - Receita líquida do canal = receita bruta − comissão − custo de aquisição atribuível.
  - Janela de compra = mediana dos dias entre a data da reserva e a da chegada.
  - Necessidade de capital = investimento total (com contingência e capital de giro) − recursos próprios disponíveis.
  - Retorno simples anual = resultado incremental anual ÷ investimento; payback simples = investimento ÷ resultado anual (só se o resultado for positivo).
  - Carga de trabalho = horas necessárias ÷ horas disponíveis. Estoque mínimo = consumo médio diário × prazo de reposição (+ margem de segurança).
- Recomendações educacionais ficam separadas de oferta comercial: **não venda nada** nos guias. Não cite preço, produto nem plano da Zion. Parceria só aparece no módulo 7, como possibilidade opcional sujeita à análise, sem garantia.
- Não escreva ZAIOS, Land Bank, Club, Collection nem nomes internos.

## Formato de saída: um arquivo JSON por módulo
Caminho: `ebook/conteudo/mod<N>.json` (UTF-8, JSON válido, sem comentários).
```
{
 "modulo": N,
 "titulo": "<título do guia, igual ao da aula>",
 "subtitulo": "<uma linha>",
 "abertura": {
   "para_que_serve": "80 a 140 palavras",
   "tenha_em_maos": ["4 a 6 itens curtos"],
   "como_trabalhar": "50 a 90 palavras (período definido, dados verificáveis, desconhecido não é zero, o diagnóstico é orientativo e não é auditoria)"
 },
 "perguntas": [   // exatamente 10, na ordem do formulário, uma por id (m<N>q1 ... m<N>q10)
  {
   "id": "m1q1",
   "por_que_importa": "50 a 90 palavras",
   "como_coletar": ["4 a 5 passos, 12 a 40 palavras cada, específicos desta pergunta (use o campo procedure como ponto de partida e aprofunde)"],
   "exemplo": {"titulo": "frase curta", "texto": "70 a 130 palavras, começa com 'Dados fictícios:' e mostra a conta ou a decisão resolvida, com números simples e coerentes com as fórmulas"},
   "erro_comum": "25 a 60 palavras",
   "como_ler": {"ausente": "15 a 40 palavras (nota 0)", "parcial": "15 a 40 palavras (nota 1)", "comprovado": "15 a 40 palavras (nota 2: o que a evidência precisa mostrar)"},
   "verificacao": "30 a 70 palavras: o indicador, o período de comparação e como confirmar que a ação funcionou sem criar outro problema"
  }
 ],
 "fechamento": {
   "resumo": "60 a 110 palavras",
   "glossario": [{"termo": "...", "definicao": "..."}],   // 4 a 6 termos
   "limites": "40 a 90 palavras (o que este módulo não substitui: parecer profissional, auditoria etc.; sem garantia de resultado)"
 }
}
```
Se a pergunta tem `calc` em `src/meta.json`, o "como_coletar" deve citar, no último passo, a calculadora (ex.: "Registre os números na Calculadora de Ocupação e Canais"). Nomes: C1 Calculadora de Posicionamento; C2 Calculadora de Ocupação e Canais; C3 Calculadora de Diária e RevPAR; C4 Calculadora de Contribuição e Equilíbrio; C5 Calculadora de Capacidade e Estoque; C6 Calculadora de Custo e Retorno da Expansão; C7 Calculadora de Necessidade de Capital.
Depois de escrever, rode `python3 -I ebook/validar_conteudo.py <N>` e corrija até passar. Faça os exemplos de forma que os números **fechem** (confira as contas).
