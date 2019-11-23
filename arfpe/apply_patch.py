import os
import basic_func as bf
import xlrd
import sys
def refresh():
    command = "rm -rf ../benchmark/gsl-2.6-repair/specfunc/"
    command2 = "cp -R ../benchmark/gsl-2.6/specfunc/. ../benchmark/gsl-2.6-repair/specfunc/"
    os.system(command)
    os.system(command2)

fid_lc = [2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 63, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]


def read_file(file_name):
    fp = open(file_name)  # Open file on read mode
    lines = fp.read().split("\n")  # Create a list containing all lines
    fp.close()  # Close file
    # /home/yixin/PycharmProjects/AutoEFT/benchmarkss/gsl_src/gsl-2.1-repair/specfunc/airy.c
    index_lst = []
    for i in lines:
        var_lst = []
        if i != '':
            temp_i = i.split()
            for j in range(4, len(temp_i)):
                if (temp_i[j] == 'double') | (temp_i[j] == temp_i[0] + '(double'):
                    if temp_i[j + 1] == '*':
                        var_lst.append(temp_i[j + 2].strip(',)'))
                    else:
                        var_lst.append(temp_i[j + 1].strip(',)'))
            index_lst.append([temp_i[0], temp_i[2], temp_i[3], var_lst])
    return index_lst

def search_line_num4f(fun_name,exname):
    data = xlrd.open_workbook(exname)
    table = data.sheets()[0]
    file_name = ''
    for i in range(0, table.nrows-1):
        temp_str = str(table.row_values(i + 1)[0]).strip('\'')
        if temp_str == fun_name:
            file_name = table.row_values(i + 1)[2].strip('\'')
    ori_file_name = file_name
    pwd1 = os.getcwd()
    os.chdir("..")
    pwd = os.getcwd()
    file_name = pwd+'/benchmark/gsl-2.6-repair/specfunc/' + file_name
    os.chdir(pwd1)
    os.system('ctags -x --c-kinds=f %s > fun_index.txt' % (file_name))
    index_lst = read_file('fun_index.txt')
    line_num = 0
    for i in index_lst:
        if fun_name == i[0]:
                line_num = int(i[1])
    fp = open(file_name)  # Open file on read mode
    lines = fp.read().split("\n")  # Create a list containing all lines
    fp.close()
    insert_num = line_num + 1
    for i in range(line_num,len(lines)):
        if lines[i-1] == '{':
            insert_num = i
            break
    return ori_file_name,insert_num


refresh()
# fun_index = bf.load_pickle("/home/yixin/PycharmProjects/ARFPE/src/gsl_26_calls")
# for i in fun_index:
#     print i
# inter_funcs = bf.load_pickle('fun_index.pkl')
# for i in fid_lc:
#     test_fun = inter_funcs[i]
#     print test_fun
#     insert_fname, insert_line = search_line_num4f(test_fun[0], "fun_index.xls")
#     print insert_fname, insert_line
#     gsl_file = "../benchmark/gsl-2.6-repair/specfunc/" + insert_fname
#     insert_file = "patches/insert_code/" + test_fun[0]+'.c'
#     orig_stdout = sys.stdout
#     patch_name = 'patch_of_'+test_fun[0] +'.c'
#     patch_name_str = '#include \"patch_of_'+test_fun[0] +'.c\" \n'
#     print patch_name
#     f = open(insert_file, "r")
#     contents = f.readlines()
#     f.close()
#     f = open(gsl_file, "r")
#     new_contents = f.readlines()
#     f.close()
#     for j in range(0, len(contents)):
#         new_contents.insert(insert_line, " " + contents[j])
#         insert_line = insert_line + 1
#     new_contents.insert(0, patch_name_str)
#     f = open(gsl_file, "w")
#     new_contents = "".join(new_contents)
#     f.write(new_contents)
#     f.close()
# command2 = "cp -R /home/yixin/PycharmProjects/ARFPE/arfpe/patches/. ../benchmark/gsl-2.6-repair/specfunc/"
# os.system(command2)