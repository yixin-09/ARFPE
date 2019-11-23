import os
def analysis_res_str(str):
    str1 = str.split('{')
    str2 = str1[-1].strip("}")
    str3 = str2.split(';')
    res_lst = []
    for i in str3:
        res_lst.append(int(i))
    return res_lst

def extract_bound_str(bound):
    str = ''
    for i in bound:
        temp_j = i[0]
        temp_str = repr(temp_j)
        for j in i[1:]:
            temp_str = temp_str + ','+ repr(j)
        if str != '':
            str = str + ',' + temp_str
        else:
            str = temp_str
    return str

def val_range_analysis(fun_name,bound,var_num):
    boud_str = extract_bound_str(bound)
    if boud_str != '':
        if var_num > 2:
            cmd = 'frama-c -load parsed.sav ' + ' -load-script add_anot.ml -main ' + fun_name + ' -adnt ' + ' -adnt-fun ' + fun_name + ' -DomainStr="' + boud_str + '"  -then -eva-ignore-recursive-calls  > log_'+fun_name
        else:
            cmd = 'frama-c -load parsed.sav ' + ' -load-script add_anot.ml -main ' + fun_name + ' -adnt ' + ' -adnt-fun ' + fun_name + ' -DomainStr="' + boud_str + '"  -then -eva -eva-equality-domain -eva-builtins-auto -slevel 200 -eva-ignore-recursive-calls  > log_' + fun_name
    else:
        if var_num > 2:
            cmd = 'frama-c -load parsed.sav ' + ' -load-script add_anot.ml -main ' + fun_name + ' -adnt ' + ' -adnt-fun ' + fun_name + '  -then -eva -eva-ignore-recursive-calls  > log_'+fun_name
        else:
            cmd = 'frama-c -load parsed.sav ' + ' -load-script add_anot.ml -main ' + fun_name + ' -adnt ' + ' -adnt-fun ' + fun_name + '  -then -eva -eva-equality-domain -eva-builtins-auto -slevel 200 -eva-ignore-recursive-calls  > log_' + fun_name
    # print cmd
    os.system(cmd)
    file_name = 'log_'+fun_name
    fp = open(file_name)  # Open file on read mode
    lines = fp.read().split("\n")  # Create a list containing all lines
    fp.close()
    excp_num = 0
    temp_i = ''
    res_val = []
    flag = 0
    for i in lines:
        if i.count('non-finite double value.') > 0:
            excp_num = excp_num + 1
        if i.count('Values at end of function '+fun_name)>0:
            flag=1
            # print res_val
        if (flag == 1)&(i.count('Values at end of function ')>0):
            flag == 0
        if (i.count('S_result') > 0)&(flag==1):
            # print temp_i
            try:
                res_val = analysis_res_str(temp_i)
            except ValueError:
                res_val = [0,1]
            flag = 0
        # if i.count('functions analyzed') > 0:
        #     print i.split()[-2]
        temp_i = i
    # print "number of exceptions"
    # print excp_num
    return excp_num,res_val