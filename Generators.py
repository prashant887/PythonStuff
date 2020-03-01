def myGen():
    yield 'A'
    yield 'B'
    yield 'C'

g=myGen()
print(type(g))

print(next(g))

gn=(x*x for x in range(10))


for i in gn:
    print(i)
    
while True:
    try:
        print(next(g))
    except Exception as ex:
        print (ex)
		

def genFirstNnums(n):
    num=0
    while num<n:
        yield num
        num=num+1
        
for i in genFirstNnums(10):
    print(i)
	
def fib():
    a,b=0,1
    while True:
        yield a
        a,b=b,a+b
        

for i in fib():
    if i>100:
        break
    print(i)