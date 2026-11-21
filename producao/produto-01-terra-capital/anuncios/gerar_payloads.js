// Gera meta_payloads.json (parâmetros prontos para o Windsor/Meta, tudo PAUSADO) e COPIES.md. Uso: node anuncios/gerar_payloads.js
const fs = require('fs'), path = require('path'); const A = __dirname; const J = JSON.parse(fs.readFileSync(A + '/anuncios.json', 'utf8'));
const tags = (slug) => `utm_source=meta&utm_medium=paid&utm_campaign=p01_terra_capital&utm_content=${slug}&utm_id={{campaign.id}}&utm_term={{adset.name}}`;
const centavos = (r) => Math.round(r * 100);
const orc = J.campanha.orcamentoDiarioReais, d = J.campanha.divisao;
const base = { optimization_goal: 'OFFSITE_CONVERSIONS', billing_event: 'IMPRESSIONS', promoted_object: { pixel_id: '<PIXEL_ID_CONFIRMADO_POR_BRUNO>', custom_event_type: 'PURCHASE' }, status: 'paused', extra_params: { attribution_spec: [{ event_type: 'CLICK_THROUGH', window_days: 7 }, { event_type: 'VIEW_THROUGH', window_days: 1 }] } };
const excl = [{ id: '<AUDIENCIA_COMPRADORES_P01>', name: 'Compradores do Produto 01 (criar após a 1ª venda)' }];
const geo = { countries: ['BR'], location_types: ['home', 'recent'] };
const payloads = {
  aviso: 'Nada foi executado. Todos os itens nascem com status paused. Substitua os marcadores <...> antes de rodar; o orçamento exige "aprovado" de Bruno.',
  campanha: { action: 'create_campaign', account: '1271873041294684', params: { name: J.campanha.nome, objective: J.campanha.objetivo, special_ad_categories: [], status: 'paused', daily_budget: centavos(orc), bid_strategy: 'LOWEST_COST_WITHOUT_CAP' } },
  conjuntos: [
    { chave: 'aberto', params: { ...base, name: 'ABERTO · Advantage+ · Brasil 25-65', campaign_id: '<ID_CAMPANHA>', advantage_audience: true, targeting: { geo_locations: geo, age_range: [25, 55], excluded_custom_audiences: excl }, daily_budget: centavos(orc * d.aberto / 100) } },
    { chave: 'lookalike', params: { ...base, name: 'LOOKALIKE 1% · leads qualificados', campaign_id: '<ID_CAMPANHA>', targeting: { geo_locations: geo, age_min: 25, age_max: 65, custom_audiences: [{ id: '<LOOKALIKE_1PCT_LEADS_QUALIFICADOS>' }], excluded_custom_audiences: excl }, daily_budget: centavos(orc * d.lookalike / 100) } },
    { chave: 'remarketing', params: { ...base, name: 'REMARKETING · base existente (LGPD)', campaign_id: '<ID_CAMPANHA>', targeting: { geo_locations: geo, age_min: 25, age_max: 65, custom_audiences: J.publicos.remarketing_existentes.map(x => ({ id: x.id })), excluded_custom_audiences: excl }, daily_budget: centavos(orc * d.remarketing / 100) } },
  ],
  anuncios: [...J.ads.map(a => ({ n: a.n, params: { name: `AD${String(a.n).padStart(2, '0')} · ${a.slug}`, adset_id: '<ID_CONJUNTO>', page_id: J.pageId, link: J.pagina.A47, image_url: `${J.hospedagem}feed/${a.arquivo}_1080x1350.jpg`, message: a.texto, headline: a.titulo, description: a.descricao, call_to_action_type: 'LEARN_MORE', status: 'paused' }, url_tags: tags(a.slug), stories: `${J.hospedagem}stories/${a.arquivo}_1080x1920.jpg` })),
    { n: 7, tipo: 'video', params: { name: `AD07 · ${J.video.slug}`, adset_id: '<ID_CONJUNTO>', page_id: J.pageId, video_id: '<VIDEO_ID_APOS_create_ad_video>', image_url: `${J.hospedagem}feed/anuncio_04_neutro_1080x1350.jpg`, link: J.pagina.A47, message: J.video.texto, headline: J.video.titulo, description: J.video.descricao, call_to_action_type: 'LEARN_MORE', status: 'paused' }, url_tags: tags(J.video.slug), video_url: `${J.hospedagem}video/${J.video.arquivo}` }],
  teste_de_preco: { quando: 'Fase 2, depois de escolher criativo e público', como: 'A/B test do Meta (Experimentos) com dois conjuntos iguais, um para a página A (R$ 47) e outro para a página B (R$ 67); url_tags igual + price_version via parâmetro da página', paginas: J.pagina },
};
fs.writeFileSync(A + '/meta_payloads.json', JSON.stringify(payloads, null, 1));
let md = '# Copies dos anúncios · Produto 01\n\nUm criativo = um anúncio. Botão "Saiba mais" (LEARN_MORE). Destino: landing do Produto 01 com checkout direto (sem formulário). Tudo em rascunho/pausado.\n\n| # | Criativo | Texto principal | Título | Descrição | UTM (url_tags) |\n|---|---|---|---|---|---|\n';
for (const a of payloads.anuncios) md += `| ${a.n} | ${a.params.name} | ${a.params.message} | ${a.params.headline} | ${a.params.description} | \`${a.url_tags}\` |\n`;
fs.writeFileSync(A + '/COPIES.md', md); console.log('ok', payloads.anuncios.length, 'anúncios');
