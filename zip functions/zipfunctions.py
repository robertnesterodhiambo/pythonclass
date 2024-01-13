# ziping on;y wrks in pyhton 2 make sure hte list are of the same size
l1 = ["1","2","3","4","5"]
l2 = ["6","7","8","9","10"]

# in python 3 or greater it worsk like this
zipped = list(zip(l1, l2))
print(zipped)

#unzipping  in python 3 we have to make sure its a list before unziping 

unzipped = list( zip(*zipped))
print(unzipped)

# zipped are used to read variable that are outside he for loops and other funtiosn into them 
#especially when getting a bunch of things into scope
#### exampes

for i in range(5):
    l1[i]
    l2[[i]]
    print(l1)

for (list1, list2) in zip(l1,l2):
    print(l1)
    print(l2)

items = ["apple","banana","orange"]
counts = [3, 15, 56]
prices = [12, 32, 36]

sentences = [] 
for (item, count, price) in (items, counts, prices):
    item, count, price = str(item), str(count), str(price)
    sentence = "I bought " + count + " " + item + "s at " + price + "shillings each ."
    sentences.append(sentence)
    print(sentences)