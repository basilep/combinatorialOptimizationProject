import os

from matplotlib.pyplot import box
def get_products_parameter(all_products):
    result_dictionnary = {}
    for elem in all_products:
        tmp = elem.split(" ")
        if(";" in elem):
            result_dictionnary[int(tmp[4])] = int(tmp[5][:len(tmp[5])-2])
        else:
            result_dictionnary[int(tmp[4])] = int(tmp[5][:len(tmp[5])-1])
        
    return result_dictionnary
def solve_bp_lp(instance_name):
    #Get the number of produts from the file's name of the instance
    number_of_product = instance_name[11:len(instance_name)].split("_")[0]
    print("Number of products: "+number_of_product)
    #Open the instance's file
    instance = open(instance_name, "r")
    #Read the file and store every line in a list
    data_file = instance.readlines()
    #Get the box capacity from the file's data
    box_capacity = data_file[2].split(":= ")[1]
    #Remove the ";"
    box_capacity = box_capacity[:len(box_capacity)-2]
    print("Box capacity: "+box_capacity)
    product_parameters= get_products_parameter(data_file[5:])
    print(product_parameters)
    #Close the file
    instance.close()
    return data_file

instances = os.listdir(".")
if "bp.py" in instances:
    instances.remove("bp.py")
if "result.txt" in instances:
    instances.remove("result.txt")
if "details.txt" in instances:
    instances.remove("details.txt")
if "binpack.py" in instances:
    instances.remove("binpack.py")
if "opentool.py" in instances:
    instances.remove("opentool.py")
if "test.txt" in instances:
    instances.remove("test.txt")



with open('test.txt','w') as f:
    for i in instances:
        instanceFile=open(i,'r')
        data_file=instanceFile.readlines()
        instanceFile.close()
        box_capacity = data_file[2].split(":= ")[1]
        box_capacity = box_capacity[:len(box_capacity)-2]
        f.write(str(box_capacity)+"\n")
        product_parameters= get_products_parameter(data_file[5:])
        number_of_products = len(product_parameters)
        f.write(str(number_of_products)+"\n")
        for i in product_parameters.values():
            f.write(str(i))
            f.write(str(" "))
        f.write("\n")   


