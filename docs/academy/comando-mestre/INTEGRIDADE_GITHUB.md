# Integridade e testes no repositório original · 10/11/2026

O Bruno ligou a ZAIOS ao GitHub em 10/11/2026 (repositório privado criado pelo Lovable; o commit `ec21ad5` está no histórico, seguido só de um commit que reescreve o README).

## Integridade da cópia auditada

| Resultado | Arquivos |
|---|---|
| Idênticos byte a byte ao `ec21ad5` | 57 de 59 |
| Diferentes só por caracteres alterados na transcrição, sem mudança de regra | 2 |

- `src/test/financas-indicadores.test.ts`: o original tem o espaço não separável (U+00A0) entre "R$" e o número; a transcrição trocou por espaço comum. **Confirma a hipótese 1 do diagnóstico da formatação monetária: a falha era da transcrição. No original o teste passa.**
- `src/lib/dossie-pdf.ts`: o original escreve a faixa de acentos como escape (`̀-ͯ`); a transcrição gravou os próprios caracteres. A expressão é a mesma.

Conclusão: **a integridade da cópia usada do 05E ao Comando Mestre está comprovada**, e os resultados dos testes daquelas etapas valem para o código original.

## Testes completos da plataforma

| Versão | Passam | Falham | Pulados (integração com o banco real) | Total |
|---|---|---|---|---|
| Original (`main`) | 370 | 0 | 26 | 396 |
| Desenvolvimento (branch `dev/comando-mestre`, decisões O7 a O14) | 411 | 0 | 26 | 437 |

- Checagem de tipos do projeto inteiro na branch: 0 erros. Compilação do site (`vite build`): concluída sem erro. Testes novos sem erro de lint.
- Os 26 testes de integração precisam do banco do Lovable Cloud e ficam pulados fora dele (também no original).

## Onde está a branch

A branch `dev/comando-mestre` (16 commits sobre a `main`) está pronta na cópia de trabalho desta sessão e no pacote enviado ao Bruno. **Ainda não foi enviada ao GitHub:** o envio pede uma permissão de escrita no repositório que precisa da confirmação do Bruno nesta sessão. A `main`, que o Lovable sincroniza e publica, não foi tocada.
