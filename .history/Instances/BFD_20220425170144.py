from doctest import FAIL_FAST


def bestFit(capacity, items, weights):
    binCount = 0
    bin = [capacity] * items
    binCap = capacity
    numItems = items
    itemWeights = weights

    #for loop goes through each item to place the item into a bin
    for item in range(numItems):
        index = 0
        min = binCap
        bestBin = 0

        #places the item in the bin that will have the least room left over with that
        #item in the bin and if it cannot fit, create a new bin.
        while(index < binCount):
            if(bin[index] >= itemWeights[item] and bin[index] - itemWeights[item] < min):
                bestBin = index
                min = bin[index] - itemWeights[item]
            index += 1
        #if item wasn't placed into a bin, create a new bin
        if(min == binCap):
            bin[binCount] = binCap - itemWeights[item]
            binCount += 1
        else:
            bin[bestBin] -= itemWeights[item]
    
    return binCount

def bestFitDec(capacity,items,weights):
    sortedWeights= sorted(weights,reverse=True)
    return bestFit(capacity,items,sortedWeights)


#main operations of the program
def main():
    #open file with input data and read in each line to set to variables
    with open("test.txt", "r") as inputFile:
        testCase = int(inputFile.readline().rstrip())

        #Loop through each test case
        for entry in range(testCase):
            #set the capacity equal to the entry read in
            capacity = int(inputFile.readline().rstrip())

            #set the number of items equal to the entry read in
            items = int(inputFile.readline().rstrip())

            #create an array for the weights entered on the next line
            weights = list(map(int, inputFile.readline().rstrip().split()))

            binsDecBestFit= bestFitDec(capacity,items,weights)

            print("Test case %d" % (entry+1))
            print("Best-Fit-Decreasing: %d" % (binsDecBestFit))
            print("\n")

if __name__ == "__main__":
    main()