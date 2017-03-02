# for decimal part
sum = 0
for i in range(12):
    if i == 0:
        continue
    x_square = 0.5**i
    bit = i + 1
    print ("square: {}, bit:{}".format(x_square, i))
    sum += x_square
    


# for int part
for i in range(6):
    x_square = 2**i
    bit = i + 1
    sum += x_square
    
print ("==========int part==========")
print (sum)
print ("bit:{}".format(bit))
