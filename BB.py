from calendar import c
import math
import copy
from pickle import TRUE
from unittest import result

"""
Compute the lower bound of a node
"""
def compute_lb(capacity,product,node):
    if len(product)!=0:
        lowest_product=min(product)
    else:
        for sac in node:
            lowest_product=min(sac)

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

    lb=len(j1)+len(j2)+max(0,(sum(j3)-(len(j2)*capacity-sum(j2)))/capacity)
    
    return math.ceil(lb)
"""
Compute the heurisical solution from a node
"""
def heuristic_local(capacity, product,node):
    # Setup all variables for loops
    binCount = len(node)
    bin = [capacity] * (len(product)+binCount)
    i=0
    for sac in node:  
        super_item=0    
        for j in sac:
            super_item+=j

        bin[i]=capacity-super_item
        i+=1

    # For loop goes through each item to place the item into a bin
    for item in range(len(product)):
        index = 0
        # While loop finds the bin to place the item into based on space
        # And what's open
        while(index < binCount):
            if(bin[index] >= product[item]):
                bin[index] = bin[index] - product[item]
                break
            index += 1
        # If there wasn't a bin for the item to go into, open a new one
        if(index == binCount):
            bin[binCount] = capacity - product[item]
            binCount += 1
   
    return binCount

"""
Get all possible node from the left boxes
"""
def forward_left(capacity,product,node_actuel):
    node_left=copy.deepcopy(node_actuel)
    node_left_ensemble=[]
    new_product=product[0]

    for sac in node_left: 
        super_item=0    
        for j in sac:
            super_item+=j
        if super_item+new_product<=capacity:
            sac.append(new_product)   #sac est juste un 
            node_left1=copy.deepcopy(node_left)
            node_left_ensemble.append(node_left1)
            sac.pop()

    return node_left_ensemble
"""
Get the node right
"""
def forward_right(product,node_actuel):
    node_right=node_actuel
    new_product=product[0]
    new_bag=[new_product]
    node_right.append(new_bag)
    return node_right


def branch_and_bound(instance_name, branching_scheme ,valid_inequalities, time_limit):
    return True

"""
Calculate all the possible child node with their lower bound and their heuristic solution

capacity = capacity of the boxes
product = the product that are not already in a box
node_actuel = node from where the child are calculated (product already in boxes)

return result which is a dictionnary containing the different nodes with their lower bound and heuristic solution
{i: [[node], lb, heur_sol]}

"""
def get_child_node(capacity, product, node_actuel):
    if(product == []):
        return False
    else:
        # Get left child
        # Need to deepcopy, otherwise, the forward_left change the node_actuel variable
        left_set = forward_left(capacity, product, copy.deepcopy(node_actuel))
        result = {}
        left_id = 0
        for left_id in range(len(left_set)):
            result[left_id] = [left_set[left_id], compute_lb(capacity, product[1:], left_set[left_id]), heuristic_local(capacity, product[1:], left_set[left_id])]
        right = forward_right(product, copy.deepcopy(node_actuel))
        result[left_id+1] = [right, compute_lb(capacity, product[1:], right), heuristic_local(capacity, product[1:], right)]
    return result
"""
Get all the sub tree from a node
"""
def get_child_info(capacity, product, node_actuel):
    if(product == []):
        total_result.append(node_actuel)
    else:
        child_info = get_child_node(capacity, product, node_actuel)
        for key, val in child_info.items():
            get_child_info(capacity, product[1:], val[0])

def test(capacity, product, node_actuel):
    if(product == []):
        total_result.append(node_actuel)
    else:
        child_info = get_child_node(capacity, product, node_actuel)
        lower_bounds=[]
        lower_key = []
        sol_heuristic=[]
        sol_heur_key = []
        for key, val in child_info.items():
            lower_bounds.append(val[1])
            lower_key.append(key)
            sol_heuristic.append(val[2])
            sol_heur_key.append(key)
        print(sol_heuristic)
        #print(lower_bounds)
        #print(sol_heuristic)
        #print(node_actuel)
        lb_min = min(sol_heuristic)
        for min_id in range(len(sol_heuristic)):
            if sol_heuristic[min_id] == lb_min:
                print(child_info)
                print(min_id)
                #print(lb_min)
                #print(child_info.get(min_id)[0])
                test(capacity, product[1:], child_info.get(min_id)[0])
        index_min_lb = lower_bounds.index(min(lower_bounds))
        index_min_sol = sol_heuristic.index(min(sol_heuristic))  

total_result = []

#get_child_info(100, [49, 41, 34, 33, 29, 26, 26, 22, 20, 19], [])

min_boxes = 10 #Changer en len(product) par la suite
supp = []

for elem in total_result:
    if len(elem) < min_boxes:
        min_boxes = len(elem)
    """
    print(elem)
    if elem not in supp:
        supp.append(elem)"""
for elem in total_result:
    if len(elem) == min_boxes:
        print(elem)
        print(len(elem))


def compute_lb3(capacity,product_list,node):
    wj=[]
    # Gets all the products in the problem
    wj = get_all_products(product_list, node)

    max_lb=0
    wj_min = [i for i in wj if i <capacity/2]

    for alpha in wj_min:
        j1_bound=capacity-alpha
        j2_bound=capacity/2
        j3_bound=alpha
        j1=[]
        j2=[]
        j3=[]
    
        for product in wj:
            if product>j1_bound:
                j1.append(product)
            elif product>j2_bound and product <=j1_bound:
                j2.append(product)
            elif product>=j3_bound and product <=j2_bound:
                j3.append(product)
 
        lb=len(j1)+len(j2)+max(0,(sum(j3)-(len(j2)*capacity-sum(j2)))/capacity)
        max_lb=max(max_lb,math.ceil(lb))
        
    return max_lb

def get_all_products(product_list, node):
    products = []
    for sac in node:
        for product in sac:
            products.append(product)

    for product in product_list:
        products.append(product)
    return products
    
print(compute_lb3(100, [34, 33, 29, 26, 26, 22, 20, 19], [[49], [41]]))