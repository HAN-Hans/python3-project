# 1
from collections import Counter
while True:
    try:
        a, b = input().strip(), 'true'
        if a.endswith(' true'):
            b = 'true'
            a = a[:-5]
        elif a.endswith(' false'):
            b = 'false'
            a = a[:-6]
        # if len(a) == 2:
        #     if a[1] == 'false':
        #         b = 'false'
        r = []
        if b == 'true':
            r = Counter(a).most_common()
        else:
            r = Counter(a.lower()).most_common()
        c, d = r[0]
        m = d
        l = [c]
        for i in r:
            if i[1] == m:
                l.append(i[0])
        # if b == 'false':
        #     c = a[0][a[0].lower().index(c)]
        t = min(l)
        res = t + ' ' + str(d)
        print(res)
    except:
        raise

