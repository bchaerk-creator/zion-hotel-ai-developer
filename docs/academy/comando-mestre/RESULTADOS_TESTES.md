# Resultados dos testes · Comando Mestre

10/11/2026 · Versão de desenvolvimento (cópia local privada). Saídas completas em `testes/financeiro/resultados/2026-11-10-mestre/`.

## Resumo

| Bateria | O que confere | Resultado |
|---|---|---|
| **Esperados independentes das regras aprovadas** (`mestre/referencia_mestre.py` + `run_mestre.js`) | 13 casos: C1, C2, C3, C3E e variações de bases das taxas, valor fixo, categorias A/B/C, sazonalidade e alíquota de C, giro disponível, reserva de 6 meses, aluguel no fixo. Receita por categoria, deduções, taxas, EBITDA, margens, indicação, equilíbrio, giro (técnica, base, reserva), captação, saída, VPL, TIR, payback, cenários conservador e otimista, curva de 120 meses, saldos anuais, primeiro mês negativo, capital adicional, atraso, colchão, passos e decisão | **673 de 673 OK** (na versão `ec21ad5`: 203 OK) |
| **Aceite O8 a O14 por valor** (`mestre/aceite_mestre.js`) | 22 verificações, com os esperados do 05G-A onde a regra é isolada | **22 de 22** (na versão `ec21ad5`: 3) |
| **Compatibilidade** (`mestre/compat_mestre.js`) | Respostas antigas, 8 cenários, base x desenvolvimento | **256 de 256** campos de regras não alteradas idênticos; 52 mudam por decisão; leitores abrem resultados antigos |
| **Vitest** (testes da ZAIOS na cópia + 41 novos) | 176 testes em 16 arquivos | **175 passam, 1 falha** (a antiga do espaço não separável, diagnosticada) |
| **Suíte financeira** (237 casos, ZAIOS de desenvolvimento, Arsenal da main) | Regressão contra o comportamento do `ec21ad5` | 185 OK, 27 divergências e 5 limitações já conhecidas; **4 falhas e 1 limitação não reproduzida, todas previstas**: os 4 casos C-ZAIOS-C conferem o giro pela regra antiga (O12) e o C-G2-impostos confere a limitação O7, agora resolvida |
| **Suíte financeira com o Arsenal de desenvolvimento** (238 casos) | Idem, com B08 e A09 novos | 188 OK, 26 divergências, 4 limitações; as mesmas 4 falhas e 1 limitação previstas; B08 e A09 sem falha |
| **Composição 05F e 05G** (referências anteriores às decisões) | 476 campos | 74 diferenças, todas em campos que as decisões mudam: selo do P6 (O8), saída e VPL com saída (O9), giro e captação (O12), curva, atraso, colchão e passos (O10 com O12) |
| **Linha de base 05G-A** (verificações por nome de campo, escritas antes da implementação) | 11 | 7 passam; as 4 restantes (O11-1, O12-1, O13-1, O14-1) procuram nomes de campo ou a regra antiga de 6 meses. Substituídas pelo aceite por valor acima, que passa |

## Cobertura pedida no comando

| Pedido | Onde |
|---|---|
| Testes financeiros independentes | `referencia_mestre.py` (Python, sem código da ZAIOS) |
| Composição | `run_mestre.js`, `run_05f.js`, `run_05g.js` |
| Vitest | 176 testes |
| Regressão | suíte de 237/238 casos, 05F, 05G, compatibilidade |
| Cenários conservador, base e otimista | `run_mestre.js` (VPL de cada cenário, 13 casos; categoria C no conservador) |
| Atrasos de inauguração | `run_mestre.js` (custos mantidos, receita não realizada, perda de saldo e de VPL), aceite O10-2, `o10-horizonte.test.ts` |
| EBITDA negativo | C1 (saída zero, VPL com = sem), `o9-saida.test.ts` |
| Receitas complementares | 3 casos A/B/C, `o14-complementares.test.ts` |
| Impostos | deduções por categoria e alíquota própria (O14), `o7-impostos.test.ts` (G2) |
| Capital de giro | `o12-giro.test.ts`, `o13-giro-disponivel.test.ts`, 13 casos |
| Ponto de equilíbrio | equilíbrio em noites nos 13 casos (com taxas fixas e categoria C); B08 nos dois indicadores |
| Compatibilidade com projetos existentes | `compat_mestre.js`, `compat-dossie.test.ts` |
| Falha de formatação monetária | `DIAGNOSTICO_FORMATACAO_MONETARIA.md` |

## Limitações dos testes

- **Integridade:** todos os testes rodam sobre a cópia transcrita. Sem o GitHub privado, não há prova de que ela é idêntica ao original.
- **Independência parcial:** a referência das regras novas e a implementação foram escritas pela mesma sessão, a partir do texto das decisões. Onde existiam, os valores conferem com os esperados do 05G-A (O8-3, O9, O11-1, O12-1, O12-2, O14-1, O14-2). Recomenda-se conferência externa.
- **Serviços externos:** testes de integração (Supabase, autenticação, gravação) e de tela no navegador não rodam no ambiente isolado; 14 arquivos de teste da ZAIOS ainda não foram lidos (leitura autorizada só depois do GitHub).
- **Tipos:** a cópia parcial não tem os tipos do React; os 2 avisos de `key` em componentes já existiam na base.
