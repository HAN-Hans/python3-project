n = input()
arr = []
for i in range(int(n)):
    arr.append(int(input()))
print(arr)
arr.sort()
print(arr)

for i in sorted(set(arr)):
    print(i)
