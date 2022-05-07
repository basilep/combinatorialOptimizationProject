from calendar import c
import math
import copy
from pickle import TRUE
from unittest import result
def compute_lb(capacity,product,node):
    if len(product)!=0:
        lowest_product=min(product)
    else:
        for sac in node:
            lowest_product=min(sac)
    # print("lowest_product is",lowest_product)
    j1_bound=capacity-lowest_product
    j2_bound=capacity/2
    j3_bound=lowest_product
    j1=[]
    j2=[]
    j3=[]
    for i in product:
        if i>j1_bound:
            j1.append(i)
        elif i>j2_bound and i <=j1_bound:
            j2.append(i)
        elif i>=j3_bound and i <=j2_bound:
            j3.append(i)
    
    for sac in node:  
        super_item=0    
        for j in sac:
            super_item+=j
        if super_item>j1_bound:
            j1.append(super_item)
        elif super_item>j2_bound and super_item <=j1_bound:
            j2.append(super_item)
        elif super_item>=j3_bound and super_item <=j2_bound:
            j3.append(super_item)
        # print("super_item is",super_item)
    # print("actuel_node is",node)
    # print("length of j1,j2,j3:",len(j1),len(j2),len(j3))
    lb=len(j1)+len(j2)+max(0,(sum(j3)-(len(j2)*capacity-sum(j2)))/capacity)
    #print("lower_bound is",math.ceil(lb))
    return math.ceil(lb)

def heuristic_local(capacity, product,node):
    #setup all variables for loops
    binCount = len(node)
    bin = [capacity] * (len(product)+binCount)
    # print(bin)
    i=0
    for sac in node:  
        super_item=0    
        for j in sac:
            super_item+=j

        bin[i]=capacity-super_item
        # print(bin[i])
        i+=1
    # print(bin)

    #for loop goes through each item to place the item into a bin
    for item in range(len(product)):
        index = 0
        #while loop finds the bin to place the item into based on space
        #and what's open
        while(index < binCount):
            if(bin[index] >= product[item]):
                bin[index] = bin[index] - product[item]
                break
            index += 1
        #If there wasn't a bin for the item to go into, open a new one
        if(index == binCount):
            bin[binCount] = capacity - product[item]
            binCount += 1


    #print("solution heuristique : ", binCount)    
    return binCount

#heuristic_local(100,[26,26,22,20,19],[[49,41],[34,33],[29]])

def forward_left(capacity,product,node_actuel):
    node_left=node_actuel
    new_product=product[0]
    # print("actual is",node_actuel)
    not_put_yet=True
    for sac in node_left:  
        super_item=0    
        for j in sac:
            super_item+=j
        if super_item+new_product<=capacity and not_put_yet==True:
            sac.append(new_product)
            not_put_yet=False

    #print("left is",node_left)
    return node_left

def forward_right(capacity,product,node_actuel):
    node_right=node_actuel
    new_product=product[0]
    new_bag=[new_product]
    # print("actual is",node_actuel)
    node_right.append(new_bag)
    #print("right is",node_right)
    return node_right
    
def forward(capacity,product,node_actuel):
    print("actual is",node_actuel)
    forward_right(capacity,product,node_actuel)
    forward_left(capacity,product,node_actuel)
    

# forward_left(100,[34,33,29,26,26,22,20,19],[[49],[41]])
#forward_right(100,[34,33,29,26,26,22,20,19],[[49],[41]])
#forward(100,[34,33,29,26,26,22,20,19],[[49],[41]])
#compute_lb(100,[29,26,26,22,20,19],[[49],[41,33],[34]])

def branch_and_bound(instance_name, branching_scheme ,valid_inequalities, time_limit):
    return True
""" 
def leftScheme(capacity, product, testNode):
    if(product==[]):
        print(testNode)
        return testNode
    else:
        #Precalculate left node if it's possible
        actual_node = copy.deepcopy(testNode)
        left = forward_left(capacity,product, testNode)
        #compute_lb(capacity, product, actual_node)
        if(left == actual_node):
            return leftScheme(capacity, product[1:], forward_right(capacity, product, actual_node))
        else:
            return leftScheme(capacity, product[1:], left)
   
def test(capacity, product, testNode):
    if(product==[]):
        return True
    else:
        firstProduct = product[0]
        node = copy.deepcopy(testNode)
        resultLeft = leftScheme(capacity, product, testNode)
        compute_lb(capacity, product, testNode)
        heuristic_local(capacity, product, node)
        
        test(capacity, product[1:], forward_right(capacity, product, node))


def leftThanRight(capacity, product):
    if(product==[]):
        return False
    else:
        productAllreadyPast = []
        result = []
        while(len(product)>0):
            left = leftScheme(capacity, product, [])
            result.append(productAllreadyPast + left)
            productAllreadyPast.append([product[0]])
            product = product[1:]
            
        print("\n\n")
        for elem in result:
            print(elem)"""

def get_child_node(capacity,product,node_actuel):
    if(product==[]):
        return False
    else:
        actual_lower_bound = compute_lb(capacity,product, node_actuel)
        #print("Actual node", node_actuel)
        #print("actual_lb", actual_lower_bound)

        # Get left child
        # Need to deepcopy, otherwise, the forward_left change the node_actuel variable
        left = forward_left(capacity,product, copy.deepcopy(node_actuel))
        left_lower_bound = compute_lb(capacity,product[1:], left)
        left_heuristic = heuristic_local(capacity,product[1:], left)
        #print("left", left)
        #print("left_lb", left_lower_bound)

        # Get right child
        right = forward_right(capacity,product, copy.deepcopy(node_actuel))
        right_lower_bound = compute_lb(capacity,product[1:], right)
        right_heuristic = heuristic_local(capacity,product[1:], right)
        #print("right", right)
        #print("right_lb", right_lower_bound)

    return {"left" : left, "left_lb" :left_lower_bound, "left_sol":left_heuristic, "right": right, "right_lb": right_lower_bound, "right_sol":right_heuristic}

def get_child_info(capacity,product,node_actuel):
    if(product==[]):
        total_result.append(node_actuel)
        #print(node_actuel)
        return False
    else:
        child_info = get_child_node(capacity,product,node_actuel)
        print("\n")
        for key, val in child_info.items():
            print(key,":", val)
        if(child_info.get("left")!= node_actuel):
            get_child_info(capacity,copy.deepcopy(product[1:]),copy.deepcopy(child_info.get("left")))
        get_child_info(capacity,copy.deepcopy(product[1:]),copy.deepcopy(child_info.get("right")))
        
        
#forward_left(100,[34,33,29,26,26,22,20,19], [[49,41]])
#leftThanRight(100,[49, 41, 34,33,29,26,26,22,20,19])

#leftScheme(100,[49, 41, 34,33,29,26,26,22,20,19],[])
total_result = []
get_child_info(100,[34,33,29,26,26,22,20,19], [[49], [41]])
print(len(total_result))
"""for elem in total_result:
    print(len(elem))"""

#print(forward_left(100, [34,33,29,26,26,22,20,19], [[49, 41]]))