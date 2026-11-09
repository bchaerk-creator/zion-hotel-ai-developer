# Recomendação · proposta de Comando 05G (não executado)

09/11/2026 · Aguarda revisão e autorização expressa do Bruno.

## 1. Onde estamos

- A composição da ZAIOS calculou certo em **288 de 288 campos** nos 3 cenários e no estresse. Não houve nenhuma divergência matemática.
- As **32 divergências metodológicas** vêm de duas regras do comando que a ZAIOS segue de outro jeito:
  - a base de gestão e royalties;
  - o capital de giro informado.
- Surgiram **7 observações novas** (O8 a O14). As mais relevantes para decisão:
  - **O8:** selo do P6 otimista ao lado de uma viabilidade negativa;
  - **O9:** valor de saída negativo;
  - **O11:** base de gestão e royalties.
- **A integridade continua sem comprovação.** É a principal condição para qualquer homologação definitiva da ZAIOS.

## 2. Riscos para decisões de investimento (se a ferramenta fosse usada hoje)

| Risco | Exemplo nos testes | Impacto possível |
|---|---|---|
| Ler o selo do P6 ou a régua de margem como aprovação (O8) | C3E: "Avançar" e margem "boa", com VPL −R$ 2,79 mi | Investir num projeto que a própria viabilidade manda redesenhar |
| Veredito exibido antes da homologação | Todos os cenários | Decisão apoiada em limites provisórios (H4) |
| VPL com saída distorcido por saída negativa (O9) | C1 | Pouco efeito na decisão (o projeto já é negativo), mas o número fica sem sentido econômico |
| Base de gestão e royalties diferente da contratada (O11) | C3: VPL −R$ 360.737,85 em relação à regra do comando | Sub ou superestimar o retorno, conforme o contrato real de gestão e de marca |
| Capital de giro diferente do planejado (O13) | C1: R$ 45.000 informados contra R$ 109.095,26 necessários | Captar menos que o necessário. A ZAIOS protege, mas o membro não consegue testar o seu próprio valor |
| Colchão de 36 meses (O10) | C1: caixa em queda depois do mês 36 | Falsa sensação de fôlego |
| Parâmetros H4 (taxa, múltiplo, limites, cenários) | Todos | As conclusões mudam com outra taxa ou outro múltiplo |
| Testes sem reserva, quebra e pró-labore | Todos | Geração de caixa maior que na metodologia aprovada (D2-C, D3-A, D4) |

## 3. Proposta de Comando 05G

**Título sugerido:** "Fechamento da cobertura da composição e prova de integridade".

| Bloco | Conteúdo | Tipo | Créditos | Depende de |
|---|---|---|---|---|
| A · Integridade | Obter um hash da origem: conectar a ZAIOS a um repositório GitHub **privado** ou receber uma exportação do Bruno. Comparar com os 9 hashes deste comando | Integridade | Verificar antes no painel (a conexão é configuração do projeto) | Autorização expressa |
| B · Segunda transcrição da composição | Nova leitura independente dos 3 módulos de `src/exercicios` e comparação byte a byte (só leitura) | Integridade | Leitura | Autorização de leitura |
| C · Cobertura restante | 3 execuções integradas com pró-labore > 0, reserva de 4% (D2-C), quebra de 1% (D3-A) e contingência de 20–25%, combinados; taxa de 12% e múltiplo de 5× | Teste de leitura | Não | Autorização de testes |
| D · Testes da própria ZAIOS | Ler os módulos que faltam (dossiê, definições) e rodar os testes vitest sobre a cópia | Teste de leitura | Leitura | idem |
| E · Decisões (Bruno) | Classificar O8 a O14; decidir D8, D10 e D14; definir a base de gestão e royalties (bruta ou hospedagem) e se o membro pode informar o capital de giro | Decisão metodológica | Não | Bruno |
| F · Conferência externa | Contador ou analista revisa os esperados independentes do 05E e do 05F | Validação | Honorários | Bruno (P2) |

**Fora do 05G:**
- corrigir divergências;
- implementar decisões;
- homologar.

Isso continua para depois da integridade comprovada, da conferência externa e da autorização expressa, como já previsto (primeiro passo: ocultar o veredito, D11-A).

## 4. Pedido de decisão ao Bruno

1. Aprovar ou ajustar a proposta de classificação (`RESSALVAS_E_CLASSIFICACAO_05F.md`, seção 4).
2. Escolher o caminho da integridade: GitHub privado, exportação manual ou adiar.
3. Autorizar ou não os blocos B, C e D (só leitura).
4. Decidir as questões do bloco E, começando por O8 e O11, as de maior impacto na decisão de investimento.
