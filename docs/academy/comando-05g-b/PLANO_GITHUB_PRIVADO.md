# Plano · conexão da ZAIOS a um repositório GitHub privado

Comando 05G-B · 09/11/2026 · **Plano. Nada foi conectado, criado ou sincronizado.**

## 1. Objetivo

1. **Integridade:** obter os arquivos diretamente da origem, com hash calculado sobre o repositório, e comparar com as cópias auditadas (commit `ec21ad5`).
2. **Canal de implementação:** permitir mudanças pequenas e revisáveis (um commit por decisão), com revisão de diff e reversão por git, em vez de mensagens ao agente do Lovable.

## 2. Origem, titularidade e permissões

| Item | Proposta |
|---|---|
| Repositório de origem | Projeto Lovable "Zaios" (id `51fa7ea5-6cb2-4867-9bf7-6e1cbb3e71dc`), pela integração nativa do Lovable com o GitHub |
| Titular | Conta do Bruno no GitHub (`bchaerk-creator`) ou organização da Zion, a decidir |
| Visibilidade | **Privado** |
| Quem conecta | O Bruno, no editor do Lovable (integração GitHub). O Claude não tem como fazer isso nem deve |
| Acesso do Claude | Leitura, adicionando o repositório a esta sessão (`add_repo`, acesso "read"). Escrita só numa etapa futura autorizada e numa branch separada, nunca direto na principal |

## 3. Arquivos necessários para a prova de integridade

- **Motor:** `src/calc/{tipos,capex,receitas,viabilidade,operacao,funcoes,convencoes,formatar,estatisticas}.ts`
- **Composição:** `src/exercicios/{capex,receitas,viabilidade,financas,mercado}-calculo.ts`
- **Testes:** `src/test/*.test.ts`
- **Para rodar a suíte completa da ZAIOS no ambiente local:** `package.json`, o arquivo de travas de dependências e a configuração do vitest

## 4. Método dos hashes

1. Clonar o repositório privado em leitura, na área temporária da sessão. Nada vai para o repositório público.
2. Verificar se o commit `ec21ad5606fd3d46f610f95d2efcbc3169386546` existe no histórico (`git cat-file -e`).
   - Se existir: fazer o checkout desse commit.
   - Se o histórico do GitHub tiver outros identificadores: localizar o commit pela data (07/11/2026 19:55 UTC) e pelo conteúdo, e registrar a diferença.
3. Calcular o SHA-256 de cada arquivo da seção 3 e comparar com os hashes registrados no 05E, no 05F e no 05G-B.
4. Rodar de novo as suítes 05E, 05F, 05G-B e aceite **a partir do clone**, em vez das transcrições.
5. **Se os hashes forem iguais:** a ressalva de integridade é encerrada para esses arquivos. **Se forem diferentes:** registrar as diferenças e refazer os testes a partir do clone.

## 5. Riscos

| Risco | Mitigação |
|---|---|
| **Sincronização bidirecional:** pelo que se sabe da integração do Lovable, mudanças na branch principal do GitHub voltam para o projeto (produção) | O Claude não escreve na branch principal. Nesta etapa o acesso é só de leitura |
| Exposição do código | Repositório privado. Nunca copiar o código para o repositório público `zion-hotel-ai-developer` |
| O `.env` do projeto vai para o repositório | Ele existe no projeto (visto no `list_files`; o conteúdo não foi lido). Costuma ter só chaves públicas do Supabase, mas precisa ser revisado. Repositório privado e sem colaboradores além do Bruno |
| Escrita acidental pelo Claude | Acesso só de leitura na sessão de integridade. Escrita apenas com autorização, numa branch separada e com revisão |

## 6. Credenciais, custos e créditos

- **Credenciais:**
  - a conexão é feita pelo Bruno no Lovable, com a conta GitHub dele;
  - o Claude não precisa receber token nem senha: o acesso da sessão vem da integração GitHub já usada neste ambiente;
  - se a organização ou o repositório não estiverem liberados, o Bruno autoriza no app do Claude no GitHub.
- **Custos e créditos:**
  - a conexão é configuração do projeto e, pelo que se sabe, não aciona o agente;
  - **não é possível confirmar daqui** se há custo ou consumo de créditos. Conferir no painel ou na documentação do Lovable antes de conectar;
  - o GitHub privado não tem custo no plano gratuito.

## 7. Reversão

1. Desconectar a integração GitHub nas configurações do projeto no Lovable. O projeto continua funcionando.
2. Arquivar ou apagar o repositório privado no GitHub.
3. Remover o repositório da sessão do Claude.

Nenhuma dessas ações altera o código em produção.

## 8. Autorização necessária

"Autorizo conectar a ZAIOS a um repositório GitHub privado em [conta], só para leitura e prova de integridade."

A escrita ou a implementação por esse canal exigem uma autorização separada.
