#!/usr/bin/env python3
"""Modelo financeiro Fase 1 Brasil (MRF 200 t/d) — Zion Ecosystem.
Premissas conservadoras nacionalizadas; ver docs/analise-viabilidade-projecao.md."""
import numpy_financial as npf

CAPEX=4.5; t_ano=73.0; gate=130.0; mat_full=4.0; ccrlr_t=25.0
ramp=[0.70]+[1.0]*9; aprov=[0.20,0.40,0.60]+[0.80]*7
opex_fix=7.2; infl=0.04; frac_rec=0.19
fcf=[-CAPEX]
for i in range(10):
    f=(1+infl)**i; vol=t_ano*ramp[i]
    rec=vol*1000*gate/1e6*f + mat_full*(aprov[i]/0.80)*f + vol*1000*frac_rec*aprov[i]*ccrlr_t/1e6*f
    opex=opex_fix*(0.85 if i==0 else 1)*f
    ebitda=rec-opex; ebit=ebitda-CAPEX/10
    fcf.append(ebitda-max(0,ebit)*0.34-rec*0.02)
print('TIR:', f'{npf.irr(fcf):.1%}', '| VPL@14%:', f'R${npf.npv(0.14,fcf):.1f}M')
