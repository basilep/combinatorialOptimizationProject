from tkinter import E
import pyomo.environ as pe
import pyomo.opt as po
import math
import os
import time
import pandas
from IPython.display import display

def display_result(tuple_obj_x_y):
    if(tuple_obj_x_y == None):
        d = open("details.txt", "a")
        d.write("\nFail\n\n")
        result_set[i]["solution"] = "not found"
        result_set[i]["result"] = "fail"
        d.close()
    else:
        details_data = []
        obj = tuple_obj_x_y[0]
        print("Number of boxes used: ",obj)
        x = tuple_obj_x_y[1]
        y = tuple_obj_x_y[2]
        d = open("details.txt", "a")
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
                
        result_set[i]["solution"] = int(obj)
        result_set[i]["result"] = "success"
        df_detail = pandas.DataFrame(clean_data, columns=['box', 'product'])
        df_detail = df_detail.set_index('box')
        #display(df_detail)
        d.write(str(df_detail)+"\n\n")
        d.close()

def get_products_parameter(all_products):
    result_dictionnary = {}
    for elem in all_products:
        tmp = elem.split(" ")
        if(";" in elem):
            result_dictionnary[int(tmp[4])] = int(tmp[5][:len(tmp[5])-2])
        else:
            result_dictionnary[int(tmp[4])] = int(tmp[5][:len(tmp[5])-1])
        
    return result_dictionnary

def minimum_boxes(capacity, data):
    weight=0
    for elem in data.values():
        weight+=elem
    return int(math.ceil(weight / capacity))

def solve_bp_lp(instance_name):
    #Open the instance's file
    instanceFile = open(instance_name, "r")
    #Read the file and store every line in a list
    data_file = instanceFile.readlines()
    #Close the file
    instanceFile.close()
    #Get the box capacity from the file's data
    box_capacity = data_file[2].split(":= ")[1]
    #Remove the ";"
    box_capacity = box_capacity[:len(box_capacity)-2]
    result_set[i]["c"] = box_capacity
    product_parameters= get_products_parameter(data_file[5:])
    number_of_products = len(product_parameters)
    result_set[i]["n"] = number_of_products
    #print(product_parameters)
    #print("Number of products: ",number_of_products)
    #print("Box capacity: "+box_capacity)
    #print("Size of the different products:", list(product_parameters.values()))
    result_set[i]["lb"] = minimum_boxes(int(box_capacity), product_parameters)
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
    solver.solve(model, timelimit=10)    #To get the details : tee=True
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

#display_result(solve_bp_lp("./bin_pack_20_0.dat"))
#Gets the files names from the directory  
instances = os.listdir(".")
if "bp.py" in instances:
    instances.remove("bp.py")
if "result.txt" in instances:
    instances.remove("result.txt")
if "details.txt" in instances:
    instances.remove("details.txt")
if "BFD.py" in instances:
    instances.remove("BFD.py")
if "opentool.py" in instances:
    instances.remove("opentool.py")
if "test.txt" in instances:
    instances.remove("test.txt")
    

f = open("result.txt", "w")
f.close()
d = open("details.txt", "w")
d.close()
#List to display the result in a DataFrame
result_set = []
i=0
for instance in instances:
    d = open("details.txt", "a")
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
    result_set[i]["time"] = round(time_after-time_before, 2)
    i+=1
df = pandas.DataFrame(result_set, columns=['file', 'c', 'n', 'lb', 'solution', 'result', 'time'])
print(df.to_string())
f = open("result.txt", "a")
f.write(df.to_string())
f.close()
