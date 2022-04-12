import pyomo.environ as pe
import pyomo.opt as po
import math

def display_result(tuple_obj_x_y):
    obj = tuple_obj_x_y[0]
    x = tuple_obj_x_y[1]
    y = tuple_obj_x_y[2]
    for b in range(0, len(y)):
        #If a box is used, find the products in this box from range of the number of products
        if(y[b]==1.0):
            print("The box ", b, " is used and contains the products:")
            for p in range(b*len(y), b*len(y)+len(y)):
                if(x[p] == 1.0):
                    print(p-b*len(y))
    print("\nAll data:")
    print("Minimum number of boxes to use:", obj,"\n",x,"\n",y)

def get_products_parameter(all_products):
    result_dictionnary = {}
    print(all_products)
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
    instance = open(instance_name, "r")
    #Read the file and store every line in a list
    data_file = instance.readlines()
    #Close the file
    instance.close()
    #Get the box capacity from the file's data
    box_capacity = data_file[2].split(":= ")[1]
    #Remove the ";"
    box_capacity = box_capacity[:len(box_capacity)-2]
    product_parameters= get_products_parameter(data_file[5:])
    number_of_products = len(product_parameters)
    print("Number of products: ",number_of_products)
    print("Box capacity: "+box_capacity)
    print(product_parameters)
    print("Physical minimum number of boxes to use:", minimum_boxes(int(box_capacity), product_parameters))
    solver = po.SolverFactory('glpk') # GNU Linear Programming Kit
    #Create the model
    model = pe.ConcreteModel() #Create the concrete model
    model.P = pe.RangeSet(0, number_of_products-1)  #Number of products (P)
    model.B = pe.RangeSet(0, number_of_products-1)  #Maximum number of boxes (Equals to P)

    model.x = pe.Var(model.P,model.B, domain=pe.Binary)  #x_pb
    model.y = pe.Var(model.B, domain=pe.Binary)  #y_b

    model.obj = pe.Objective(sense=pe.minimize, expr=sum(model.y[b] for b in model.B))

    model.s = pe.Param(model.P, initialize=product_parameters)
    model.c = pe.Param(initialize=int(box_capacity))
    
    #Constraints
    model.product_in_only_one_box = pe.ConstraintList()
    for p in model.P:
        lhs=sum(model.x[p,b] for b in model.B)
        rhs=1
        model.product_in_only_one_box.add(lhs == rhs)

    model.capacity_box_const = pe.ConstraintList()
    for b in model.B:
        lhs1=sum(model.s[p] * model.x[p,b] for p in model.P)
        rhs1=model.c * model.y[b]    
        model.capacity_box_const.add(lhs1 <= rhs1)

    #Solver
    solver.solve(model,tee=True)
    
    #Results
    obj = pe.value(model.obj)
    x = []
    y = []
    for b in model.B:
        y.append(pe.value(model.y[b]))
        for p in model.P:
            x.append(pe.value(model.x[p, b]))
    return (obj, x, y)

display_result(solve_bp_lp("./bin_pack_25_2.dat"))


