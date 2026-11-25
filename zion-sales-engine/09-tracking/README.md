# 09 · Tracking

**Propósito:** medir a jornada de ponta a ponta e conciliar com as vendas.
**Dono:** DATA.

**O que vai aqui:**
- Estado do pixel, da API de Conversões, das UTMs e da deduplicação.
- Requisitos de aceite (R1 a R8 em `13-relatorios/H_rastreamento.md`).
- Conciliações ClickMax × gateway × Meta e lead × comprador (`conciliacao/`).
- Funil de 8 eventos (`FUNIL_DE_EVENTOS_P0.md` §7), validação local do receptor (`VALIDACAO_EM_TESTE.md`) e públicos (`ARQUITETURA_DE_PUBLICOS.md`).

Configurar pixel, CAPI ou webhook em produção exige 'aprovado'. Tokens nunca entram no repositório nem no chat.

## Base legal, consentimento e finalidade (LGPD) · A12
Texto curto de trabalho, **a validar com orientação jurídica antes de qualquer envio ou instalação** [NC: a base legal ainda não foi confirmada por advogado].
- **Finalidade:** medir de qual anúncio veio cada compra, entregar o acesso comprado e evitar anúncio repetido para quem já comprou. Nenhuma outra finalidade (sem venda ou cessão de dados).
- **Base legal proposta [H]:** execução do contrato (dados da compra, para entregar o produto) e legítimo interesse (medição de anúncios), com aviso claro. Marketing por mensagem exige consentimento ou outra base própria.
- **Dados mínimos:** e-mail e telefone saem com hash SHA-256 para o Meta; nome só normalizado e com hash; nada de CPF, endereço ou dado sensível.
- **Snippet `persistir-utm.js`:** grava a origem (UTM, `fbclid`) no navegador por 30 dias. **Só instalar depois** de a política de privacidade e o aviso de cookies/armazenamento mencionarem esse uso. O visitante pode recusar; o site funciona sem o snippet.
- **Recuperação e lista de compradores ao Meta:** só após base legal confirmada e aviso de privacidade atualizado; envio de teste antes do real; CSV com dados de compradores **fora do repositório** (ver `../.gitignore`).
- **Direitos do titular:** pedido de exclusão ou de oposição atendido pelo suporte; registrar o que foi enviado ao Meta para poder responder.
- **E-mail de suporte:** usar e-mail de domínio da empresa, não e-mail pessoal do titular (pendente de Bruno).
