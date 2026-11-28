// Classificação comercial preliminar do Zion Investors (ClickMax). Funciona com respostas parciais:
// sem capital/disponibilidade (perguntas 5 e 6 movidas para a qualificação privada) só chega a PENDENTE/C/D/T/BUBBLE;
// A+/A/B saem quando a qualificação privada preencher capital e disponibilidade (atualização posterior).
// A classificação é interna e preliminar; não é qualificação regulatória de investidor e nunca é exibida ao lead.
const CAP_ALTO=['1m_3m','3m_mais'], CAP_A=['450_750','750_1m'], CAP_B=['150_300','300_450'];
const PRAZO_90=['imediato','30d','30_90d'], PRAZO_LONGO=['3_6m','6_12m'];
const DISP_DEPENDE=['reorganizar','venda_ativo','socios','financiamento'];
const REUNIAO_SIM=['decide_reuniao','com_socios','com_familia','empresa_grupo'];
function classificar(r){
  const intencaoInvest = ['investir_capital','diversificar'].includes(r.interesse_principal)
    || ['sim_investir','sim_entender'].includes(r.compreensao);
  // 1) comprador de estrutura (exclusivo)
  if(r.interesse_principal==='comprar_bubble' && !['sim_investir','sim_entender'].includes(r.compreensao)) return 'BUBBLE';
  if(r.compreensao==='nao_bubble' && !intencaoInvest) return 'BUBBLE';
  // 2) proprietário de terreno que busca exclusivamente investidor
  if(r.interesse_principal==='terreno_parceiro' || (r.terreno==='sim_procura_investidor' && r.interesse_principal!=='investir_capital' && r.interesse_principal!=='diversificar')) return 'T';
  const cap=r.capital, disp=r.disponibilidade;
  const semDados = (!cap||cap==='reuniao') && (!disp||disp==='reuniao');
  // 3) faixas por capital + disponibilidade (A+, A, B)
  if(intencaoInvest && disp==='possuo'){
    if(CAP_ALTO.includes(cap) && PRAZO_90.includes(r.prazo)) return 'A+';
    if(CAP_ALTO.includes(cap)||CAP_A.includes(cap)) return 'A';
  }
  if(intencaoInvest && CAP_B.includes(cap) && REUNIAO_SIM.includes(r.decisao) && !DISP_DEPENDE.includes(disp)) return 'B';
  // 4) maturação: quer investir, mas depende de algo, prazo longo ou capital menor (nunca exclui)
  if(intencaoInvest && (DISP_DEPENDE.includes(disp)||PRAZO_LONGO.includes(r.prazo)||['ate150','sem_capital'].includes(cap)||disp==='nao_possuo'||CAP_ALTO.concat(CAP_A,CAP_B).includes(cap))) return 'C';
  // 5) apenas pesquisando, sem previsão e sem querer avançar
  if(r.prazo==='pesquisando' && (r.interesse_principal==='conhecer'||!intencaoInvest) && r.decisao==='sem_reuniao') return 'D';
  // 6) quer investir mas ainda não informou capacidade (ou prefere falar em reunião): não é curioso
  if(intencaoInvest || semDados) return 'PENDENTE';
  return 'PENDENTE';
}
const TAGS={'A+':'ZI_A_PLUS_ESTRATEGICO','A':'ZI_A_QUALIFICADO','B':'ZI_B_POTENCIAL','C':'ZI_C_MATURACAO','D':'ZI_D_INSTITUCIONAL','T':'ZI_T_TERRENO','BUBBLE':'ZI_BUBBLE','PENDENTE':'ZI_PENDENTE'};
module.exports={classificar,TAGS};
