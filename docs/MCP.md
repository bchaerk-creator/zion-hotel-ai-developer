# Servidores MCP do projeto

O arquivo `.mcp.json` na raiz configura servidores MCP com escopo de projeto: qualquer
pessoa que abrir este repositório no Claude Code recebe a mesma configuração.

## 21st.dev (Magic)

Geração e busca de componentes de UI. Gera variantes polidas de um componente,
abre uma página no navegador para você escolher e devolve o código ao agente.

- **Site:** https://21st.dev/mcp
- **Transporte:** HTTP (`https://21st.dev/api/mcp`)
- **Autenticação:** header `x-api-key`, lido da variável de ambiente `API_KEY_21ST`
- **Custo:** o plano Pro (Magic Generate) é pago — US$ 20/mês na data desta configuração

### Como ativar na sua máquina

1. Pegue sua API key em https://21st.dev/magic/console
2. Exporte a variável no seu shell (`~/.zshrc`, `~/.bashrc` ou equivalente):

   ```bash
   export API_KEY_21ST="sua_chave_aqui"
   ```

3. Reabra o terminal e o Claude Code neste diretório. Na primeira vez o Claude Code
   pede aprovação para servidores MCP definidos no projeto — aceite.
4. Verifique:

   ```bash
   claude mcp list
   ```

A chave **nunca** entra no repositório: `.mcp.json` guarda só a referência
`${API_KEY_21ST}`, que é expandida a partir do ambiente em tempo de execução.

### Observação sobre comandos antigos

Tutoriais mais antigos mandam rodar:

```bash
claude mcp add magic --scope user --env API_KEY=... -- npx -y @21st-dev/magic@latest
```

O pacote `@21st-dev/magic` hoje é apenas um proxy de compatibilidade mantido para
configurações legadas. A configuração acima é a atual, gerada por
`npx @21st-dev/cli@latest init --client claude`.

Além disso, `--scope user` grava em `~/.claude.json`, que é pessoal e não versionado.
O escopo de projeto usado aqui é o que faz a configuração viajar com o repositório.

### CLI opcional

O `@21st-dev/cli` também funciona fora do MCP, direto no terminal:

```bash
npx @21st-dev/cli@latest login
npx @21st-dev/cli@latest search "hero section hotel" --type c
npx @21st-dev/cli@latest generate "card de reserva para glamping"
```
