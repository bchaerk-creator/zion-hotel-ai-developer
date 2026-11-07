import json, sys
# uso: fix_auto.py spec.json N  -> a última ação "auto" passa a ter N telas
p, n = sys.argv[1], int(sys.argv[2])
d = json.load(open(p))
last = None
for sc in d['scenes']:
    for a in sc['actions']:
        if 'auto' in a:
            last = a
last['auto'] = n
json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
print("ok", p, "último auto =", n)
