# ziping on;y wrks in pyhton 2 make sure hte list are of the same size
l1 = ["1","2","3","4","5"]
l2 = ["6","7","8","9","10"]

# in python 3 or greater it worsk like this
zipped = list(zip(l1, l2))
print(zipped)

#unzipping  in python 3 we have to make sure its a list before unziping 

unzipped = list( zip(*zipped))
print(unzipped)