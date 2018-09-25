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

# p = sorted(d, key=lambda k:int(k))
# print(p)
# for k in p:
#     print(k, d[k])

# # 9
# a, s = input(), []
# print(a, a[::-1])
# [s.append(i) for i in a[::-1] if i not in s]
# print(''.join(s))

# # 10
# def number_of_ascii(s):
#     sum = 0
#     for i in range(s):
#         if ord(i) <= 127:
#             sum += 1
#     return sum

# # 11
# a = int(input())
# b = 0
# while a:
#     if a % 2 == 1:
#         b += 1
#     a = a // 2
# print(b)

# # 12  A10;S20;W10;D30;X;A1A;B10A11;;A10;
# import re
# a = input()
# point = [0, 0]
# for b in a.split(';'):
#     if len(b) != 3:
#         continue
#     p = re.match('^[ADSW][\d]{2}$', b)
#     if p:
#         if b[:1] == ('A'):
#             point[0] -= int(b[1:])
#         elif b[:1] == ('D'):
#             point[0] += int(b[1:])
#         elif b[:1] == ('W'):
#             point[1] += int(b[1:])
#         elif b[:1] == ('S'):
#             point[1] -= int(b[1:])
# print(str(point[0])+','+str(point[1]))

# 20
# while True:
#     try:
#         a = int(input())
#         b = map(int, input().split()[:8])
#         for i in range(a):
#             n, m = 0, 0
#             for j in range(i):
#                 if b[j] < b[i]:
#                     n += 1
#             for j in range(a - i):
#                 if b[j] > b[i]:
#                     m += 1
#     except:
#         pass


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


# from collections import namedtuple
# while True:
#     try:
#         n = int(input())
#         a = [int(i) for i in input().strip().split()]
#         l, m = [0 for i in range(n)], [0 for i in range(n)]
#         l[0], m[n-1] = 1, 1
#         for i in range(1, n):
#             l[i], m[n-1-i] = 1, 1
#             for j in range(i):
#                 # 如果大于前面的数字, 只需要查看该值的最长子序列
#                 # 如果大于当前当前就将当前值的设置为前序加一
#                 if a[i] > a[j] and l[j] + 1 > l[i]:
#                     l[i] = l[j] + 1
#                 if a[n-1-i] > a[n-1-j] and m[n-1-i] + 1 > m[n-1-j]:
#                     m[n-1-i] = m[n-1-j] + 1
#         ans = 0
#         for i in range(n):
#             if (l[i] + m[i] - 1 > ans):
#                 ans = l[i] + m[i] - 1
#         print(n - ans)
#     except:
#         break


# # 22
# while True:
#     try:
#         a = list(map(int, input().split()))
#         n, p = a[0], a[1:]
#         b = list(map(int, input().split()))
#         m, q = b[0], sorted(set(b[1:]))
#         r, s = [], []
#         for i in range(len(q)):
#             res = []
#             for j in range(n):
#                 if str(q[i]) in str(p[j]):
#                     res.extend([j, p[j]])
#                     if q[i] not in s:
#                         s.append(q[i])
#             if res:
#                 r.append(res)
#         l = 0
#         p = [0]
#         for i in range(len(r)):
#             p.append(s[i])
#             p.append(len(r[i])//2)
#             p.extend(r[i])
#         p[0] = len(p) - 1
#         print(' '.join(map(str, p)))
#     except:
#         break


# # 23
# while True:
#     try:
#         s = input()
#         p, q = [], []
#         for i in range(len(s)):
#             if not s[i].isalpha():
#                 p.append(s[i])
#             else:
#                 p.append("")
#                 q.append(s[i])
#         q.sort(key=lambda s: ord(s.lower()))
#         s = 0
#         for i in range(len(p)):
#             if p[i] == "":
#                 p[i] = q[s]
#                 s += 1
#         print(''.join(p))
#     except:
#         break

# # 24
# from collections import Counter
# while True:
#     try:
#         n, *s, a, b = input().split()
#         l = []
#         for i in range(int(n)):
#             if s[i] != a and Counter(s[i]) == Counter(a):
#                 l.append(s[i])
#         print(len(l))
#         if l and b <= len(l):
#             print(sorted(l)[int(b)-1])
#     except:
#         raise

# # 25
# import math
# def is_prime(a):
#     if a == 1:
#         return False
#     if a == 2:
#         return True
#     for i in range(2, int(math.sqrt(a))):
#         if a % i:
#             print(a)
#             return True
#     return False

# while True:
#     try:
#         n, s = int(input()), input().split()
#         l = 0
#         for i in range(n-1):
#             for j in range(i+1, n):
#                 if is_prime(int(s[i]) + int(s[j])):
#                     l += 1
#         print(l)
#     except:
#         raise

# # 26
# def encrypt(a):
#     b = ''
#     for i in range(len(a)):
#         if a[i].isalpha():
#             p = ord(a[i]) + 33
#             if p < 123:
#                 b += chr(p)
#             elif p == 123:
#                 b += 'a'
#             elif p == 155:
#                 b += 'A'
#             else:
#                 b += chr(p - 64)
#         elif a[i].isdigit():
#             if int(a[i]) < 9:
#                 b += str(int(a[i]) + 1)
#             else:
#                 b += '0'
#         else:
#             b += a[i]
#     return b
#
# def unencrypt(a):
#     b = ''
#     for i in range(len(a)):
#         if a[i].isalpha():
#             p = ord(a[i]) - 33
#             if p > 64:
#                 b += chr(p)
#             elif p == 64:
#                 b += 'Z'
#             elif p == 32:
#                 b += 'z'
#             else:
#                 b += chr(p + 64)
#         elif a[i].isdigit():
#             if int(a[i]) == 0:
#                 b += '9'
#             else:
#                 b += str(int(a[i]) - 1)
#         else:
#             b += a[i]
#     return b
#
# while True:
#     try:
#         a, b = input(), input()
#         print(encrypt(a))
#         print(unencrypt(b))
#     except:
#         raise

# # 27
# while True:
#     try:
#         a = input().replace(' ', '')
#         m, n = ''.join(sorted(a[::2])), ''.join(sorted(a[1::2]))
#         r, b = '', ''
#         for i in range(len(n)):
#             r += m[i] + n[i]
#         if len(m) > len(n):
#             r += m[len(n):]
#         for i in r:
#             if i in '0123456789ABCDEFabcdef':
#                 # 注意在转成二进制要不补齐到四位
#                 s = hex(int(bin(int(i, base=16))[2:].rjust(4, "0")[::-1], base=2))[2:]
#                 if s.isalpha():
#                     s = s.upper()
#                 b += s
#             else:
#                 b += i
#         print(b)
#     except:
#         raise

# # 28
# while True:
#     try:
#         a = input()
#         l = []
#         s = ''
#         for i in a:
#             if i.isalpha():
#                 s += i
#             else:
#                 if s:
#                     l.append(s)
#                 s = ''
#         if s:
#             l.append(s)
#         print(' '.join(l[::-1]))
#     except:
#         raise


# 29
# while True:
#     try:
#         a = input().strip()
#         m = 0
#         for i in range(len(a)-1):
#             for j in range(i+1, len(a)+1):
#                 print(a[i:j])
#                 if a[i:j] == a[i:j][::-1]:
#                     if j - i > m:
#                         m = j - i
#         print(m)
#     except:
#         raise
# while True:
#     try:
#         a = input().strip()
#         m = 0
#         for i in range(1, len(a)):
#             if i - m >= 1 and a[i-m-1:i+1] == a[i-m-1:i+1][::-1]:
#                 m += 2
#             elif i - m > 0 and a[i-m:i+1] == a[i-m:i+1][::-1]:
#                 m += 1
#         print(m)
#     except:
#         raise

# # 30
# while True:
#     try:
#         a = map(bin, map(int, input().split('.')))
#         b = bin(int(input()))[2:].rjust(32, "0")
#         s = ""
#         for i in a:
#             t = i[2:].rjust(8, "0")
#             s += t
#         r = []
#         for i in range(4):
#             r.append(str(int(b[8*i:8*(i+1)], base=2)))
#         print(int(s, base=2))
#         print('.'.join(r))
#     except:
#         raise

# # 31
# while True:
#     try:
#         print(''.join(sorted(input())))
#     except:
#         break

# # 32
# while True:
#     try:
#         n = int(input())
#         p, f = [], 1
#         for i in range(n):
#             q = [f]
#             for j in range(i, n-1):
#                 q.append(q[j-i]+j+2)
#             p.append(q)
#             f += i+1
#         for i in p:
#             print(' '.join(map(str, i)))
#     except:
#         raise

# # 33
# m = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# while True:
#     try:
#         key, pw, chs, res = input(), input(), [], ''
#         for i in key:
#             i = i.upper()
#             if i not in chs:
#                 chs.append(i)
#         n = []
#         chs += m
#         for i in chs:
#             if i not in n:
#                 n.append(i)
#         for i in pw:
#             c = n[m.index(i.upper())]
#             if i.islower():
#                 res += c.lower()
#             else:
#                 res += c
#         print(res)
#     except:
#         raise

# # 34
# # while True:
# #     try:
# #         month = int(input()) - 1
# #         a, b, c = 1, 0, 0
# #         while month:
# #             c += b
# #             b = a
# #             a = c
# #             month -= 1
# #         print(a+b+c)
# #     except:
# #         break
# def fn(m):
#     if m < 3:
#         return 1
#     return fn(m-1) + fn(m-2)
#
# while True:
#     try:
#         month = int(input())
#         print(fn(month))
#     except:
#         raise

# # 35
# while True:
#     try:
#         h = int(input())
#         s = 0
#         for i in range(5):
#             s += h + h/2
#             h = h / 2
#         s = s - h
#         print(s, h)
#     except:
#         break

# # 36
# while True:
#     try:
#         mask, ip1, ip2 = input(), input(), input()
#         s = ''
#         for i in range(mask.split('.')):
#             s += bin(int(i))[2:].rjust(8, "0")
#         if '01' in s:
#             print(1)
#             break
#         f = False
#         for i in range(ip1.split('.')):
#             if i > '255':
#                 f = True
#         if f:
#             print(1)
#             break
#         for i in range(ip2.split('.')):
#             if i > '255':
#                 f = True
#         if f:
#             print(1)
#             break
#         print()
#     except:
#         break

# # 37
# while True:
#     try:
#         n, m, x = int(input()), list(map(int, input().split())), list(map(int, input().split()))
#         l = [[m[i]*j for j in range(1, x[i]+1)] for i in range(n)]
#         p = set()
#         print(l)
#         q = [0]
#         for i in l:
#             i = [0] + i
#             for j in i:
#                 for k in q:
#                     p.add(k + j)
#             q = list(p)
#         print(len(q))
#     except:
#         raise

# # 38
# while True:
#     try:
#         a = input()
#         if a.isdigit():
#
#     except:
#         raise