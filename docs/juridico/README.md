# Documentos jurídicos — Contratos operacionais

## Contrato de Zeladoria — Mediterrâneo × 19.525.600 Camila Rabelo Glicerio Gois

| Arquivo | Conteúdo | Uso |
|---|---|---|
| `contrato-zeladoria-mediterraneo.*` | Contrato principal, 18 cláusulas, objeto modular (Módulos A a G) | Assinatura (2 vias + 2 testemunhas) |
| `anexos-contrato-zeladoria.*` | Anexos I a V (escopo, recibos, comodato, checklist, preposto) | Assinatura junto ao contrato + rotina mensal |
| `regimento-operacional-mediterraneo.*` | Anexo VI — regras da operação, uso da Casa de Operações, protocolos de emergência e Termo de Adesão | Assinatura junto ao contrato + adesão individual da equipe |
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
4. Assinalar no Anexo I os módulos contratados (A conservação · B paisagismo · C hospitalidade · D manutenção · E zeladoria e ronda · F recebimento de valores · G alimentos e bebidas) e preencher perímetro, frequências, janelas e SLA
5. Definir onde o A&B é produzido e conferir o alvará sanitário do local (Cláusula 3.11 c)
5. Definir preço, datas de faturamento e pagamento, e os valores das multas
6. Vistoria da Casa de Operações com fotos datadas (Anexo III-B)

Detalhamento completo em `nota-estrategica-zeladoria.md`.

### Rotina mensal (pasta por competência)

`NFS-e` + `Anexo II-A` (relatório) + `Anexo II-B` (recibo com quitação) + certidões do `Anexo IV` — conferidos **antes** do pagamento.
