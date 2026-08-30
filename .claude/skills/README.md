# Skills do projeto

## UI UX Pro Max

Skills de inteligência de design de UI/UX instaladas neste repositório.

- **Origem:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Versão:** 2.13.0
- **Commit de origem:** 8bd29e7 (`feat(design): add Atlas Cloud logo provider (#447)`)
- **Licença:** MIT (ver `LICENSE-ui-ux-pro-max`)
- **Instalado em:** 2026-08-30

### Skills incluídas

| Skill | Para que serve |
|---|---|
| `ui-ux-pro-max` | Núcleo: base local pesquisável com 79 estilos, 192 paletas/perfis de produto, 74 pares tipográficos, 119 diretrizes de UX, 105 ícones, 17 presets GSAP, 25 tipos de gráfico e 22 stacks |
| `ui-styling` | Componentes shadcn/ui, Tailwind, designs em canvas (inclui fontes em `canvas-fonts/`) |
| `design` | Identidade de marca, design tokens, geração de logo, programa de identidade corporativa |
| `design-system` | Arquitetura de tokens em três camadas (primitivo → semântico → componente) e specs de componentes |
| `brand` | Voz de marca, identidade visual, frameworks de mensagem |
| `banner-design` | Banners para redes sociais, anúncios, heros e material impresso |
| `slides` | Apresentações em HTML com Chart.js e design tokens |

### Requisito

Python 3.x (apenas biblioteca padrão — os scripts não instalam nada nem fazem chamadas de rede).

### Uso

As skills ativam sozinhas quando a tarefa envolve UI/UX. Para consultar a base diretamente:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "landing page hotel de luxo" -d style
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "paleta wellness" -d color --json
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "hero section" -s nextjs
```

### Como atualizar

```bash
npm install -g ui-ux-pro-max-cli
uipro update
```

Ou recopiar `.claude/skills/` a partir de um clone novo do repositório de origem.

### Atenção: colisão de nomes

A skill `design` tem o mesmo nome da skill nativa `design` (canvas do Claude Design). Skills do projeto têm precedência sobre as nativas, então a nativa fica sombreada enquanto esta estiver aqui. Se preferir manter a nativa, remova `.claude/skills/design/`.
