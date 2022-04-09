from pathlib import Path
from bs4 import BeautifulSoup
from typing import Final

import re
import unicodedata
import svgwrite


SOURCE: Final[Path] = Path('noto-emoji/svg')
CACHE: Final[Path] = Path('cache')
FINAL: Final[Path] = Path('final')

STYLE: Final[str] = 'fill:#ffffff;stroke:#e4e4e4;stroke-width:0.5pt;vector-effect:non-scaling-stroke;stroke-miterlimit:4;stroke-dasharray:none;-inkscape-stroke:hairline;'


def slurp(name: str) -> Path:
    sym = unicodedata.lookup(name)
    code = '_'.join(f'{ord(c):x}' for c in sym)

    orig = SOURCE / f'emoji_u{code}.svg'
    assert orig.exists(), orig

    with orig.open() as f:
        soup = BeautifulSoup(f, 'xml')

    for elem in soup.find_all(style=True):
        elem['style'] = re.sub('fill:.+;', STYLE, elem['style'])

    for elem in soup.find_all(fill=True) + soup.find_all(stroke=True):
        del elem['fill']
        del elem['stroke']
        elem['style'] = STYLE

    outline = CACHE / f'{sym}.svg'
    with outline.open('wb') as f:
        f.write(soup.prettify('utf-8'))

    return (sym, outline.resolve())


if __name__ == '__main__':
    CACHE.mkdir(exist_ok=True)
    FINAL.mkdir(exist_ok=True)

    # Read triples to generate
    with open('data', 'r') as f:
        while line := f.readline():
            line = line.strip()
            line = line.split('|')

            (s1, p1) = slurp(line[0])
            (s2, p2) = slurp(line[1])
            (s3, p3) = slurp(line[2])

            final = FINAL / f'{s1}{s2}{s3}.svg'
            print(final)

            dwg = svgwrite.Drawing(final, size=('210mm', '148mm'), profile='tiny')
            dwg.add(dwg.image(p1.as_uri(), ('10mm', '44mm'), ('60mm', '60mm')))
            dwg.add(dwg.image(p2.as_uri(), ('75mm', '44mm'), ('60mm', '60mm')))
            dwg.add(dwg.image(p3.as_uri(), ('140mm', '44mm'), ('60mm', '60mm')))

            dwg.save(pretty=True)


