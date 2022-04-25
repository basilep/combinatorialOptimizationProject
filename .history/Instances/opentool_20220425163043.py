import os

from matplotlib.pyplot import box
def get_products_parameter(all_products):
    result_dictionnary = {}
    for elem in all_products:
        tmp = elem.split(" ")
        result_dictionnary[tmp[4]] = tmp[5][:len(tmp[5])-1]
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
if "bin.txt" in instances:
    instances.remove("bin.txt")
if "binpack.py" in instances:
    instances.remove("binpack.py")
if "opentool.py" in instances:
    instances.remove("opentool.py")
if "test.txt" in instances:
    instances.remove("test.txt")


# print(instances)
# for i in instances:
    # print(i)
    # solve_bp_lp(i)

indice=1
with open('test.txt','w') as f:
    for i in instances:
        instanceFile=open(i,'r')
        data_file=instanceFile.readlines()
        instanceFile.close()
        f.write(str(indice)+"\n")
        indice+=1
        box_capacity = data_file[2].split(":= ")[1]
        box_capacity = box_capacity[:len(box_capacity)-2]
        f.write(str(box_capacity)+"\n")
        product_parameters= get_products_parameter(data_file[5:])
        print(product_parameters)
        number_of_products = len(product_parameters)
        f.write(str(number_of_products)+"\n")
        # f.write(str(indice)+"\n")
        # indice+=1
        # number_of_product = i[11:len(i)].split("_")[0]
        # f.write(str(number_of_product+"\n"))

        # f.write(str(150)+"\n")


        
# import random
# with open("2.txt","w") as f:
#   for i in range(5):
#     number=random.randint(1,50)
#     text=f.write(str(number)+"\n")
#     print(text)
# f.close()

solve_bp_lp('bin_pack_125_1.dat')
