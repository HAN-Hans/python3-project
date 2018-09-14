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
while True:
    try:
        a = int(input())
        b = map(int, input().split()[:8])
        for i in range(a):
            n, m = 0, 0
            for j in range(i):
                if b[j] < b[i]:
                    n += 1
            for j in range(a - i):
                if b[j] > b[i]:
                    m += 1

    except:
        pass