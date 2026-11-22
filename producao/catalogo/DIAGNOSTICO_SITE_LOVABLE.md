# Diagnóstico do site Zion Hotel Group (Lovable) · 22/11/2026

Somente leitura. Nada foi alterado no site. Projeto "Zion Hospitality Platform" (`dd227afd…`), domínio zionhotelgroup.com.
Fonte: leitura do código publicado (main) por busca de termos, preços e links. Não é uma varredura visual de cada tela.

## 1. Resumo em cinco linhas
1. O site inteiro foi montado em volta do **diagnóstico grátis**: ele é a porta de entrada da home, do Land Bank, da Academy, do Inscreva e do HeroVenda.
2. Depois do grátis vem uma escada de preços que **já existe e vende por outro sistema (Asaas)**: Diagnóstico de Viabilidade R$ 47 → Zion Land Members + Radar / Jornada R$ 270 → Consultoria prévia R$ 490 → Mentoria.
3. A nova **Sessão Zion 360° (R$ 270, ClickMax)** entra no meio dessa escada e **concorre com três ofertas**: o R$ 47 (também entrega dossiê e plano de 30/60/90), o R$ 270 da Jornada (mesmo preço, outro conteúdo, outro checkout) e o R$ 490 (também é "consultoria com o Bruno").
4. As páginas de reunião (`/reuniao`, `/sessao`, `/diagnostico/agendar`, `/diagnostico-previo`) e as páginas estáticas do `docs/` ainda dizem **"sem custo para agendar" / "reunião sem custo"**.
5. Não está em harmonia hoje. Para ficar, é preciso **decidir qual escada fica** antes de trocar textos.

## 2. Mapa das páginas (rotas públicas)
| Grupo | Rotas |
|---|---|
| Institucional | `/`, `/sobre`, `/fundador`, `/manifesto`, `/cases`, `/contato`, `/projects`, `/oportunidades`, `/management`, `/advisor`, `/hub`, `/app` |
| Método e Academy | `/metodo`, `/metodo-zion`, `/metodo-zion-360`, `/academy` (+ Marco Zero), `/jornada-desenvolvimento`, `/inscreva`, `/livros/*` (9 e-books) |
| Clube e parceiros | `/club`, `/clube`, `/collection`, `/parceiro`, `/land-members` (+ privacidade) |
| Glamping Store | `/store`, `/store-v1`, `/store/comprar`, `/glamping` |
| **Funil do diagnóstico grátis** | `/raio-x`, `/diagnostico`, `/diagnostico-b`, `/diagnostico-previo`, `/diagnostico/agendar`, `/diagnostico/resultado`, `/land-bank` (+ documentos) |
| **Funil pago (Asaas)** | `/dossie-de-viabilidade`, `/dossie/*` (pagamento, gerando, obrigado, briefing), `/pagamento-confirmado`, `/consultoria/obrigado`, `/hub/obrigado` |
| Reunião | `/reuniao`, `/reuniao/$`, `/sessao` |
| Nova | `/sessao-zion-360` (só rascunho no Lovable, ainda não publicada) |
| Restritas e APIs | `/admin/*`, `/equipe/*`, `/login`, `/api/public/*` (webhooks Asaas, Hotmart, ClickMax, Land Bank, sessão agendada/liberar). **Não mexer.** |

## 3. Achados

### A. Diagnóstico grátis espalhado (para tirar ou trocar)
- **Home** (`HomeSections.tsx`): "Você preenche o diagnóstico gratuito" (passo 1), "O diagnóstico preliminar é gratuito e sem compromisso", três botões "Diagnóstico gratuito" e "Diagnóstico gratuito do meu terreno" (todos para `/land-bank`), "Grátis, sem compromisso, em menos de 5 minutos".
- **HeroVenda** (topo da home de venda): link "Não sei por onde começar: fazer o diagnóstico grátis" → `/raio-x`.
- **Inscreva**: "Faça o diagnóstico grátis" → `/raio-x`.
- **Academy**: seção "Comece pelo diagnóstico gratuito" com botão.
- **`/diagnostico`, `/diagnostico-b`, `DiagnosticoPage`**: "O diagnóstico é gratuito mesmo?", "Fazer meu diagnóstico gratuito", "sem custo", títulos e descrições de SEO.
- **`/dossie-de-viabilidade`**: "Começar pelo diagnóstico gratuito", "só depois do diagnóstico gratuito", "Você fica sabendo no diagnóstico gratuito, antes de pagar qualquer coisa".
- **Land Bank** (`OfertaLandBank`, `OfertaDossie`, `ResultadoView`): "Faça primeiro, é grátis", "resultado grátis (Etapa 1)", "webinário gratuito toda quinta às 20h" (o link está vazio, então o bloco fica oculto).
- **`/dossie/pagamento`, `/dossie/obrigado`**: "Faça o diagnóstico gratuito".
- **Textos legais**: `/termos` ("Escopo e limites do diagnóstico gratuito e do Dossiê") e `/privacidade` ("dados informados no diagnóstico gratuito").
- **Máquinas de busca**: `public/llms.txt` ("Diagnóstico prévio gratuito"), `sitemap.xml`.
- **Conteúdo do dossiê gerado** (`dossieEngine`): rótulos "Declarado no diagnóstico gratuito" (interno, não precisa mudar).
- **Páginas estáticas do `docs/` servidas pelo site**: "Reunião sem custo" e "sem custo para agendar" em `land-members`, `zion-collection`, `parceiro-zion/inscricao`; agenda embutida em `diagnostico-previo`, `reuniao-direta`, `agendar`, `sessao`.

### B. Ofertas e preços que se sobrepõem
| Oferta | Preço | Onde | Entrega | Conflito com a Sessão 360° |
|---|---|---|---|---|
| Diagnóstico de Viabilidade | R$ 47 | `/dossie-de-viabilidade` (Asaas) | Dossiê PDF, mapa mental, plano de 30/60/90 dias | **Alto**: promete o mesmo dossiê e o mesmo plano, por 1/6 do preço, e só depois do grátis |
| Jornada do passo a passo | R$ 270 (6x R$ 45) | HeroVenda, `/inscreva`, Asaas `zrhq4rk…` | Curso online + Zion Land Members + Radar | **Alto**: mesmo preço, produto diferente, checkout diferente; os dois incluem Land Bank |
| Consultoria prévia com o Bruno | R$ 490 (10x R$ 49) | HeroVenda, `/inscreva`, Asaas `r053uyk…` | Conversa de 45 min, "vira crédito na mentoria" | **Alto**: é outra "consultoria com o Bruno", mais cara |
| Mentoria / "a Zion faz por você" | sob consulta | HeroVenda (WhatsApp) | — | Baixo |
| Bubble Zion (Store) | — | `/store` | — | Nenhum |
| Sessão Zion 360° (nova) | R$ 270 | ClickMax | Sessão 60 min, dossiê, plano 30/60/90, Land Bank, área de membros | — |

Além disso, `/pagamento-confirmado` manda quem pagou o R$ 47 ou o R$ 270 da Jornada "agendar a reunião de diagnóstico depois do dossiê", usando a agenda que agora é da sessão paga.

### C. Dois sistemas de pagamento
O site cobra pelo **Asaas** (webhooks em `/api/public/asaas*`, tags no ClickMax). A Sessão 360° cobra pelo **checkout do ClickMax**. Funciona, mas o financeiro, as tags e o acesso ficam em dois caminhos. Não unificar agora.

### D. Reunião e agenda
- `/diagnostico-previo` descreve "Sem custo para agendar".
- `/reuniao`, `/reuniao/$`, `/sessao` e `/diagnostico/agendar` levam à agenda que agora é só da sessão paga.
- `produtosProjects.ts`: botão "Agendar reunião" → `/contato`.

### E. O que está certo e deve ficar
- Glamping Store (`/store`), livros, método, fundador, cases, Clube/Collection, Land Members: sem relação com o grátis, só precisam apontar para a escada final.
- Todo o back-end (`/api/public/*`, `/admin`, `/equipe`): não mexer.

## 4. Desenho de harmonia proposto (para aprovação)
**Porta única:** todo botão de entrada da home e das páginas vai para `/sessao-zion-360` (Sessão 360°, R$ 270, ClickMax).
**Escada que sobra:** Sessão 360° (R$ 270) → Mentoria / "a Zion faz por você" (sob consulta). O Land Bank continua como benefício incluso na sessão.
**O que sai da vitrine (sem apagar nada):**
1. Diagnóstico grátis / Raio-X: botões, textos e FAQ trocados pela sessão; as rotas `/raio-x`, `/diagnostico*` e `/land-bank` ficam fora do menu e do sitemap (não apagadas, para não quebrar anúncios e links já enviados).
2. R$ 47 (Dossiê de Viabilidade): fica **desligado da vitrine**; `/dossie/*` continua existindo para quem já pagou.
3. R$ 490 (Consultoria prévia) e R$ 270 da Jornada: tirar do HeroVenda e do `/inscreva`; decidir o destino de cada um.
4. "Sem custo para agendar" e "reunião sem custo": trocar nas páginas do site e do `docs/`.
5. `/termos`, `/privacidade`, `llms.txt`, sitemap: atualizar.

**Ordem de execução (cada etapa em rascunho, você vê antes de publicar):**
1. Home, HeroVenda, Inscreva, Academy (todos os botões de entrada).
2. Páginas de reunião e do `docs/` (agendar/sem custo).
3. Funil do grátis e do R$ 47 (tirar da vitrine, manter rotas).
4. Textos legais, `llms.txt`, sitemap.
5. Revisão final por busca de termos e navegação no celular.

## 5. Riscos
- **Anúncios e e-mails já enviados** apontam para `/raio-x`, `/diagnostico`, `/land-bank`: manter as rotas vivas e, se quiser, redirecionar para a sessão.
- **Quem já pagou** o R$ 47 ou o R$ 270 da Jornada precisa continuar acessando `/dossie/*` e o Land Bank.
- **Tags e automações do ClickMax** ligadas ao funil do grátis (META | FORM LAND BANK, DIAG) continuam existindo; não desligar sem decisão.
- Publicar o site do Lovable troca tudo de uma vez: por isso rascunho primeiro.

## 6. Decisões necessárias
1. O Diagnóstico de Viabilidade R$ 47 sai da vitrine, fica como está ou vira outra coisa?
2. A Consultoria prévia R$ 490 e a Jornada R$ 270 saem, ficam ou se fundem com a Sessão 360°?
3. `/raio-x` e `/diagnostico*`: apenas saem do menu ou redirecionam para a sessão?
4. A mudança começa pela home (etapa 1) já neste rascunho?
