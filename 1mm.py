from pyrsistent import pvector

a = pvector([])
for i in range(10000000):
  a = a.append(i)

print (len(a))
print (a[12345])
