import sys

with open('site/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'function filterPageCards() {',
    'window.applyCurrentFilters = filterPageCards;\n  function filterPageCards() {'
)

content = content.replace(
    'initExpandableCards();\n  }\n}',
    'initExpandableCards();\n    if (window.applyCurrentFilters) window.applyCurrentFilters();\n  }\n}'
)

with open('site/js/app.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
