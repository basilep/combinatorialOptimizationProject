import os
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


# print(instances)
# for i in instances:
    # print(i)
    # solve_bp_lp(i)
for i in range(150):
    with open('test.txt','w') as f:
        f.write('1')

# with open('text.txt','w',encoding='utf-8')as f: 
#     f.write('文件读取\n文件写入')  #\n换行符
# #查看文件内容
# with open('text.txt','r',encoding='utf-8')as f: 
#     print(f.read()) 


# solve_bp_lp('bin_pack_125_1.dat')
