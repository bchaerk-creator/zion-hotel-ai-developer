/* Zion · persistência de origem (primeiro toque) · PROPOSTA, NÃO INSTALADA.
 * Para colar em ClickMax > página > Configurações da Página > Scripts (código personalizado), SÓ com "aprovado" de Bruno.
 * Faz: guarda UTMs, src, sck, ids do anúncio e fbclid na primeira visita (30 dias) e, quando o visitante volta por um
 * link SEM esses parâmetros (ex.: mensagem de WhatsApp), devolve à URL só o que falta, antes do checkout ler a URL.
 * Não sobrescreve parâmetro que já veio na URL (a origem do canal continua sendo a do link atual).
 * Limites: só funciona no MESMO navegador (localStorage); não cruza aparelhos; não cria dado que nunca existiu.
 * Sem dependências, sem rede, sem dados pessoais. */
(function () {
  try {
    var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'src', 'sck', 'ad_id', 'campaign_id', 'adset_id', 'fbclid'];
    var STORE = 'zion_first_touch_v1';
    var TTL = 30 * 24 * 3600 * 1000;
    var now = Date.now();
    var cur = new URLSearchParams(location.search);
    var saved = null;
    try { saved = JSON.parse(localStorage.getItem(STORE) || 'null'); } catch (e) { saved = null; }
    if (saved && now - saved.t > TTL) saved = null;
    var incoming = {};
    var any = false;
    KEYS.forEach(function (k) { var v = cur.get(k); if (v) { incoming[k] = v; any = true; } });
    if (any && !saved) {
      saved = { t: now, p: incoming };
      try { localStorage.setItem(STORE, JSON.stringify(saved)); } catch (e) { /* sem storage: segue sem persistir */ }
    }
    if (saved && saved.p) {
      var changed = false;
      KEYS.forEach(function (k) {
        if (!cur.get(k) && saved.p[k]) { cur.set(k, saved.p[k]); changed = true; }
      });
      if (changed) history.replaceState(null, '', location.pathname + '?' + cur.toString() + location.hash);
    }
  } catch (e) { /* nunca quebrar a página */ }
})();
