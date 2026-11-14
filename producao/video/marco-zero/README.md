# Marco Zero em 14 vídeos

Série curta (até 3:50 cada) feita a partir da aula de 60 minutos, conduzindo até a Trilha 1.

```bash
pdftoppm -png -r 150 -scale-to-x 1920 -scale-to-y 1080 marco-zero.pdf slides/p   # 49 páginas
python3 mz.py narrar --videos 1-12      # voz Kokoro pm_alex (modelo em ../d01-territorio/modelos/)
python3 mz.py montar --videos 1-12      # saida/videos, saida/verticais, saida/legendas, saida/relatorio.txt
```

- `roteiro.md`: o texto falado, página por página, agrupado nos 14 vídeos. Não altere sem o Bruno.
- Vídeos 13 e 14 esperam a versão para vídeo das páginas 41, 42, 44, 45 e 46 (ainda mostram a oferta ao vivo).
