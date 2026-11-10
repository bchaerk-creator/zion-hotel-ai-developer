# Jornada 2 · Gestão · Módulo 7 · Qualidade, reputação e plano de crescimento · Plano da lição (G07)

Último módulo da Jornada 2. Produzido em 10/11/2026 com o molde do Módulo 2 e as correções dos Módulos 1, 3 e 5. Nada publicado no ClickMax, nada ativado.

## 1. A lição em uma frase
Aprenda o passo a passo para juntar o que você construiu na jornada num único **Plano de Gestão Profissional**: as oito páginas, a página de qualidade e reputação (nota, resposta às avaliações, padrão mínimo e plano de crescimento), a rotina semanal e o teste de prontidão, em um PDF.

## 2. Públicos e jornadas
- **A · Vai abrir:** a nota e o volume ficam em branco; a meta, o protocolo e o padrão mínimo valem para as primeiras avaliações («As primeiras avaliações são permanentes», Panorama · Pilar 07). O plano de saída começa com a abertura.
- **B · Dono que opera (público central):** junta as páginas, mede a nota, escreve o protocolo e marca a saída da operação com data.
- **C · Operador:** o Plano vira a prestação de contas ao dono; o teste das duas semanas é combinado com ele.
A ficha pergunta a situação na abertura (e a lê das fichas anteriores) e adapta as validações e leituras.

## 3. Fontes Zion (mapa completo fora do repositório) e convenções
- **Panorama do Desenvolvimento Hoteleiro:** Trilha B · G7 Governança e Indicadores («Estar presente não é gerir.»; cinco indicadores; reunião semanal de 30 minutos; «A operação continua funcionando sem você por um mês»); síntese da Trilha B (os sete entregáveis, espinha das páginas 1 a 6); Trilha A · Pilar 07 Lançamento («As dez primeiras avaliações valem mais que o primeiro ano de anúncio.»; «Reputação ruim no começo é a coisa mais cara e mais lenta de consertar neste setor.»; plano das vinte primeiras avaliações). O pilar «Reputação e Avaliações» da Trilha C só aparece no mapa dos 21 pilares, sem conteúdo (lacuna).
- **Método Zion 360° · Volume 07 Lançamento, capítulo 18:** Protocolo da Primeira Avaliação™ (média pequena, pedir na saída, resolver antes de pedir, responder todas, positiva específica, negativa «reconheça, não discuta, diga o que mudou», regra das 24 horas).
- **Jornada do COMO · Etapa 07, Passos 05 e 06:** «Responder em menos de uma hora, sempre»; Sistema de Avaliações™ («Três menções ao mesmo item em um trimestre é um problema de produto, não de hóspede.»; taxa abaixo de 40%; dimensão mais baixa; comparar com os concorrentes diretos).
- **Etapa 09 · Passo 13 Rotina Financeira:** 5 minutos por semana, 10 por mês, 2 horas por trimestre, meio dia por ano; sete datas no calendário.
- **Etapa 10 · Passos 10, 12 e 13:** painel por exceção (retomado do Módulo 5), Teste de Prontidão (catorze dias, ocupação média, o que medir, como ler) e Plano de Saída da Operação™ (quatro fases, seis a oito meses, o tempo que sobra, as quatro condições da segunda unidade). É a "saída completa da operação" que o Módulo 5 deixou para cá.
- **Convenções:** linguagem simples, sem siglas na tela; "nota" sempre na escala do canal (5 ou 10); "página pronta" é a que chegou ao PDF na ficha do módulo. Os ™ aparecem só no resumo, com o nome da fonte. Exemplos numéricos das fontes (R$ 199.700, 64%, 4,82, R$ 9.800) não foram usados.

## 4. Objetivos (verbos observáveis)
1. **Reunir** as páginas 0 a 6 do Plano e **identificar** as que faltam (lembrar, aplicar).
2. **Calcular** a taxa de avaliação e **explicar** por que uma avaliação ruim pesa mais com pouco volume (aplicar, compreender).
3. **Escrever** o protocolo de avaliação: o pedido, quando não pedir, as respostas positiva e negativa e a regra das 24 horas (criar).
4. **Definir** o padrão mínimo de reputação e **transformar** uma crítica repetida em ajuste de produto com prazo (avaliar, criar).
5. **Marcar** a rotina semanal, mensal, trimestral e anual no calendário (aplicar).
6. **Agendar** o teste das duas semanas e **ler** o resultado pela régua da fonte (aplicar, avaliar).
7. **Datar** as quatro fases do plano de saída e **decidir** o que fazer com o tempo que sobra e com a segunda unidade (criar, avaliar).

## 5. As seis etapas
1. As páginas que você já fez (leitura das chaves `zion-t2-*` do aparelho).
2. A nota e as avaliações (nota, meta, volume, taxa, dimensão mais baixa, concorrentes, crítica repetida, tempo de resposta).
3. O protocolo de resposta e o padrão mínimo.
4. A rotina semanal (e as datas do mês, do trimestre e do ano).
5. O teste de prontidão e o plano de crescimento (plano de saída, tempo que sobra, segunda unidade).
6. O Plano em PDF: páginas 0 a 7, rotina, teste, plano de saída, atenção, como verificar e a próxima etapa.

## 6. Regras da ferramenta (testáveis; `src/logic.js`)
### 6.1 Entradas
Situação; escala (5 ou 10); nota atual, meta e prazo; avaliações acumuladas; estadias e avaliações dos últimos 3 meses; dimensão mais baixa e a nota dela; nota dos concorrentes; críticas do trimestre; a crítica que mais se repetiu e quantas vezes; tempo médio de resposta. Protocolo (pedido, regra de não pedir, respostas, regra das 24 horas, quem responde); padrão mínimo (nota mínima, resposta máxima em minutos, taxa mínima, auditoria por amostragem, ajuste de produto e prazo quando a crítica se repetiu 3 vezes). Rotina (dia e hora da reunião, dia do painel, dia do mês da Folha, primeira trimestral, anual). Plano (início da Fase 1, semanas das Fases 1 e 2, início do teste, responsável, ocupação projetada, nota média de 3 meses, período de ocupação média, tempo que sobra, quatro condições; resultados do teste quando feito).
Pré-preenchimento a partir das fichas do mesmo aparelho: nome, e-mail, hospedagem e situação (qualquer ficha); escala, nota, meta e reunião (Módulo 1); nota mínima, dia do painel e início (Módulo 5); meta de venda direta (Módulo 3, só para o plano de crescimento). A função `num` lê "13.000" como treze mil (correção do Módulo 1).

### 6.2 Cálculo
- Página pronta: a chave existe e tem o campo `pdf`; em andamento: a chave existe sem `pdf`; ainda não feita: sem chave.
- Taxa de avaliação = avaliações dos 3 meses ÷ estadias dos 3 meses.
- Média depois de uma avaliação ruim = (nota × avaliações + 3) ÷ (avaliações + 1), com 6 na escala de 10 (generalização declarada da tabela do Volume 07).
- Fases: Fase 1 = início + semanas × 7 − 1; Fase 2 começa no dia seguinte; Fase 3 vai do fim da Fase 2 até a véspera do teste (semanas inteiras); Fase 4 = 14 dias corridos. Meses = dias do início ao fim do teste ÷ 30,4375, com uma casa.
- Trimestrais: a primeira e mais três, de três em três meses (dia ajustado ao fim do mês quando preciso).
- Segunda unidade: quatro sim = "pode estudar"; qualquer não = "agora não".
- Leitura do teste (Etapa 10, Passo 12), nesta ordem: nota abaixo da média de 3 meses menos a tolerância (0,1 em 5; 0,2 em 10) = falta padrão ou treino; ocupação abaixo da projetada sem causa externa = falta quem trabalhe a demanda; com causa externa = repetir o teste; mais de dois contatos = falta critério; senão, passou.

### 6.3 Leituras e atenção (só a fonte)
Atenção em ordem: páginas que faltam; nota abaixo da mínima; crítica repetida 3 vezes (problema de produto); taxa abaixo do mínimo; resposta acima do máximo; Fase 3 com menos de 8 semanas; período que não é de ocupação média; segunda unidade sem as quatro condições; dimensão mais baixa. Sem alerta: "mantenha a rotina".

### 6.4 Critério de conclusão (selo)
Sete itens + PDF: (1) páginas 0 a 6 prontas; (2) nota, volume e meta; (3) protocolo escrito com as duas regras adotadas; (4) padrão mínimo definido; (5) rotina marcada; (6) teste de prontidão agendado (data, responsável, ocupação projetada, nota de referência, período de ocupação média); (7) quatro fases datadas e o tempo que sobra decidido. Com o PDF baixado: selo "Plano completo · pronto para a Jornada 3". Faltando páginas, o PDF sai mesmo assim, com "página ainda não feita" e o endereço da ficha.

## 7. Telas da ficha "O Montador do Plano de Gestão"
Abertura (nome, e-mail, hospedagem, situação, botão do exemplo) → 1 As páginas (estado de cada uma, link para a ficha) → 2 A nota → 3 Protocolo e padrão mínimo → 4 Rotina → 5 Teste e plano de crescimento → Resultado em cinco partes, critério, PDF, próxima etapa. A ficha carrega a lógica dos sete módulos anteriores uma a uma (três usam o mesmo nome global `ZP`) para resumir cada página; se alguma lógica mudar ou faltar, a página entra com um resumo mínimo, sem erro.

## 8. Planilha "Qualidade e Reputação" (openpyxl, em branco e exemplo)
Abas: Comece aqui · Avaliações por canal (nota ponderada, taxa, média depois de uma avaliação ruim, leitura contra a meta, a mínima e os concorrentes) · Críticas (menções por item no trimestre, três ou mais pedem ajuste e prazo) · Painel semanal (exceção, atenção ou relatório) · Teste de prontidão (agendamento e leitura do resultado) · Plano de saída (quatro fases, meses, segunda unidade, rotina do ano).

## 9. Exemplo didático (dados fictícios, conferidos duas vezes)
Cabanas do Vale, 4 unidades, a mesma dos módulos 0 a 6. **Nota 4,7 de 5 com 38 avaliações; meta 4,8 até 31/10/2027** (Módulo 1); nota mínima 4,7 (Módulo 5). Canais: Plataforma A 24 avaliações, 4,7; Plataforma B 9, 4,6; perfil no mapa 5, 4,9 → nota ponderada 178,7 ÷ 38 = 4,70. Últimos 3 meses: 72 estadias, 25 avaliações → **taxa 34,7%** (abaixo de 40%). Uma avaliação de 3 leva a média a **4,66** ((4,7 × 38 + 3) ÷ 39). Concorrentes 4,6 (+0,1). Dimensão mais baixa: limpeza, 4,6. Sete críticas no trimestre (01/08 a 31/10/2026); "ralo do chuveiro com cheiro na cabana 3" **3 vezes** → ajuste: trocar o sifão e incluir o ralo no checklist de limpeza, até **30/11/2026**. Tempo médio de resposta 40 min (máximo 60). Painel de quatro semanas (12/10 a 02/11/2026): 2 exceções (nota 4,5; gasto 15% acima), 1 avaliação sem resposta.
Protocolo: "Avaliações são o que faz uma casa pequena ser encontrada. Se a estadia foi boa, a sua ajudaria muito."; não pede com problema não resolvido; regra das 24 horas; quem responde: Ana (dona).
Rotina: reunião segunda-feira 08:00 (Módulo 1), painel na segunda (Módulo 5), Folha no dia 5, trimestrais 11/01, 11/04, 11/07 e 11/10/2027, anual 08/11/2027.
Plano de saída: Fase 1 de 16/11/2026 a 10/01/2027 (8 semanas); Fase 2 de 11/01 a 07/03/2027 (8); Fase 3 de 08/03 a 13/06/2027 (14); **teste de 14/06 a 27/06/2027**; **7,4 meses** (224 dias). Responsável: a diarista, com o auxiliar de manutenção; ocupação projetada 50% (meta do Módulo 1); nota de referência 4,7. Tempo que sobra: trabalhar sobre o negócio (duas horas por semana para preço e venda direta, como no Módulo 5). Segunda unidade: só a retirada está paga (Folha do Módulo 2 com resultado positivo depois da retirada) → **agora não, faltam 3 de 4**.
Plano de crescimento: nota 4,7 → 4,8 até 31/10/2027; **venda direta 30% → 40% até 30/06/2027** (Módulo 3).
Nas páginas do Plano: nota de gestão 50 (Marco Zero); resultado R$ 4.269,20 e equilíbrio 28,5% (Módulo 2); piso R$ 225 (Módulo 3); 20 horas e alçada R$ 100 → 300 (Módulo 5); os números dos Módulos 4 e 6 vêm das fichas deles.

## 10. Versão autônoma e acompanhada
Autônoma: a ficha, a planilha, o resumo e o prompt de IA bastam. Acompanhamento Zion 360°: o PDF do Plano é o material da revisão de marco final; a equipe Zion comenta a página 7 e a data do teste. Nenhum envio automático de dados (ver `LIMITACOES.md`).

## 11. Lacunas das fontes e decisões
1. **"Pilar 07 (reputação) da Trilha 1"**: no Panorama, o Pilar 07 da Trilha A é Lançamento, com o plano das primeiras avaliações, e o pilar "Reputação e Avaliações" da Trilha C não tem conteúdo. Usamos o Volume 07 (capítulo 18) e a Etapa 07 como fonte de reputação.
2. **Padrão mínimo**: o nome é do comando; o conteúdo é a soma de regras das fontes (nota mínima, resposta em menos de uma hora, taxa de 40%, 24 horas, auditoria por amostragem, três menções). Elaboração declarada.
3. **Tolerância da nota no teste** (0,1 em 5; 0,2 em 10): a fonte diz "dentro da variação normal" sem número. Convenção declarada na ficha, na planilha e no resumo.
4. **Ocupação mantida** = ocupação do período maior ou igual à projetada (a fonte diz «mantida ou melhor»).
5. **Página pronta** = PDF gerado na ficha do módulo. Não é nota de qualidade da página.
6. **Rotina semanal consolidada**: junta G7, Etapa 10, Etapa 09 e Etapa 07. Os 15 minutos das avaliações e da auditoria são estimativa da lição, não da fonte.
7. As fases 1 e 2 do plano de saída correm em paralelo ao treino de quatro semanas do Módulo 5 (que começa em 16/11/2026 no exemplo): a Fase 2 da fonte inclui contratar e treinar todas as funções, não só a primeira atividade.
8. O resumo de cada página depende da lógica de cada módulo; se um módulo mudar o formato da chave, a página entra com resumo mínimo e o pedido de anexar o PDF da ficha.
