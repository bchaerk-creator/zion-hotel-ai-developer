# Organização das áreas de membros · 12/11/2026

Reorganização aprovada por Bruno em 12/11/2026. Nada foi apagado. Nenhum aluno foi criado, movido ou removido. Não foram tocados: Land Bank, Zion Collection, ofertas, produtos, checkouts, fluxos, tags, webhook/Asaas. Workspace `e87e8ba9-37cf-4c54-9a97-3e4e1b01827a`.

## Antes e depois

| Item | Id | Antes | Depois |
|---|---|---|---|
| Portal | `6d1b8c4d-05b0-4bf8-b3ba-5e8e1d0b2b79` | Zion Hospitality Business | **Zion · Jornada do Desenvolvimento** (subdomínio `mentoria-zion` igual) |
| Descrição do portal | idem | "Academia de Negócios de Hospedagem · Do terreno ao negócio que funciona. Uma iniciativa Zion Hotel Group International." | "Aprenda o passo a passo para transformar o seu terreno em um projeto de hospedagem. Uma iniciativa Zion Hotel Group International." |
| Turma do Terreno (a do webhook) | `a490c3c8-17c5-478f-b017-3986bce21166` | Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso | **Jornada do Desenvolvimento · Trilha 1** (mesmo id, mesmos 2 conteúdos) |
| Turma Fundadores | `2c33680d-9f95-4c60-9d3f-452b4cf94d26` | Turma Fundadores · Mentoria em grupo | **Arquivo · Turma Fundadores (não vender)** |
| Biblioteca (curso) | `6ce56665-eacd-4513-b8d3-bb2a3a06528d` | Biblioteca · Método Zion 360° | **Biblioteca · Material de apoio (e-books Método Zion 360°)** (continua ligada à turma) |
| Curso do Terreno | `fa9a6c54-e40c-4ee0-99cc-ee6ec70e68fb` | 9 módulos, 58 aulas | 10 módulos, 63 aulas |

As 6 turmas "Arquivo" vazias do portal: não mexi (já têm o prefixo).

## Ordem dos módulos do curso (depois)

1. **Comece aqui · Onboarding** (novo) `206a5a61-c1cf-4759-bb2c-772d6baa1d72`
2. Marco Zero · A visão de toda a jornada `da251ac7`
3. Pilar 1 · Território e destino `a271c00b`
4. Pilar 2 · Mercado e demanda `d77157a5`
5. Pilar 3 · Produto e tipologias `2c0ab9f3`
6. Pilar 4 · Modelo de negócio `3f0b830d`
7. Pilar 5 · Masterplan faseado `c7e0e5c6`
8. Pilar 6 · Pré-viabilidade `6e06c29d`
9. Pilar 7 · Capital e Dossiê `430dbc2f`
10. Bônus · Ferramentas Zion Collection Club `48b713d7` (último)

Nomes dos módulos, descrições, URLs e aulas existentes: sem alteração. Não achei erro evidente de título, então nenhum título foi corrigido.

## Conferência das duplicatas (antes de copiar)

Comparei o módulo Marco Zero do Terreno com o Panorama `03aa8ff9-a274-4a33-8506-2bdf5dc4d87f`. As duplicatas existem, com a mesma URL: Vídeo 1 (`youtu.be/D7Htb0ED7eA`), Vídeo 2 (`youtu.be/SJ1Cy5vqCJM`), e-book Marco Zero (`Marco-Zero-ebook.pdf`) e a aula interativa (`marco-zero-aula/`). Por isso não foram copiados. Os 5 itens copiados não têm correspondente no Terreno (o Terreno tem "Comece aqui · Como usar o curso" em PDF, que é outra aula).

## Aulas criadas no módulo "Comece aqui · Onboarding" (cópias; as originais do Panorama continuam onde estavam)

| # | Aula | Tipo | Id |
|---|---|---|---|
| 1 | 0 · Comece aqui · Bem-vindo à Zion (vídeo `onboarding-land-bank.mp4`, descrição sem "Land Bank") | vídeo | `941b61a0-a14c-4c69-bd41-0458638543e5` |
| 2 | Monte o seu dossiê inicial (`/dossie/`) | link | `cc238783-d1b3-403c-840c-22972c65df65` |
| 3 | Agende a sua reunião de diagnóstico e feedback (`/agendar/`) | link | `2b6d424c-a198-4a4e-8e61-8ba7cd76e3d0` |
| 4 | Suporte · Tire suas dúvidas aqui (link do chat) | link | `0d3f7093-6e75-4f62-a4cc-f5292e805cb9` |
| 5 | Bônus · E-book Glamping (PDF) | documento | `7e9c378b-e059-4f29-b684-10171fc9beb3` |

Nas aulas 2 e 4 também retirei do texto as menções a "reunião estratégica" e "masterclass" (a aula 4 antes citava masterclass). O vídeo de boas-vindas ficou com duração 0: o campo não aceitou o valor 125 (a atualização voltou com 0). O vídeo tem 125 s no Panorama.

## Capas

- Verifiquei com `curl -sI`: as capas usadas respondem 200. As pastas `/capas-zion/` e `/trilha1/capas/` sozinhas dão 404 (é o esperado no GitHub Pages, que não lista pastas); os arquivos dentro respondem 200.
- Módulo novo: `capas-zion/trilha-1-modulo-h.jpg` (horizontal) e `trilha-1-modulo-v.jpg` (vertical), a capa oficial da Trilha 1. Não há capa própria de "Comece aqui", então usei a da Trilha 1.
- Aula "Monte o seu dossiê inicial": `trilha1/capas/mz-c-faca.jpg`. Aula do e-book Glamping: `assets/ebooks/glamping-capa-h.jpg`. As outras três aulas ficaram sem capa.
- Nenhuma imagem gerada foi usada como foto real.

## Conferência final

- Turma `a490c3c8`: mesmo id, continua com os 2 conteúdos (Terreno 63 aulas em 10 módulos + Biblioteca 36 aulas em 18 módulos).
- Alunos da turma: a leitura lista 2 (antes e depois da mudança, os mesmos 2). A auditoria de hoje dizia 3; a diferença vem da contagem da auditoria (`totalMemberUsers`), não de mudança minha. Vale conferir no painel.
- O curso do Terreno continua ligado às 3 turmas (Jornada Trilha 1, Arquivo Fundadores e Land Bank Candidatos), então o módulo novo também aparece no Land Bank. Isso é consequência de ser o mesmo curso.

## Pendências

- **Masterclass:** a aula "Masterclass ao vivo" do Panorama (Land Bank) cita quinta 5/11 e já passou. Não foi copiada; precisa ser reescrita ou desligada por Bruno.
- **Capas que faltam:** capa própria do módulo Comece aqui; capas das aulas Boas-vindas, Agende e Suporte.
- **Duração dos vídeos:** o vídeo de boas-vindas ficou com 0; no Terreno só 8 de 17 vídeos têm duração.
- **Certificado:** desligado no Terreno (só a Biblioteca tem).
- **Land Bank:** o portal e o Panorama continuam como estavam, com o Terreno ligado também lá. Falta decidir se Land Bank vira turma deste portal.
- **Alunos a migrar:** nenhum foi movido. Fundadores (1) e os alunos de turmas Arquivo seguem onde estão.
- **Título do portal no rodapé:** o campo `footerDescription` ainda diz "Zion Hospitality Business · Academia de Negócios de Hospedagem" (não pedi mudança; sugiro alinhar).
- Oferta Trilha 1 (R$ 970) segue incompleta; não foi tocada.
- Os 2 rascunhos do Gamma desligados e as aulas duplicadas do Marco Zero continuam só no Panorama.

## Como reverter

- **Portal:** `portals_update` no id `6d1b8c4d...` com `name` "Zion Hospitality Business" e a descrição antiga (tabela acima).
- **Turma do Terreno:** `classrooms_update` em `a490c3c8...` com `name` "Transforme Seu Terreno em um Projeto de Hospedagem de Sucesso".
- **Turma Fundadores:** `classrooms_update` em `2c33680d...` com `name` "Turma Fundadores · Mentoria em grupo".
- **Biblioteca:** `content_update` em `6ce56665...` com `title` "Biblioteca · Método Zion 360°".
- **Módulo novo e aulas:** o módulo e as 5 aulas são novos. Para desfazer, primeiro `modules_organize_positions` devolvendo o Marco Zero à posição 1 e os pilares/bônus às posições 2 a 9 (ordem antiga), e depois apagar o módulo `206a5a61...` (`modules_delete`, exige "aprovado" de Bruno). Ou, sem apagar, desligar as 5 aulas com `lessons_toggle_enabled`.
