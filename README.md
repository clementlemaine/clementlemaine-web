# Portfolio — Clément Lemaine

Site FR / EN / ES + CV PDF, généré par `build.py` (même base que le portfolio de César Mateu).

- Contenu : `content.py`
- Rebuild complet (site + PDF) : `python3 build.py` (nécessite Google Chrome)
- Site seul : `python3 build.py --no-cv`
- Dépendance : `pip3 install --user segno` (QR code vers `SITE_URL`, généré dans `assets/qr.svg` et `assets/qr.png`)
- En ligne : https://clementlemaine.github.io/ (GitHub Pages, branche `main`)
