# Prompt de IA · Revisar o Painel de Gestão (Módulo 1)

Uso: o membro exporta o Painel de Gestão em PDF (ou copia a aba Metas e donos da planilha), abre qualquer assistente de IA, cola o prompt abaixo inteiro e, logo depois, o conteúdo do painel. O texto em `docs/trilha2/materiais/Modulo-1-Prompt-de-IA.txt` é gerado deste arquivo por `src/build_resumo.py`.

```
Você vai revisar o Painel de Gestão de uma hospedagem pequena (cabanas, chalés, casa de temporada, pousada, glamping ou hotel pequeno). O painel segue o Método Zion 360°: cinco indicadores (ocupação, diária média, resultado do mês, nota das avaliações e taxa de venda direta), um dono para cada um, uma meta para o mesmo mês daqui a 12 meses e uma reunião semanal de trinta minutos com os mesmos cinco números.

Regras para a sua resposta:
- Use só os números que eu colar. Não invente média de mercado, ocupação da região, diária de concorrente nem "meta ideal".
- Não prometa resultado. Meta é decisão de gestão, não previsão.
- Escreva em português simples, sem siglas. Se precisar de um termo técnico, explique em uma linha.
- Quando algo for opinião sua e não conta, diga "sugestão".

Faça quatro blocos:
A) As metas: para cada indicador, diga a variação entre o ponto de partida e a meta. Confira a conta: noites que a meta de ocupação pede (meta de ocupação × noites disponíveis) e receita de hospedagem que as metas pedem (noites × meta de diária). Se eu informei ocupação de equilíbrio ou número de corte, diga se a meta fica acima deles.
B) Coerência entre as metas: as metas de ocupação, diária e resultado apontam na mesma direção? Se uma meta está abaixo do ponto de partida, pergunte se é decisão (por exemplo, trocar ocupação por diária) ou engano.
C) Donos e reunião: cada número tem dono? A reunião tem dia, hora e trinta minutos? Diga o que falta, sem julgar.
D) Três perguntas para a primeira reunião: formule três perguntas que eu deva responder na primeira reunião semanal, ligadas aos números mais frágeis deste painel (por exemplo: "de onde vieram as reservas diretas desta semana?"). Perguntas, não promessas.

Termine com uma linha: "Esta revisão confere a lógica do painel com os números que você informou. Ela não substitui a sua decisão e não é previsão de resultado."

Aqui está o meu Painel de Gestão:
```

---

Depois da revisão, escreva a resposta da pergunta D na primeira linha da aba Reunião semanal da planilha.
