## 1
# import sys
# s = sys.stdin.readline().lower()
# w, d = (s.split())
# print(d)
# print(w.count(d))

# # 2
# import sys
# r = sys.stdin.readline()
# l = r.split()[-1]
# print(l)
# print(len(l))

# # 3
# n = input()
# arr = []
# for i in range(int(n)):
#     arr.append(int(input()))
# print(arr)
# arr.sort()
# print(arr)
#
# for i in sorted(set(arr)):
#     print(i)

# # 4
# a = input()
# b = input()
#
# an = len(a) % 8
# if an != 0:
#     a += '0'*(8-an)
# bn = len(b) % 8
# if bn != 0:
#     b += '0'*(8-bn)
#
# i = 0
# while True:
#     if 8*(i)>=len(a):
#         break
#     print(a[8*i:8*(i+1)])
#     i += 1
# j = 0
# while True:
#     if 8*(j)>=len(b):
#         break
#     print(b[8*j:8*(j+1)])
#     j += 1

# # 5
# a = input()
# a = a[2:]
# sum = 0
# p = 0
# for i in a[::-1]:
#     if not i.isdigit():
#         if i == 'A':
#             i = 10
#         elif i == 'B':
#             i = 11
#         elif i == 'C':
#             i = 12
#         elif i == 'D':
#             i = 13
#         elif i == 'E':
#             i = 14
#         elif i == 'F':
#             i = 15
#     sum += 16 ** p * int(i)
#     p += 1
# print(sum)

# 6   180 2 2 3 3 5
# a = int(input())
#
# def prime():
#     yield 2
#     p = 3
#     while True:
#         flag = True
#         import math
#         for i in range(2, int(math.sqrt(p))):
#             if p % i == 0:
#                 flag = False
#                 break
#         if flag:
#             yield p
#         p += 1
#
# p = prime()
# x = next(p)
# while a > 1:
#     if a % x == 0:
#         print(x)
#         a = a / x
#     else:
#         x = next(p)
# a = int(input())
# res = ''
# i = 2
# while a != 1:
#     while a%i == 0:
#         a = a / i
#         res += str(i) + ' '
#     i += 1
# print(res)

# # 7
# a = float(input())
# if (a - int(a)) > 0.5:
#     print(int(a) + 1)
# else:
#     print(int(a))

# # 8
# n = int(input())
# d = {}
# for i in range(n):
#     a = input().split()
#     if a[0] in d.keys():
#         d[a[0]] = d[a[0]] + a[1]
#     else:
#         d[a[0]] = a[1]
# 
# p = sorted(d, key=lambda k:int(k))
# print(p)
# for k in p:
#     print(k, d[k])


# # 15
# import sys
# try:
#     a, b, c, d, e, err, ps = 0, 0, 0, 0, 0 ,0, 0
#     while True:
#         line = sys.stdin.readline().strip()
#         if line == '':
#             break
#         lines = line.split('~')
#         ip, mask =  lines[0], lines[1]
#         l = ip.split('.')
#         br = False
#         for i in l:
#             if not i or int(i)>=256:
#                 err += 1
#                 br = True
#                 break
#         if br:
#             continue
#         m = mask.split('.')
#         xs = ['254','252','248','240','224','192','128','0']
#         if m[0] == '255':
#             if m[1] == '255':
#                 if m[2] == '255':
#                     if m[3] not in xs:
#                         err += 1
#                         continue
#                 else: 
#                     if m[2] not in xs or m[3] != '0':
#                         err += 1
#                         continue 
#             else:
#                 if m[1] not in xs or m[2] != '0' or m[3] != '0':
#                     err += 1
#                     continue 
#         else:
#             if m[0] not in xs or m[1] != '0' or m[2] != '0' or m[3] != '0':
#                 err += 1
#                 continue 
#         flag = int(l[0])
#         if flag >=1 and flag <= 126:
#             a += 1
#             if flag == 10:
#                 ps += 1
#         elif flag >=128 and flag <= 191:
#             b += 1
#             if flag == 172:
#                 if int(l[1]) >= 16 and int(l[1]) <= 31:
#                     ps += 1
#         elif flag >=192 and flag <= 223:
#             c += 1
#             if flag == 192:
#                 if int(l[1]) == 168:
#                     ps += 1
#         elif flag >=224 and flag <= 239:
#             d += 1
#         elif flag >=240 and flag <= 255:
#             e += 1
#     print(a, b, c, d, e, err, ps)
# except:
#     pass


# 16
# import sys
# out = []
# while True:
#     try:
#         line = sys.stdin.readline().strip()
#         if line == '':
#             break
#         fi, num = line.split()
#         name = fi.split('\\')[-1]
#         if len(name) > 16:
#             name = name[-16:]
#         if out:
#             f = True
#             for i in out:
#                 if name == i[0] and num == i[1]:
#                     i[2] += 1
#                     f = False
#                     break
#             if f:
#                 s = [name, num, 1]
#                 out.append(s)
#         else:
#             s = [name, num, 1]
#             out.append(s)
#     except:
#         pass
# for i in out[-8:]:
#     print(i[0] + ' '+ str(i[1]) + ' '+ str(i[2]))

# 17
# import sys
# while True:
#     try:
#         line = sys.stdin.readline().strip()
#         if not line:
#             break
#         kind, sub = [0, 0, 0, 0], False
#         l = len(line)
#         if l <= 8:
#             print('NG')
#             continue
#         for i in range(l):
#             if line[i].isdigit():
#                 kind[0] = 1
#             elif line[i].islower():
#                 kind[1] = 1
#             elif line[i].isupper():
#                 kind[2] = 1
#             else:
#                 kind[3] = 1
#             if i >= 3:
#                 if line[i+1:].find(line[i-3:i]) > 0:
#                     sub = True
#                     break
#         if kind.count(1) >= 3 and sub == False:
#             print('OK')
#         else:
#             print('NG')
#     except:
#         raise

# # 18
# import sys
# while True:
#     try:
#         line = sys.stdin.readline().strip()
#         if not line:
#             break
#         ch = ['0', '1', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
#         new_password = ''
#         for i in range(len(line)):
#             if line[i].isupper():
#                 p = ord(line[i]) + 32 + 1
#                 if p == 123:
#                     p = 97
#                 new_password += chr(p)
#             elif line[i].islower():
#                 for j in range(len(ch)):
#                     if line[i] in ch[j]:
#                         new_password += str(j)
#                         break
#             else:
#                 new_password += line[i]
#         print(new_password)
#     except:
#         raise

# # 19
# import sys
# b = []
# while True:
#     try:
#         m = 3
#         n = int(input())
#         if n == 0:
#             break
#         sum = 0
#         while True:
#             p = n // m
#             q = n % m
#             sum += p
#             n = p + q
#             if n == 2:
#                 n = 3
#             elif n == 1:
#                 break
#         b.append(sum)
#     except:
#         pass
# for i in b:
#     print(i)

# # 20
# from collections import Counter
# while True:
#     try:
#         n = input()
#         if not n:
#             break
#         d = Counter(n).most_common()
#         p, q = d[-1]
#         n = n.replace(p, '')
#         for k, v in d:
#             if v == q:
#                 n = n.replace(k, '')
#             else:
#                 break
#         print(n)
#     except:
#         pass

# # 21 
# while True:
#     try:
#         n = int(input())
#         a = [int(i) for i in input().strip().split()]
#         l, m = [0] * n, [0] * n
        
#         l[0] = 1
#         for i in range(1, n):
#             l[i] = 1
#             for j in range(i):
#                 # 如果大于前面的数字, 只需要查看该值的最长子序列
#                 # 如果大于当前当前就将当前值的设置为前序加一
#                 if a[i] > a[j] and l[j] + 1 > l[i]:
#                     l[i] = l[j] + 1
        
#         m[n-1] = 1
#         for i in range(n-2, -1, -1):
#             m[i] = 1
#             for j in range(n-1, i, -1):
#                 if a[i] > a[j] and m[j] + 1 > m[i]:
#                     m[i] = m[j] + 1
        
#         ans = 0
#         for i in range(n):
#             if (l[i] + m[i] - 1 > ans):
#                 ans = l[i] + m[i] - 1
#         print(n - ans)
#     except:
#         break


from collections import namedtuple
while True:
    try:
        n = int(input())
        a = [int(i) for i in input().strip().split()]
        l, m = [0 for i in range(n)], [0 for i in range(n)]
        l[0], m[n-1] = 1, 1
        for i in range(1, n):
            l[i], m[n-1-i] = 1, 1
            for j in range(i):
                # 如果大于前面的数字, 只需要查看该值的最长子序列
                # 如果大于当前当前就将当前值的设置为前序加一
                if a[i] > a[j] and l[j] + 1 > l[i]:
                    l[i] = l[j] + 1
                if a[n-1-i] > a[n-1-j] and m[n-1-i] + 1 > m[n-1-j]:
                    m[n-1-i] = m[n-1-j] + 1
        ans = 0
        for i in range(n):
            if (l[i] + m[i] - 1 > ans):
                ans = l[i] + m[i] - 1
        print(n - ans)
    except:
        break
