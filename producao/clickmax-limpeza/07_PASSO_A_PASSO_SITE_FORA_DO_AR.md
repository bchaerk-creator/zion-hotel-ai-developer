# Passo a passo · voltar o site da Zion para o ar (13/11/2026)

Situação (pelos registros, não reverificada ao vivo): o domínio `zionhotelgroup.com` foi cadastrado no ClickMax em 12/11 (lista de domínios de redirecionamento, status "connecting"). O DNS de `www.zionhotelgroup.com` passou a apontar para o ClickMax/Entri, que responde 404 em todas as páginas. O site continua intacto na Lovable. O endereço `lovable.app` redireciona para `www.zionhotelgroup.com`, então hoje nenhum endereço abre o site.

Nada foi executado por mim. Quem tem acesso ao DNS e à Lovable executa. O Claude só prepara e confere depois.

## Passo 0 · Confirmar (1 minuto)
Abra no celular (4G, fora do Wi-Fi) `https://www.zionhotelgroup.com`. Se mostrar 404 ou erro, siga. Se abrir normalmente, pare e me avise.

## Passo 1 · Paliativo imediato (Lovable, 2 minutos)
Projeto "Zion Hospitality Platform" → Configurações → Domínios. No `www.zionhotelgroup.com`, escolha **Unset as primary**. Assim o endereço `lovable.app` volta a servir o site enquanto o DNS é consertado.

## Passo 2 · Consertar o DNS (onde o domínio é gerenciado)
1. Entre no painel do provedor de DNS de `zionhotelgroup.com`. Se não souber qual é, é o do registro do domínio. Procure por Registro.br, GoDaddy, Wix ou Cloudflare e me diga qual.
2. Anote os registros atuais (tire print) antes de mexer, para poder desfazer.
3. Para `www` e para a raiz (`@`), remova os registros que apontam para o ClickMax/Entri (IPs `13.248.221.243`, `76.223.74.74` e o CNAME `entri-domains.clickmax.space`).
4. Crie para `@` e para `www` um registro **A** com valor **185.158.133.1** (IP que a Lovable informa).
5. Mantenha os registros TXT de verificação que a Lovable pedir em Configurações → Domínios.
6. Na Lovable, clique em **Check again** nos Domínios e, se estiver tudo certo, volte a marcar `www.zionhotelgroup.com` como primário.
7. O DNS pode levar de minutos a algumas horas para propagar.

## Passo 3 · Limpar o ClickMax
No ClickMax, na lista de domínios de redirecionamento, remover `zionhotelgroup.com` (status "connecting"). Se for preciso um domínio próprio para links, páginas ou checkout, use um **subdomínio**, por exemplo `go.zionhotelgroup.com` ou `pay.zionhotelgroup.com`, com os registros que o ClickMax indicar. Nunca o domínio raiz do site.

## Passo 4 · Conferir (Claude, só leitura)
Quando você disser "feito", eu confiro: resposta da Home e das rotas principais (clube, parceiro, land-members, raio-x, store), `lovable.app` e o subdomínio novo, se houver. As ferramentas daqui sofrem bloqueio de proxy, então pode ser preciso que você me mande um print ou o código de resposta.

## Atenção
- Não exclua nada na Lovable. A correção é só de endereço.
- Links de anúncios, WhatsApp e e-mails que apontam para `zionhotelgroup.com` voltam a funcionar quando o DNS propagar.
- Se algum link do Club ou do Land Bank depender do ClickMax no domínio raiz, ele precisa migrar para o subdomínio. Eu listo esses links na conferência.
