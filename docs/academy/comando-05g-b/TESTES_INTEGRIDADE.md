# Testes de integridade (Teste A)

Comando 05G-B · 09/11/2026 · **A integridade continua sem comprovação.** Este teste aumenta a evidência, mas não substitui um hash calculado na origem.

## 1. Procedimento

1. Um agente separado leu de novo, pelo conector do Lovable (`read_file` no commit `ec21ad5`), os 6 arquivos da camada de composição e de G2/G3. A regra foi expressa: não abrir, listar nem comparar com as cópias já existentes.
2. Os arquivos foram salvos numa pasta separada, fora do repositório.
3. Foi calculado o SHA-256 das duas cópias e comparado.

## 2. Resultado

| Arquivo | Cópia do 05E | Segunda transcrição (05G-B) | Resultado |
|---|---|---|---|
| `src/exercicios/capex-calculo.ts` | `b728645b2a0ae834` | `b728645b2a0ae834` | Idênticos |
| `src/exercicios/receitas-calculo.ts` | `c36e73513e0a0402` | `c36e73513e0a0402` | Idênticos |
| `src/exercicios/viabilidade-calculo.ts` | `2bcba2abb27a1e31` | `2bcba2abb27a1e31` | Idênticos |
| `src/exercicios/mercado-calculo.ts` | `595b6b20b4c948df` | `595b6b20b4c948df` | Idênticos |
| `src/exercicios/financas-calculo.ts` | `420f36cad2929d47` | `420f36cad2929d47` | Idênticos |
| `src/calc/operacao.ts` | `016810f560aed332` | `016810f560aed332` | Idênticos |

Somado ao 05E (três transcrições idênticas dos 4 arquivos do motor), **todos os arquivos de cálculo e de composição testados agora têm pelo menos duas leituras independentes e idênticas.**

## 3. Limitação importante, achada neste comando

As leituras vêm **da mesma fonte**: o conector do Lovable devolve o texto, não o arquivo bruto. **Caracteres invisíveis podem ser normalizados da mesma forma em todas as leituras**, e então as cópias ficariam idênticas entre si e diferentes do original.

O Teste C deu um indício concreto disso:
- a função de moeda da ZAIOS gera o espaço não separável (U+00A0) em "R$ 1.300,00";
- a cópia do teste `financas-indicadores.test.ts` espera um espaço comum e falha;
- o mais provável é que o arquivo original tenha o espaço não separável e que a leitura por texto o tenha trocado por espaço comum.

**Consequência:**
- **Para o cálculo:** a normalização não afeta números, porque não há espaço não separável nas fórmulas, e todos os resultados conferiram com o cálculo independente.
- **Para a integridade:** **transcrições idênticas não provam fidelidade byte a byte.** A ressalva só fecha com hash calculado sobre o arquivo original (`PLANO_GITHUB_PRIVADO.md`).

## 4. Situação

| Item | Situação |
|---|---|
| Segunda transcrição da composição | **Feita.** 6 de 6 idênticos |
| Commit do projeto | Continua `ec21ad5`, sem edição desde 07/11 (verificado no 05F; nenhuma edição foi feita desde então) |
| Hash na origem | **Indisponível** (GitHub não conectado, por instrução) |
| Integridade comprovada | **Não** |
