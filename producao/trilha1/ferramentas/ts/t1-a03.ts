// Trilha 1 · Aula 3 · Mercado (slug 1-3). Fonte: exercicios/aula-03.json.
import type { Calculo, ResultadoCalculos, Respostas, Veredito } from "./types";
import { brl, div, falta, fechar, fmtN, fmtPct, juntar, num, pct, pisoSeguro } from "./util";

const REGUA_OCUP =
  "Régua: 35% a 40% vende só nos fins de semana; 50% a 60% com fins de semana, feriados e datas; 65% a 85% só com procura extraordinária comprovada.";

function faixaOcupacao(o: number): string {
  if (o < 0.35) return "abaixo de 35%, abaixo da primeira faixa da régua";
  if (o <= 0.4) return "na faixa de 35% a 40%: vende só nos fins de semana";
  if (o < 0.5) return "entre faixas; a mais próxima abaixo é 35% a 40%, vende só nos fins de semana";
  if (o <= 0.6) return "na faixa de 50% a 60%: fins de semana, feriados e datas";
  if (o < 0.65) return "entre faixas; a mais próxima abaixo é 50% a 60%, fins de semana, feriados e datas";
  if (o <= 0.85) return "na faixa de 65% a 85%: só com procura extraordinária comprovada";
  return "acima de 85%; a faixa mais próxima abaixo é 65% a 85%, só com procura extraordinária comprovada";
}

export function calcular(r: Respostas): ResultadoCalculos {
  const calculos: Calculo[] = [];

  // 1. conta_semana
  const oF = pct(r, "ocup_fds"), oS = pct(r, "ocup_semana");
  const dF = num(r, "diaria_fds"), dS = num(r, "diaria_semana");
  let diariaMedia: number | null = null;
  {
    if (oF === null || oS === null || dF === null || dS === null) {
      const f = [oF === null && "ocupação de sexta e sábado", oS === null && "ocupação de domingo a quinta", dF === null && "diária do fim de semana", dS === null && "diária de domingo a quinta"].filter(Boolean) as string[];
      calculos.push({ id: "conta_semana", rotulo: "A conta da semana", valor: null, texto: `Para a conta da semana falta ${juntar(f)}.` });
    } else {
      const noites = 2 * oF + 5 * oS;
      const receita = 2 * oF * dF + 5 * oS * dS;
      const ocupJanela = noites / 7;
      diariaMedia = div(receita, noites);
      const porNoite = receita / 7;
      calculos.push({
        id: "conta_semana", rotulo: "A conta da semana", valor: diariaMedia,
        texto: diariaMedia === null
          ? "Nenhuma noite vendida na semana: a diária média fica em branco."
          : `Numa semana típica, uma unidade vende ${fmtN(noites, 2)} noites e entra ${brl(receita)}. Ocupação da janela: ${fmtPct(ocupJanela)}. Diária média de verdade (o que entra dividido pelas noites vendidas): ${brl(diariaMedia)}. Por noite disponível: ${brl(porNoite)}.`,
        detalhes: { noites_semana: noites, receita_semana: receita, ocup_janela_pct: ocupJanela * 100, diaria_media: diariaMedia, por_noite_disponivel: porNoite },
      });
    }
  }

  // 2. fds_vs_semana
  const razao = div(oF, oS);
  calculos.push({
    id: "fds_vs_semana", rotulo: "Quantas vezes o fim de semana enche mais", valor: razao,
    texto: razao === null ? "Falta a ocupação do fim de semana ou da semana (ou a da semana é zero)." : `O fim de semana enche ${fmtN(razao, 1)} vezes mais que a semana.`,
  });

  // 3. regua_amplitude
  const amp = num(r, "amplitude");
  {
    let t: string, alerta: Calculo["alerta"];
    if (amp === null) t = "Falta a amplitude: diária mais cara dividida pela mais barata do raio.";
    else if (amp > 3) { t = `Amplitude de ${fmtN(amp, 2)}: acima de 3, o destino paga pela diferença.`; alerta = "ok"; }
    else if (amp < 2) { t = `Amplitude de ${fmtN(amp, 2)}: abaixo de 2, a briga é de preço.`; alerta = "atencao"; }
    else t = `Amplitude de ${fmtN(amp, 2)}. Entre 2 e 3 a fonte não traz leitura: fica só o número.`;
    calculos.push({ id: "regua_amplitude", rotulo: "Leitura da amplitude", valor: amp, texto: t, alerta });
  }

  // 4. ocup_ano
  const mA = num(r, "meses_alta"), mF = num(r, "meses_fraco");
  const oA = pct(r, "ocup_alta"), oFr = pct(r, "ocup_fraco"), oM = pct(r, "ocup_media");
  let ocupAno: number | null = null;
  {
    let t: string;
    let alerta: Calculo["alerta"];
    const mM = mA !== null && mF !== null ? 12 - mA - mF : null;
    if (mA === null || mF === null) t = "Falta quantos meses de alta e quantos fracos.";
    else if ((mM as number) < 0 || mA < 0 || mF < 0) t = "Meses de alta mais meses fracos passam de 12: confira.";
    else {
      const precisa: [number, number | null, string][] = [[mA, oA, "ocupação da alta"], [mM as number, oM, "ocupação dos meses médios"], [mF, oFr, "ocupação dos meses fracos"]];
      const f = precisa.filter(([m, o]) => m > 0 && o === null).map(([, , n]) => n);
      if (f.length) t = `Para a média do ano falta ${juntar(f)}.`;
      else {
        ocupAno = (mA * (oA ?? 0) + (mM as number) * (oM ?? 0) + mF * (oFr ?? 0)) / 12;
        t = `Ocupação média do ano: ${fmtPct(ocupAno)}, ${faixaOcupacao(ocupAno)}. ${REGUA_OCUP}`;
        alerta = ocupAno >= 0.65 - 1e-12 ? "atencao" : "ok";
      }
    }
    calculos.push({ id: "ocup_ano", rotulo: "Ocupação média do ano", valor: ocupAno === null ? null : ocupAno * 100, texto: t, alerta, detalhes: { meses_medios: mM } });
  }

  // 5. erro_mes_cheio
  const erro = ocupAno !== null && oA !== null ? div(oA, ocupAno) : null;
  calculos.push({
    id: "erro_mes_cheio", rotulo: "Quanto a conta sairia maior usando o mês mais cheio", valor: erro === null ? null : (erro - 1) * 100,
    texto: erro === null ? "Falta a ocupação da alta ou a média do ano." : `Quem usa a ocupação da alta no lugar da média do ano faz uma conta ${fmtPct(erro - 1)} maior do que o ano entrega.`,
    alerta: erro !== null && erro - 1 > 0 ? "atencao" : undefined,
  });

  // 6. receita_bruta_unidade
  const rbu = ocupAno !== null && diariaMedia !== null ? ocupAno * 365 * diariaMedia : null;
  calculos.push({
    id: "receita_bruta_unidade", rotulo: "Receita bruta por unidade no ano (não é retorno)", valor: rbu,
    texto: rbu === null ? "Falta a ocupação do ano ou a diária média." : `Receita bruta por unidade no ano: ${brl(rbu)} (${fmtN((ocupAno as number) * 365, 1)} noites a ${brl(diariaMedia as number)}). Não é retorno: ainda saem impostos, comissões, custos e a retirada do dono.`,
  });

  // 7. mes_fraco_unidade
  const mfu = oFr !== null && diariaMedia !== null ? 30 * oFr * diariaMedia : null;
  calculos.push({
    id: "mes_fraco_unidade", rotulo: "Quanto entra num mês fraco, por unidade", valor: mfu,
    texto: mfu === null ? "Falta a ocupação dos meses fracos ou a diária média." : `Num mês fraco entra cerca de ${brl(mfu)} por unidade, antes de qualquer custo.`,
  });

  // 8. absorcao
  // Atenção: o JSON escreve "sobra = noites_hoje + mais - menos". A conta conferida da auditoria
  // (Passo 8) é "sobra = mais - menos": as noites de hoje já são vendidas pelos comparáveis.
  // Somar noites_hoje faria caber dezenas de unidades. Ver ts/README.md, item A3.
  const comp = num(r, "unidades_comparaveis");
  const crescNS = falta(r["crescimento_ate_abrir"]);
  const obraNS = falta(r["unidades_em_obra"]);
  const cresc = pct(r, "crescimento_ate_abrir") ?? 0;
  const emObra = num(r, "unidades_em_obra") ?? 0;
  let cabem: number | null = null;
  {
    if (comp === null || ocupAno === null || ocupAno <= 0) {
      calculos.push({ id: "absorcao", rotulo: "Quantas unidades o mercado aguenta agora", valor: null, texto: `Para a absorção falta ${comp === null ? "quantas unidades somam os comparáveis" : "a ocupação média do ano"}.` });
    } else {
      const noitesHoje = comp * 365 * ocupAno;
      const mais = noitesHoje * cresc;
      const menos = emObra * 365 * ocupAno;
      const sobra = mais - menos;
      const porUnidade = 365 * ocupAno;
      cabem = Math.max(0, pisoSeguro(sobra / porUnidade));
      const marcas = [crescNS && "sem a série (crescimento entrou como zero)", obraNS && "sem os alvarás (unidades em obra entraram como zero)"].filter(Boolean) as string[];
      calculos.push({
        id: "absorcao", rotulo: "Quantas unidades o mercado aguenta agora", valor: cabem,
        texto: `Os comparáveis vendem ${fmtN(noitesHoje, 0)} noites hoje. Até você abrir, a procura cresce ${fmtN(mais, 0)} noites e as unidades em obra levam ${fmtN(menos, 0)}. Sobram ${fmtN(sobra, 0)} noites para quem entra; cada unidade precisa de ${fmtN(porUnidade, 1)}. Cabem ${cabem} agora.` + (marcas.length ? ` Conta ${juntar(marcas)}.` : ""),
        alerta: cabem < 1 ? "critico" : undefined,
        detalhes: { noites_hoje: noitesHoje, mais, menos, sobra, noites_por_unidade: porUnidade, cabem_agora: cabem, sem_serie: crescNS, sem_alvaras: obraNS },
      });
    }
  }

  // 9. checa_regua
  const alerta65 = ocupAno === null ? null : ocupAno >= 0.65 - 1e-12;
  calculos.push({
    id: "checa_regua", rotulo: "Prova exigida acima de 65%", valor: alerta65,
    texto: alerta65 === null ? "Sem a média do ano, não dá para checar a régua." : alerta65 ? `Alerta: ${fmtPct(ocupAno as number)} no ano exige prova de procura extraordinária.` : "Abaixo de 65%: não exige prova de procura extraordinária.",
    alerta: alerta65 ? "critico" : alerta65 === false ? "ok" : undefined,
  });

  // 10. veredito_sugerido
  const pretendidas = num(r, "unidades_pretendidas");
  let v: Veredito, motivo: string;
  // Pausar só com a absorção medida: com a série ou os alvarás em Não sei (entram como zero),
  // a sobra sai incompleta e o caso cai em "testar" (ver ts/README.md, item A3).
  if (cabem !== null && cabem < 1 && !crescNS && !obraNS) {
    v = "pausar"; motivo = "A sobra do destino não cabe nem uma unidade: não existe procura para o que se quer fazer ali.";
  } else if (cabem === null || ocupAno === null || (alerta65 as boolean) || crescNS || obraNS) {
    v = "testar";
    const m: string[] = [];
    if (cabem === null || ocupAno === null) m.push("falta dado para a média do ano ou a absorção");
    if (alerta65) m.push("a ocupação do ano passou de 65% sem prova de procura extraordinária");
    if (crescNS) m.push("falta a série de visitantes");
    if (obraNS) m.push("faltam os alvarás");
    motivo = `Testar: ${juntar(m)}.`;
  } else if (pretendidas === null) {
    v = "testar"; motivo = "Testar: falta quantas unidades você pensava em abrir para comparar com o que cabe.";
  } else if (cabem < pretendidas) {
    v = "ajustar"; motivo = `Cabem ${cabem} agora, menos que as ${fmtN(pretendidas)} pretendidas: desenha a infraestrutura para o total e abre com as que cabem.`;
  } else {
    v = "avancar"; motivo = "Seguir com condições: o mercado aguenta as unidades pretendidas, desde que se entregue o que o topo da faixa entrega.";
  }
  calculos.push({ id: "veredito_sugerido", rotulo: "Veredito sugerido pela página", valor: v, texto: motivo });

  return { calculos: calculos.map((c) => fechar(c)), veredito_sugerido: v, motivo_veredito: motivo };
}
