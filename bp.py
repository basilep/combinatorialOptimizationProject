import re
from tkinter import E
import pyomo.environ as pe
import pyomo.opt as po
import math
import os
import time
import pandas
import copy
from IPython.display import display

################################
###           GLPK           ###
################################

# Globals variable
# List to display the result in a DataFrame
result_set = []
result_id = 0

# List for branch and bound
total_result = []
"""
Allow to display the results in a dataframe and in detail file
"""
def display_result(tuple_obj_x_y):
    global result_set
    global result_id
    if(tuple_obj_x_y == None):
        d = open("details_glpk.txt", "a")
        d.write("\nFail\n\n")
        result_set[result_id]["solution"] = "not found"
        result_set[result_id]["result"] = "fail"
        d.close()
    else:
        details_data = []
        obj = tuple_obj_x_y[0]
        print("Number of boxes used: ",obj)
        x = tuple_obj_x_y[1]
        y = tuple_obj_x_y[2]
        d = open("details_glpk.txt", "a")
        d.write("\n")
        for b in range(0, len(y)):
            details_data.append({"product":"", "box":""})
            #If a box is used, find the products in this box from range of the number of products
            if(y[b]==1.0):
                details_data[b]["box"] = str(b)
                #print("The box ", b, " is used and contains the products:")
                for p in range(b*len(y), b*len(y)+len(y)):
                    if(x[p] == 1.0):
                        #print(p-b*len(y))
                        details_data[b]["product"] = details_data[b]["product"]+str(p-b*len(y))+", "
                details_data[b]["product"] = details_data[b]["product"][:len(details_data[b]["product"])-2]
                #remove empty boxes
                clean_data = [elem for elem in ({key: val for key, val in sub.items() if val} for sub in details_data) if elem]
                
        result_set[result_id]["solution"] = int(obj)
        result_set[result_id]["result"] = "success"
        df_detail = pandas.DataFrame(clean_data, columns=['box', 'product'])
        df_detail = df_detail.set_index('box')
        #display(df_detail)
        d.write(str(df_detail)+"\n\n")
        d.close()
"""
Get product in a dictionnary from an instance file (from the statement)
"""
def get_products_parameter(all_products):
    result_dictionnary = {}
    for elem in all_products:
        tmp = elem.split(" ")
        if(";" in elem):
            result_dictionnary[int(tmp[4])] = int(tmp[5][:len(tmp[5])-2])
        else:
            result_dictionnary[int(tmp[4])] = int(tmp[5][:len(tmp[5])-1])
        
    return result_dictionnary
"""
Get the physical minimum of boxes to use
"""
def minimum_boxes(capacity, data):
    weight=0
    for elem in data.values():
        weight+=elem
    return int(math.ceil(weight / capacity))
"""
Solve the bin packing problem from an instance
Return a tuple containing:
- the optimal value (obj)
- an optimal solution with a list of x[p][b] = xpb and a list of y[b] = yb
"""
def solve_bp_lp(instance_name):
    global result_set
    global result_id
    data_file = get_data_instance(instance_name)
    #Get the box capacity from the file's data
    box_capacity = data_file[2].split(":= ")[1]
    #Remove the ";"
    box_capacity = box_capacity[:len(box_capacity)-2]
    result_set[result_id]["c"] = box_capacity
    product_parameters= get_products_parameter(data_file[5:])
    number_of_products = len(product_parameters)
    result_set[result_id]["n"] = number_of_products
    #print(product_parameters)
    #print("Number of products: ",number_of_products)
    #print("Box capacity: "+box_capacity)
    #print("Size of the different products:", list(product_parameters.values()))
    result_set[result_id]["lb"] = minimum_boxes(int(box_capacity), product_parameters)
    #print("Physical minimum number of boxes to use:", minimum_boxes(int(box_capacity), product_parameters))
    solver = po.SolverFactory('glpk') # GNU Linear Programming Kit
    #Create the model
    model = pe.ConcreteModel() #Create the concrete model
    model.P = pe.RangeSet(0, number_of_products-1)  #Number of products (P)
    model.B = pe.RangeSet(0, number_of_products-1)  #Maximum number of boxes (Equals to P)
    
    #Decision variable
    model.x = pe.Var(model.P,model.B, domain=pe.Binary)  #x_pb
    model.y = pe.Var(model.B, domain=pe.Binary)  #y_b

    #Objective
    model.obj = pe.Objective(sense=pe.minimize, expr=sum(model.y[b] for b in model.B))

    #Data
    model.s = pe.Param(model.P, initialize=product_parameters)
    model.c = pe.Param(initialize=int(box_capacity))
    
    #Constraints
    model.capacity_box_const = pe.ConstraintList()
    for b in model.B:
        lhs=sum(model.s[p] * model.x[p,b] for p in model.P)
        rhs=model.c * model.y[b]    
        model.capacity_box_const.add(lhs <= rhs)

    model.product_in_only_one_box = pe.ConstraintList()
    for p in model.P:
        lhs=sum(model.x[p,b] for b in model.B)
        rhs=1
        model.product_in_only_one_box.add(lhs == rhs)

    #Solver
    solver.solve(model, timelimit=600)    #To get the details : tee=True
    try:
        #Results
        obj = pe.value(model.obj)
        x = []
        y = []
        for b in model.B:
            y.append(pe.value(model.y[b]))
            for p in model.P:
                x.append(pe.value(model.x[p, b]))
        return (obj, x, y)
    except:
        return None
"""
Solve the linear relaxation problem with glpk
For all instances in the current folder
Store the result in result_glpk.txt
and the details of the products in box in details_glpk.txt
"""
def launch_glpk():
    global result_id

    f = open("result_glpk.txt", "w")
    f.close()
    d = open("details_glpk.txt", "w")
    d.close
    
    instances = get_instances()
    for instance in instances:
        d = open("details_glpk.txt", "a")
        d.write(instance)
        d.close()
        print(instance)
        result_set.append({"file":instance})
        time_before = time.time()
        try:
            display_result(solve_bp_lp("./"+instance))
        except:
            print("ERROR")
        time_after = time.time()
        print("The solve lasts ", round(time_after-time_before, 2), "seconds\n")  #Round the float to 2 digits after the comas
        result_set[result_id]["time"] = round(time_after-time_before, 2)
        result_id += 1
    df = pandas.DataFrame(result_set, columns=['file', 'c', 'n', 'lb', 'solution', 'result', 'time'])
    print(df.to_string())
    f = open("result_glpk.txt", "a")
    f.write(df.to_string())
    f.close()

#################################
###     Branch and bound      ###
#################################

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
Compute another lower bound
"""
def compute_lb2(capacity,product,node):
    wj=[]
    for sac in node:
        super_item=0
        for i in sac:
            super_item+=i
        wj.append(super_item)
    for i in product:
        wj.append(i)

    max_lb=0
    wj_min = [i for i in wj if i <capacity/2]
    #print(wj_min)

    for alpha in wj_min:
        j1_bound=capacity-alpha
        j2_bound=capacity/2
        j3_bound=alpha
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
        max_lb=max(max_lb,math.ceil(lb))
        
    #print('max_lb is',max_lb)
    return max_lb
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


def branch_and_bound(instance_name, branching_scheme, valid_inequalities, time_limit):
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
            result[left_id] = [left_set[left_id], compute_lb2(capacity, product[1:], left_set[left_id]), heuristic_local(capacity, product[1:], left_set[left_id])]
        right = forward_right(product, copy.deepcopy(node_actuel))
        result[left_id+1] = [right, compute_lb2(capacity, product[1:], right), heuristic_local(capacity, product[1:], right)]
    return result
"""
Get all the sub tree from a node
"""
def get_child_info(capacity, product, node_actuel):
    global total_result
    global start_time
    if(product == []):
        #print(node_actuel)
        total_result.append(node_actuel)
    else:
        if(time.time() > start_time + 10):
            return False
        child_info = get_child_node(capacity, product, node_actuel)
        lower_bounds=[]
        sol_heuristic=[]
        for key, val in child_info.items():
            lower_bounds.append(val[1])
            sol_heuristic.append(val[2])
        lb_min = min(lower_bounds)
        sol_heu_min = min(sol_heuristic)
        for min_id in range(len(sol_heuristic)):
            if (sol_heuristic[min_id] == sol_heu_min) and (lower_bounds[min_id] == lb_min):
                try:
                    get_child_info(capacity, product[1:], child_info.get(min_id)[0])
                except:
                    get_child_info(capacity, product[1:], child_info.get(min_id+1)[0])
"""

"""
def bb(instance):
    data_file = get_data_instance(instance)
    #Get the box capacity from the file's data
    box_capacity = data_file[2].split(":= ")[1]
    #Remove the ";"
    box_capacity = box_capacity[:len(box_capacity)-2]
    product_parameters=get_products_parameter(data_file[5:])
    product_list = [int(product) for product in list(product_parameters.values())]
    get_child_info(int(box_capacity), product_list, [])
    return len(product_list)
"""
PAS ENCORE OK
"""
def launch_branch_and_bound():
    global total_result
    global start_time
    f = open("result_branch_and_bound_lb2.txt", "w")
    f.close()
    instances = get_instances()
    for instance in instances:
        total_result=[]
        d = open("result_branch_and_bound_lb2.txt", "a")
        d.write(instance+"\n")
        print(instance)
        start_time = time.time()
        min_boxes = bb(instance)    #Call the branch_and_bound function
        after = time.time()
        d = open("result_branch_and_bound_lb2.txt", "a")
        d.write("Time of solving: "+"%0.2f" % (after - start_time)+"\n")
        print("Time of solving: ", "%0.2f" % (after - start_time))
        for elem in total_result:
            if len(elem) < min_boxes:
                min_boxes = len(elem)
        for elem in total_result:
            if len(elem) == min_boxes:
                print(len(elem))
                d.write("Obj: "+ str(len(elem))+"\n")
                print(elem)
                d.write("Details: "+ str(elem)+"\n\n")
                break
        if len(total_result) == 0:
            print("fail")
            d.write("Fail\n\n")
        d.close()

#############################
###         Tools         ###
#############################

"""
Gets the files names from the directory
"""
def get_instances():
    files = os.listdir("./Instances")
    instances = []
    #remove other file
    for file in files:
        if file.endswith(".dat"):
            instances.append(file)
    return instances

"""
Read and extract the interesting data from an instance
"""
def get_data_instance(instance):
    #Open the instance's file
    instanceFile = open("./Instances/"+instance, "r")
    #Read the file and store every line in a list
    data_file = instanceFile.readlines()
    #Close the file
    instanceFile.close()
    return data_file

#############################
###       Main code       ###
#############################
start_time = 0
#launch_branch_and_bound()