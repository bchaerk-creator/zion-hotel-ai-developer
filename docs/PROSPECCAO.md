# Prospecção — de onde vem cada contato

Este documento define quais fontes a Zion usa para montar a carteira, e quais
não usa. A distinção não é técnica — tudo é tecnicamente possível. É de risco.

## A régua

Uma fonte é utilizável quando as três respostas são sim:

1. O dado é de **pessoa jurídica** e foi publicado pela própria empresa como
   canal comercial?
2. Os **termos de uso** do site permitem acesso automatizado, e o `robots.txt`
   não proíbe?
3. Existe **base legal** (LGPD Art. 7º) — para prospecção B2B, legítimo
   interesse — e conseguimos demonstrar a origem do dado?

## Fontes utilizáveis

| Fonte | O que traz | Por que serve |
|---|---|---|
| Site próprio de pousada/hotel | e-mail e telefone comercial, endereço, nº de UHs | A empresa publicou como canal de contato. É PJ. |
| Associações setoriais (ABIH, sindicatos de hotéis) | lista de associados | Diretório público de empresas do setor |
| Convention & Visitors Bureaux | associados e operadores locais | Idem |
| Secretarias e portais municipais de turismo | cadastro de meios de hospedagem | Dado público municipal |
| CADASTUR (MTur) | prestadores de serviço turístico registrados | Cadastro público federal, por definição consultável |
| Imobiliárias com CRECI | corretoras de imóveis rurais e turísticos | PJ registrada em conselho |
| Portais de imóvel rural | anúncios com corretor responsável | Contato do corretor é comercial, não do proprietário |
| Feiras e eventos (ABAV, Equipotel, Festuris) | expositores | Empresa se expôs publicamente como fornecedora |
| Juntas comerciais e CNPJ | razão social, CNAE, endereço | Registro público |

## Fontes que não usamos

| Fonte | Por quê |
|---|---|
| **Airbnb** | Termos proíbem extração de dados de anúncio e anfitrião. A empresa litiga contra scrapers. O anfitrião típico é pessoa física — sem base legal para abordagem fria. |
| **Booking, Expedia, Hotéis.com, Despegar** | Mesma proibição contratual. E o dado de contato do hotel geralmente nem está lá — a OTA intermedeia justamente para retê-lo. |
| **TripAdvisor** | Termos proíbem coleta automatizada. |
| **Instagram, Facebook, LinkedIn, TikTok** | Termos proíbem. Perfil pessoal é dado de PF. |
| **Cartório de registro de imóveis** | Matrícula identifica proprietário pessoa física. Consulta é legítima caso a caso, com propósito; varredura em massa não é. |
| **CAR / SIGEF / SNCI** | O georreferenciamento é público, mas o vínculo com o CPF do proprietário é dado pessoal. Serve para mapear a **terra**, nunca para montar mailing. |
| Listas compradas de terceiros | Sem origem rastreável não há como demonstrar base legal. É o caminho mais rápido para uma notificação da ANPD. |

Essas restrições estão no código, não só aqui: `DOMINIOS_BLOQUEADOS` em
`src/prospects/coletor.py` recusa esses domínios, e há teste cobrindo.

## Como chegar no dono do terreno sem raspar registro

O proprietário rural é o alvo mais difícil e o mais valioso. O caminho legítimo
não é a matrícula — é o intermediário:

1. **Corretor de imóveis rurais** — tem a carteira, tem o relacionamento e é PJ.
   Uma parceria com dez corretores em Urubici vale mais que mil matrículas.
2. **Sindicatos rurais e cooperativas** — chegam a quem tem terra sem
   intermediar dado pessoal.
3. **Escritórios de agronomia e topografia** — atendem quem está pensando em
   dar destino à área.
4. **Inbound** — o diagnóstico territorial como isca. Quem preenche o
   formulário dá consentimento explícito, que é a base legal mais forte que
   existe. É mais lento e converte muito melhor.

## O mapa de destinos

`data/destinos/destinos_sul.csv` traz 20 destinos por estado do Sul, com a
região turística, vocação, bioma, sazonalidade e uma leitura de relevância para
o modelo Zion.

```bash
zion-ai destinos resumo
zion-ai destinos listar --uf SC --relevancia alta
zion-ai destinos prospectar Urubici --uf SC
```

**Relevância não é tamanho de fluxo.** Balneário Camboriú tem fluxo enorme e
relevância baixa: o produto local é torre à beira-mar, e o modelo Zion não
dialoga com isso. Guaraqueçaba tem fluxo pequeno e relevância alta: é o maior
remanescente contínuo de Mata Atlântica do país, com oferta qualificada quase
inexistente.

### Procedência deste mapa — leia antes de usar como meta

O arquivo foi montado a partir de conhecimento da geografia turística
brasileira, **não de uma extração da base oficial**. O ranking por UF é
julgamento editorial sobre demanda conhecida, não número medido.

Antes de virar meta comercial, valide contra:

- **Mapa do Turismo Brasileiro** (MTur) — categoriza municípios de A a E por
  número de estabelecimentos, empregos formais em hospedagem e estimativa de
  fluxo doméstico e internacional. É o instrumento oficial de demanda.
- **CADASTUR** — quantos meios de hospedagem cada município tem registrado.
- **IBGE / SIDRA** — PIB de serviços e emprego no setor.

Nenhuma dessas fontes era alcançável do ambiente onde o arquivo foi gerado, por
restrição de rede. A validação precisa rodar numa máquina com acesso aberto.

## Ordem de trabalho sugerida

1. Validar o mapa de destinos contra o MTur.
2. Escolher **três** destinos de relevância alta para começar — não trinta.
3. Levantar as fontes institucionais desses três (ABIH, secretaria, bureau).
4. Importar via `zion-ai prospects importar`.
5. Rodar `zion-ai prospects listar --score-minimo 7` e abordar por ordem.
6. Só depois automatizar coleta, e sempre com `--simular` antes.

Começar por três destinos e fechar o ciclo até a primeira reunião ensina mais
sobre o funil do que uma base de dez mil contatos que ninguém liga.
