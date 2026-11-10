# Diagnóstico · falha de formatação monetária

10/11/2026 · Teste afetado: `financas-indicadores.test.ts:98` ("Dossiê de Operação G2 e G3 monta seções 8, 9 e 10"), que falha na cópia desde o 05G-B.

## O que foi verificado

| Verificação | Resultado |
|---|---|
| Caractere entre "R$" e o número na saída do formatador (`toLocaleString("pt-BR", { style: "currency" })`) | U+00A0 (espaço não separável), código `a0` |
| Caractere no texto esperado do teste, na cópia transcrita | U+0020 (espaço comum) |
| Mesmo teste, trocando só U+00A0 por espaço comum na saída (cópia descartável, sem alterar o teste) | Os 50 testes do arquivo passam |
| Teste de diagnóstico novo (`diagnostico-nbsp.test.ts`) | Passa: confirma U+00A0 e que só ele difere |
| Outros testes que comparam texto monetário | Nenhum na cópia |

## Conclusão

A diferença é **um caractere invisível**, não um erro de cálculo nem de formatação de valor. Duas hipóteses:

1. **Mais provável:** o arquivo original tem U+00A0 no texto esperado e a transcrição (leitura pelo conector) trocou por espaço comum.
2. O teste também falha no repositório original.

A confirmação depende do arquivo original, pelo GitHub privado. O teste **não foi alterado**. Se a hipótese 2 se confirmar, a correção recomendada é o teste comparar com o próprio formatador (ou normalizar U+00A0), sem mudar o formatador, que segue o padrão do idioma.

## Atualização · 10/11/2026 (GitHub ligado)

Confirmado no repositório original: o texto esperado do teste tem U+00A0. **A falha era da transcrição; no original o teste passa** (370 de 370 testes executáveis passam na main). Ver .
