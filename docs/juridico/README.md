# Documentos jurídicos — Contratos operacionais

## Contrato de Zeladoria — Mediterrâneo × 19.525.600 Camila Rabelo Glicerio Gois

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `contrato-zeladoria-mediterraneo.*` | Contrato principal, 18 cláusulas | Assinatura (2 vias + 2 testemunhas) |
| `anexos-contrato-zeladoria.*` | Anexos I a V (escopo, recibos, comodato, checklist, preposto) | Assinatura junto ao contrato + rotina mensal |
| `nota-estrategica-zeladoria.*` | Racional das decisões, riscos e regras de operação | **Uso interno** — não entregar à Contratada |

Cada documento existe em três formatos: `.md` (fonte editável e versionada), `.docx` (edição em Word) e `.pdf` (leitura e assinatura).

### Regenerar os arquivos após editar o Markdown

```bash
python3 scripts/md2docx.py docs/juridico/<nome>.md docs/juridico/<nome>.docx
python3 scripts/md2pdf.py  docs/juridico/<nome>.md docs/juridico/<nome>.pdf "<texto do rodapé>"
```

### Antes de assinar

1. Revisão por advogado trabalhista de SC (cláusulas 2, 7, 8 e 9)
2. Camila altera o endereço da sede no CNPJ (hoje coincide com o do empreendimento)
3. Camila altera o CNAE principal de 97.00-5-00 para 81.21-4-00 ou 81.29-0-00
4. Preencher Anexo I (perímetro, frequências, janelas, SLA) com a operação real
5. Definir preço, datas de faturamento e pagamento, e os valores das multas
6. Vistoria da Casa de Operações com fotos datadas (Anexo III-B)

Detalhamento completo em `nota-estrategica-zeladoria.md`.

### Rotina mensal (pasta por competência)

`NFS-e` + `Anexo II-A` (relatório) + `Anexo II-B` (recibo com quitação) + certidões do `Anexo IV` — conferidos **antes** do pagamento.
