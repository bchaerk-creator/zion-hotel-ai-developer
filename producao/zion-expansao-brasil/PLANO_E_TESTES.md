# Plano de entrega, acesso protegido e testes · Sessão Zion 360° (R$ 270)

## O que foi criado no ClickMax (tudo em rascunho; nada publicado)
| Item | Id |
|---|---|
| Produto "Sessão de Diagnóstico e Estratégia Personalizada Zion 360°" (Consultoria) | `14c6c51e-b24e-4fbc-a87f-3fb298c75ae5` |
| Oferta R$ 270 · Pix + cartão até 12x · sem boleto · sem afiliados · reembolso 7 dias · ZIONACADEMY | `037959a0-c602-4323-8e2f-e99902f377f4` (hash do checkout `W11sGasqD2`) |
| Área de membros: conteúdo + módulo "Comece aqui" + 2 aulas de texto | conteúdo `16f37c16…`, módulo `b4dbcda8…` |
| Turma nova no portal Zion Collection (não padrão, sem membros; turmas existentes intactas) | `a6db275c-eeb1-4a78-a9a2-dadc24339006` |
| Entrega da oferta = essa turma (`offers_add_membership_delivery`) | entrega `a02a9f10…` |
| ~~Quiz Raio-X~~ | **Removido em 21/11 por decisão do Bruno: não haverá Raio-X gratuito. O rascunho `963286c9…` foi apagado (0 respostas).** |
| Landing (draft, `/sessao-zion-360`) | página `3bf6dd22-051e-4f1a-92b0-0686ee168a96` |

**Ocorrência:** ao salvar o preço com `offers_update`, a oferta passou sozinha para `approved` (`moderatedAt` 21/11 23:04). Eu não enviei para aprovação. Ela ainda não está em nenhuma página publicada nem anúncio.

## Regra inegociável: calendário só após o pagamento confirmado
**Estado: NÃO validada. Não declare como pronta.**
O que existe e é nativo: a turma só é liberada pela entrega da oferta, que depende da transação paga (não por tag nem redirecionamento). A turma não contém nenhum link de agenda.
O que falta e por quê:
1. **Agenda paga.** O ClickMax só tem agenda por link público (assinado só na gestão da reserva). Não há ferramenta para criar agenda por API. Desenho proposto, a validar:
   - criar no painel uma agenda nova "Sessão Zion R$ 270" (60 min, fuso America/Sao_Paulo, buffer e limites que Bruno aprovar, verificação por código ligada), **sem divulgar o link em nenhum lugar público**;
   - colocar o link só numa aula da turma paga (lição 3, hoje inexistente);
   - **fluxo de guarda** no gatilho `crm.scheduling.booked` desta agenda: se o contato não tem a marca de "pagamento confirmado" (aplicada pelo gatilho `checkout.transaction.paid.v1` da oferta `037959a0…`), cancelar a reserva e avisar. Precisa confirmar se o fluxo consegue cancelar a reunião.
   - **limite honesto:** um link copiado por quem pagou ainda permitiria reservar até o fluxo de guarda agir. O ClickMax não oferece link de uso único. Alternativa de controle total: Bruno reserva o horário (`scheduled_calls_create`) depois do pedido de horário no formulário privado, sem autoagendamento.
2. **Testes reais de pagamento** (Pix, cartão, parcelado, pendente, recusado, reembolso, chargeback, reenvio de webhook, Pix atrasado, acesso sem compra): não executados. O vendedor está `pending` e eu não faço compra real. Precisam de teste de Bruno ou da liberação do vendedor.
3. **Webhook autenticado e verificação na fonte:** neste caminho quem verifica é o próprio checkout nativo do ClickMax (ticto). Não há webhook próprio para auditar. Se Bruno quiser trilha externa (Land Bank, Meta CAPI), é uma camada nova a aprovar.
4. **Integração Land Bank:** não feita (só a promessa na página). Desenho: fluxo `checkout.transaction.paid.v1` → marca "LAND BANK | SESSÃO 270 PAGA" + cadastro sujeito a avaliação, sem liberar Clube nem cursos pagos. Pendente de "aprovado" (mexe em automações).

## Jornada pós-compra (a configurar após aprovação)
Pagamento → turma (aulas 1 e 2 prontas) → formulário privado (modelo em `insumos/QUIZZES.md`; fotos e documentos só em ambiente seguro) → agenda protegida → confirmação + link de vídeo → lembretes (véspera, manhã, 1 h, 15 min) → sessão → gravação só com consentimento expresso separado do marketing (senão, anotações) → transcrição → IA → **revisão humana** → PDF 12–20 p. + plano 30/60/90 anexados à turma e ao perfil → Land Bank.
Dossiê: fatos, resumo, diagnóstico, potencial, riscos, lacunas, hipóteses de números (rotuladas), capitalização e parceiros, argumento comercial, ações 30/60/90 com responsável, prioridade e critério. Prazo proposto: 2 dias úteis (validar). Sem dados inventados nem garantia de crédito, retorno ou viabilidade. Retenção e exclusão de dados: política a definir (LGPD).
A transcrição "autorizada da consultoria" citada no pedido **não veio no pacote**; sem ela não montei dossiê.

## Eventos e UTMs
Entrada A (landing): `utm_source=meta&utm_medium=paid&utm_campaign=sessao-270&utm_content=<criativo>`. Entrada B (formulário Meta): ver `META.md`. Pixel/CAPI: ViewContent, Lead, InitiateCheckout; **Purchase só com pagamento real** (não configurado; depende de pixel e aprovação). Nada de dado financeiro ou documento em evento Meta.

## Pendências de Bruno (decisões)
1. Enviar `00_VIDEO_ORIGINAL.mp4`, os 6 JPG e a transcrição autorizada (ou confirmar que `expansao-zion.mp4` é o vídeo).
2. Política de reagendamento, cancelamento, indisponibilidade e prazo do dossiê; duração dos acessos; capacidade de agenda (sessões por dia, buffer).
3. Parcelamento: está em até 12x; conferir no checkout o custo total mostrado ao comprador.
4. Escolher o desenho da agenda paga (link na aula + guarda, ou reserva feita pela equipe).
5. Liberar o vendedor ClickMax (hoje pending) para testar compras.
6. "Aprovado" para: ativar o quiz, publicar a landing, mudar a Zaya, pausar a campanha ativa, criar campanhas, ligar Land Bank.
