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

# 8
n = int(input())
d = {}
for i in range(n):
    a = input().split()
    if a[0] in d.keys():
        d[a[0]] = d[a[0]] + a[1]
    else:
        d[a[0]] = a[1]

p = sorted(d, key=lambda k:int(k))
print(p)
for k in p:
    print(k, d[k])


