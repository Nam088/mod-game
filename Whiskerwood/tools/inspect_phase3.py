import json

data = json.load(open('scratch_p3.json', encoding='utf-8'))

for p in ['crop', 'policy', 'unlock', 'resource']:
    items = [x for x in data if x['key'].startswith(p)]
    print(f"\n{'='*20} {p.upper()} ({len(items)}) {'='*20}")
    for x in items:
        print(f"  {repr(x['key'])}: {repr(x['en'])},")

