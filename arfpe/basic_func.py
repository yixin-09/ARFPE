import pickle
import xlrd
import os
import itertools
import numpy as np
import sys
import struct
from mpmath import *
import random
import math
# from gen_drivfunc import load_pure_fun
def floatToRawLongBits(value):
	return struct.unpack('Q', struct.pack('d', value))[0]

def longBitsToFloat(bits):
	return struct.unpack('d', struct.pack('Q', bits))[0]


f64max = sys.float_info.max
f64min = sys.float_info.min
# print f64max - 1.7976931348623157e+308
# print f64max-1.7976931348623157e+308
def getulp(x):
    x = float(x)
    k = frexp(x)[1]-1
    if x == 0.0:
        return pow(2,-1074)
    if (k<=1023)&(k>-1022):
        return pow(2.0,k-52)
    else:
        return pow(2.0,-1074)
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

def pickle_fun(file_name,l):
    with open(file_name, "wb") as fp:
        pickle.dump(l, fp)

def load_pickle(file_name):
    return pickle.load(open(file_name, "rb"))

def get_var_num(test_fun):
    count = 0
    for i in test_fun[1]:
        if i[0] == 'double':
            count = count + 1
    return count
# funs_to_w2xls(new_name_lst,"fun_index")
def search_line_num4f_ori(fun_name,exname):
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
    file_name = pwd+'/benchmark/gsl-2.6/specfunc/' + file_name
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


def search_line_num4f(fun_name,file_name):
    ori_file_name = file_name
    pwd1 = os.getcwd()
    os.chdir("..")
    pwd = os.getcwd()
    file_name = pwd+'/benchmark/gsl-2.6/specfunc/' + file_name
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

# partition the input domain according to floating-point distribution
def fdistribution_partition(in_min, in_max):
    tmp_l = []
    a = np.frexp(in_min)
    b = np.frexp(in_max)
    tmp_j = 0
    if (in_min < 0)&(in_max > 0):
        if in_min >= -1.0:
            tmp_l.append([in_min, 0])
        else:
            for i in range(1, a[1]+1):
                tmp_i = np.ldexp(-0.5, i)
                tmp_l.append([tmp_i, tmp_j])
                tmp_j = tmp_i
            if in_min != tmp_j:
                tmp_l.append([in_min, tmp_j])
        tmp_j = 0
        if in_max <= 1.0:
            tmp_l.append([0, in_max])
        else:
            for i in range(1, b[1]+1):
                tmp_i = np.ldexp(0.5, i)
                tmp_l.append([tmp_j, tmp_i])
                tmp_j = tmp_i
            if in_max != tmp_j:
                tmp_l.append([tmp_j, in_max])
    if (in_min < 0) & (0 >= in_max):
        if in_min >= -1:
            tmp_l.append([in_min, in_max])
            return tmp_l
        else:
            if in_max > -1:
                tmp_l.append([-1, in_max])
                tmp_j = -1.0
                for i in range(2, a[1] + 1):
                    tmp_i = np.ldexp(-0.5, i)
                    tmp_l.append([tmp_i, tmp_j])
                    tmp_j = tmp_i
                if in_min != tmp_j:
                    tmp_l.append([in_min, tmp_j])
            else:
                if a[1] == b[1]:
                    tmp_l.append([in_min, in_max])
                    return tmp_l
                else:
                    tmp_j = np.ldexp(-0.5, b[1]+1)
                    tmp_l.append([tmp_j, in_max])
                    if tmp_j != in_min:
                        for i in range(b[1]+2, a[1]+1):
                            tmp_i = np.ldexp(-0.5, i)
                            tmp_l.append([tmp_i, tmp_j])
                            tmp_j = tmp_i
                        if in_min != tmp_j:
                            tmp_l.append([in_min, tmp_j])
    if (in_min >= 0) & (in_max > 0):
        if in_max <= 1:
            tmp_l.append([in_min, in_max])
            return tmp_l
        else:
            if in_min < 1:
                tmp_l.append([in_min, 1])
                tmp_j = 1.0
                for i in range(2, b[1] + 1):
                    tmp_i = np.ldexp(0.5, i)
                    tmp_l.append([tmp_j, tmp_i])
                    tmp_j = tmp_i
                if in_max != tmp_j:
                    tmp_l.append([tmp_j, in_max])
            else:
                if a[1] == b[1]:
                    tmp_l.append([in_min, in_max])
                    return tmp_l
                else:
                    tmp_j = np.ldexp(0.5, a[1]+1)
                    tmp_l.append([in_min, tmp_j])
                    if tmp_j != in_max:
                        for i in range(a[1]+2, b[1]+1):
                            tmp_i = np.ldexp(0.5, i)
                            tmp_l.append([tmp_j, tmp_i])
                            tmp_j = tmp_i
                        if in_max != tmp_j:
                            tmp_l.append([tmp_j, in_max])
    return tmp_l
def fpartition(input_domain):
    l_var = []
    for i in input_domain:
        for j in i:
            tmp_l = fdistribution_partition(j[0], j[1])
            l_var.append(tmp_l)
    ini_confs = []
    for element in itertools.product(*l_var):
        temp_ele = []
        for i in list(element):
            temp_ele.append(tuple(i))
        ini_confs.append(temp_ele)
    return ini_confs

# return a list of double value
# sign -1,1
# exponent -1024, 1023 0-2047
# significand 1 to 2
def get_double_random():
    rand_inps = []
    lst_a = [9]
    for i in range(-1024,1023,256)+lst_a:
        sigcand = random.uniform(1.0,2.0)
        expt = np.power(2.0,i)
        rand_inps.append(sigcand*expt)
    # exp_lst = [0.0,np.pi,2*np.pi,1,2,np.pi/2.0,np.e,f64min,f64min*2.0,1.0/1.3407807929942596e+154,2.2250738585072014e-308]
    exp_lst = [0.0,np.pi,f64min,f64min*2.0,2.2250738585072014e-308]
    rand_inps = rand_inps + exp_lst
    sign_rand_inps = [x*-1 for x in rand_inps]
    sign_rand_inps.reverse()
    return sign_rand_inps+rand_inps

# print len(get_double_random())
def get_double_random_small():
    rand_inps = []
    lst_a = range(-9,9)
    for i in range(-60,30,16)+lst_a:
        sigcand = random.uniform(1.0,2.0)
        expt = np.power(2.0,i)
        rand_inps.append(sigcand*expt)
    exp_lst = [0.0,np.pi,2*np.pi,1,2,np.pi/2.0,np.e,1.0/1.3407807929942596e+154,2.2250738585072014e-308]
    rand_inps = rand_inps + exp_lst
    sign_rand_inps = [x*-1 for x in rand_inps]
    sign_rand_inps.reverse()
    return sign_rand_inps+rand_inps


def analysis_res_str(str):
    str1 = str.split('{')
    str2 = str1[-1].strip("}")
    str3 = str2.split(';')
    res_lst = []
    for i in str3:
        res_lst.append(int(i))
    return res_lst

def creat_bound_lst(bound):
    bounds_lst = []
    for i in bound:
        temp_bounds = []
        if i != []:
            temp_bounds.append([-f64max, i[0]])
            temp_j = i[0]
            if len(i) > 1:
                for j in i[1:]:
                    temp_bounds.append([temp_j, j])
                    temp_j = j
            temp_bounds.append([i[-1], f64max])
        else:
            temp_bounds.append([-f64max,f64max])
        temp_bounds0 = temp_bounds + []
        for i in temp_bounds0:
            if i[0] == i[1]:
                temp_bounds.remove(i)
        bounds_lst.append(temp_bounds)
    mix_bounds_lst = []
    for element in itertools.product(*bounds_lst):
        mix_bounds_lst.append(list(element))
    return mix_bounds_lst

def find_mid_val(val_l):
    b0 = val_l[0]
    b1 = val_l[-1]
    mp.dps = 40
    temp_val = val_l[1]
    temp_sub_dis = fsub(b1,b0,exact=True)
    count = 0
    idx = 0
    for i in val_l[1:-2]:
        dis0 = fsub(i,b0,exact=True)
        dis1 = fsub(b1,i,exact=True)
        sub_dis = fabs(fsub(dis0,dis1,exact=True))
        # print "dis"
        # print i
        # print dis0
        # print dis1
        # print sub_dis
        if sub_dis < temp_sub_dis:
            temp_val = i
            idx = count
            temp_sub_dis = sub_dis
        count = count + 1
    return temp_val,sub_dis,idx
# [[-0.0, 1.4916681462400413e-154, 1.0], [-5.928530882240775, -0.1, -0.0, 1.4916681462400413e-154], [6.283185307179586, 6.284073485599286, 11.45993140869097, 17.11015528246687, 26.515534971672018]]
# print find_mid_val([6.283185307179586, 6.284073485599286, 11.45993140869097, 17.11015528246687, 26.515534971672018])
# print find_mid_val([1,2,3,4,5],0,10)

def find_largest_val(val_l,n):
    b0 = val_l[0]
    b1 = val_l[1]
    new_val_l = []
    temp_j,sub_dis,idx = find_mid_val(val_l)
    for i in range(1,n):
        return 0


def reduce_bounds(bound):
    count = 1.0
    new_bound = []
    for i in bound:
        count = count*(len(i)+1)
    if count > 24:
        max_len = 24/len(bound)
        for i in bound:
            if (len(i)+1)>max_len:
                return 0
            else:
                new_bound.append(i)

    else:
        return bound

def reduce_bounds(bound):
    count = 1.0
    new_bound = []
    for i in bound:
        count = count * (len(i) + 1)
    if count > 81:
        if len(bound)==4:
            for i in bound:
                if len(i)>2:
                    new_bound.append([i[0],i[-1]])
                else:
                    new_bound.append(i)
        if len(bound) in [1,2,3]:
            for i in bound:
                if len(i) > 3:
                    temp_j, sub_dis, idx = find_mid_val(i)
                    new_bound.append([i[0],temp_j, i[-1]])
                else:
                    new_bound.append(i)
        return new_bound
    else:
        return bound

# bound_lst = [[-20.0, -10.0, 10.0, 20.0], [-20.38165821125173, -20.0, -0.04536301826722435, 2.718281828459045, 3.4962049445872942, 10.0, 27.719858896202116], [-2.472986313903353, -2.3897645485182246, -2.220446049250313e-13, -1.0009872950116272e-13, -0.0, 2.3897645485182246, 2.3902086377280747, 3.141592653589793, 3.8552684724759256, 23.70921542181057, 42.270899439515965], [-1203576.3838545945, -1203343.5532109407, -0.5567647565435773, -0.36082055745084624, -0.25, -0.24994448884876874, 0.0, 0.0004763409059899055, 1.0]]
# print len(creat_bound_lst(bound_lst))
# print reduce_bounds(bound_lst)
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


def boundary_test(fun_name,boud_str,var_num):
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
def rm_duplicates(seq, idfun=None):
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result


def mp_bdary_fun(fun_exe,inp,x,idx):
    inp[idx]=float(x)
    return mpf(fun_exe(inp))
def simple_bdary_fun(fun_exe,inp,x,idx):
    inp[idx]=float(x)
    return fun_exe(*inp)

def simple_root_search(fun_exe,inp,bdary_lst):
    temp_inp = list(inp)
    temp_res = 0.0
    for i in range(0, len(inp)):
        mp_test_fun = lambda a: simple_bdary_fun(fun_exe, list(temp_inp), float(a), i)
        res_inp = mp_test_fun(0)
        if (mp_test_fun(res_inp) == 0):
            temp_inp[i] = res_inp
            return temp_inp
        if (mp_test_fun(-res_inp) == 0):
            temp_inp[i] = -res_inp
            return temp_inp
        if mp_test_fun(0) == 1:
            temp_res = mp_test_fun(temp_inp[i])
            # ulp_s = getulp(temp_inp[i]-temp_res)
            ulp_s = 0
            if (mp_test_fun(temp_inp[i]-temp_res - ulp_s)== -ulp_s)|(mp_test_fun(temp_inp[i]-temp_res + ulp_s)==ulp_s):
                res_inp = temp_inp[i]-temp_res
                if res_inp not in bdary_lst[i]:
                    temp_inp[i] = res_inp
                    return temp_inp
            else:
                if temp_inp[i]-temp_res == 0:
                    small_inp_pos = 2.2250738585072014e-308
                    temp_res_pos = mp_test_fun(small_inp_pos)
                    if mp_test_fun(small_inp_pos-temp_res_pos)==0:
                        res_inp = small_inp_pos-temp_res_pos
                        temp_inp[i] = res_inp
                        return temp_inp
                    if mp_test_fun(small_inp_pos+temp_res_pos)==0:
                        res_inp = small_inp_pos+temp_res_pos
                        temp_inp[i] = res_inp
                        return temp_inp
                    small_inp_neg = -2.2250738585072014e-308
                    temp_res_neg = mp_test_fun(small_inp_neg)
                    if mp_test_fun(small_inp_neg-temp_res_neg)==0:
                        res_inp = small_inp_pos-temp_res_pos
                        temp_inp[i] = res_inp
                        return temp_inp
                    if mp_test_fun(small_inp_neg+temp_res_neg)==0:
                        res_inp = small_inp_pos-temp_res_pos
                        temp_inp[i] = res_inp
                        return temp_inp
                else:
                    res_inp_temp = temp_inp[i]-temp_res - mp_test_fun(temp_inp[i]-temp_res)
                    if mp_test_fun(res_inp_temp-mp_test_fun(res_inp_temp))==0:
                        res_inp = res_inp_temp-mp_test_fun(res_inp_temp)
                        temp_inp[i] = res_inp
                        return temp_inp
    return []



def try_rootFind(fun_exe, inp):
    mp.dps = 200
    temp_inp = list(inp)
    for i in range(0,len(inp)):
        mp_test_fun = lambda a: mp_bdary_fun(fun_exe, temp_inp, a, i)
        temp_i = float(temp_inp[i])+0.0
        # res = findroot(mp_test_fun, temp_i,tol=0.0)
        try:
            res = findroot(mp_test_fun,temp_i,tol=0.0,solver='anewton')
            if mp_test_fun(res) == 0:
                inp[i] = float(res)
                return list(inp)
        except (UnboundLocalError,ValueError,ZeroDivisionError):
            try:
                res = findroot(mp_test_fun, [temp_i - getulp(temp_i) * 4e15, temp_i + getulp(temp_i) * 4e15], tol=0.0,
                               solver='anderson')
                if mp_test_fun(res) == 0:
                    inp[i] = float(res)
                    return inp
            except (UnboundLocalError, ValueError, ZeroDivisionError):
                return []
    return []


# reduce input into the bound
def reduce_x(bound_l,xl):
    try:
        xl = list(xl)
    except TypeError:
        xl = [xl]
    new_x = []
    for i,j in zip(bound_l,xl):
        j = float(j)
        if j > f64max:
            j = f64max
        if j < -f64max:
            j = -f64max
        new_x.append((i[0]/2.0+i[1]/2.0)+(i[1]/2.0-i[0]/2.0)*math.sin(j))
    return tuple(new_x)

def generate_x(bound_l,xl):
    xl = list(xl)
    new_x = []
    for i,j in zip(bound_l,xl):
        temp = j/(i[1]/2.0-i[0]/2.0) - (i[0]/2.0+i[1]/2.0)/(i[1]/2.0-i[0]/2.0)
        if temp<0:
            temp = np.max([-1,temp])
        else:
            temp = np.min([1,temp])
        new_x.append(float(asin(temp)))
    return tuple(new_x)

# 64-bit floating-point -> sign*pow(2,exponent)*matissia
def double_divede(x):
    if math.isnan(x):
        return 1,2047,2.0
    val = np.fabs(x)
    valint = floatToRawLongBits(val)
    # val = valint<<1
    if x<0:
        sign = -1
    else:
        sign = 1
    exponent = (valint>>52)
    significant =val/pow(2.0,exponent-1023)
    return sign,exponent,significant

def getUlpError(a,b):
    try:
        ia = floatToRawLongBits(np.abs(a))
        ib = floatToRawLongBits(np.abs(b))
        zo = floatToRawLongBits(0)
        if sign(a)!=sign(b):
            res = abs(ib-zo)+abs(ia-zo)
        else:
            res = abs(ib-ia)
        return int(res+1)
    except (ValueError, ZeroDivisionError, OverflowError, Warning,TypeError):
        return 1.0
# print getUlpError(0,0)
def div_to_fp(s,e,m):
    return s*pow(2.0,e-1023)*m

def get_next_point(point,step,sign):
    if point>0:
        fint = floatToRawLongBits(point)
        stint = int(step)
        if stint > fint:
            if sign == -1:
                return -longBitsToFloat(stint-fint)
        return longBitsToFloat(fint + sign*stint)
    else:
        fint = floatToRawLongBits(fabs(point))
        stint = int(step)
        if stint > fint:
            if sign == 1:
                return longBitsToFloat(stint-fint)
        return -longBitsToFloat(fint - sign * stint)
# print get_next_point(1.52912469728e+308,1.44115188076e+19,-1)
# print float(getUlpError(get_next_point(1.52912469728e+308,1.44115188076e+19,-1),1.52912469728e+308))
# print get_next_point(-1.0,5.14115188076e+18,1)
# print float(getUlpError(get_next_point(-1.0,1.14115188076e+18,1),-1.0))
# print float(floatToRawLongBits(get_next_point(-1.0,1.44115188076e+19,1)))
# print np.log2(getUlpError(-1,1))
# print floatToRawLongBits(0)
# print float(getUlpError(f64max,-f64max))
# print float(getUlpError(-1,0))
# print float(floatToRawLongBits(1.52912469728e+308))
# print float(floatToRawLongBits(-f64max))
# print float(floatToRawLongBits(f64max))
# print float(floatToRawLongBits(-1))


def rm_dump_lst(lst):
    temp_lst = []
    count = 0
    for i in lst:
        if i not in lst[count+1:]:
            temp_lst.append(i)
        count = count + 1
    return temp_lst

def fp_to_bound(x):
    s,e,m = double_divede(x)
    e = e - 1023
    if m == 0:
        mat = 0
    else:
        mat = 1
    if s == -1:
        up_bound = s*pow(2.0,e)*1.0
        if e == 1023:
            dw_bound = -f64max
        else:
            dw_bound = s*pow(2.0,e+1)*mat
    else:
        if e == 1023:
            up_bound = f64max
        else:
            up_bound = s*pow(2.0,e+1)*mat
        dw_bound = s*pow(2.0,e)*mat
    return [dw_bound,up_bound]

def bound_fpDiv(bound):
    b0 = bound[0]
    b1 = bound[1]
    s0,e0,m0 = double_divede(b0)
    s1,e1,m1 = double_divede(b1)
    if (e0 == e1)&(s0==s1):
        return [bound]
    bounds_lst = []
    temp_bds = []
    if b0*b1<0:
        temp_bds = []
        fpb0 = fp_to_bound(b0)
        if b0 < fpb0[1]:
            temp_bds.append([b0,fpb0[1]])
        if e0 != 0:
            temp_b0 = fpb0[1]
            for i in range(0,e0-1):
                temp_b1 = div_to_fp(s0, e0-i-1, 1.0)
                temp_bds.append([temp_b0,temp_b1])
                temp_b0 = temp_b1
            temp_bds.append([temp_b0, 0.0])
            temp_b0 = 0.0
            for i in range(0,e1):
                temp_b1 = div_to_fp(s1,i+1,1.0)
                temp_bds.append([temp_b0, temp_b1])
                temp_b0 = temp_b1
            if b1 > temp_b0:
                temp_bds.append([temp_b0, b1])
    if b0*b1>0:
        temp_bds = []
        if b0 > 0:
            fpb0 = fp_to_bound(b0)
            if b0 < fpb0[1]:
                temp_bds.append([b0,fpb0[1]])
            temp_b0 = fpb0[1]
            for i in range(e0+1,e1):
                temp_b1 = div_to_fp(s0, i+1, 1.0)
                temp_bds.append([temp_b0,temp_b1])
                temp_b0 = temp_b1
            if b1 > temp_b0:
                temp_bds.append([temp_b0, b1])
        if b0 < 0:
            fpb0 = fp_to_bound(b0)
            if b0 < fpb0[1]:
                temp_bds.append([b0,fpb0[1]])
            temp_b0 = fpb0[1]
            for i in range(1,e0-e1):
                temp_b1 = div_to_fp(s0, e0-i, 1.0)
                temp_bds.append([temp_b0,temp_b1])
                temp_b0 = temp_b1
            if b1 > temp_b0:
                temp_bds.append([temp_b0, b1])
    if b0 * b1 == 0:
        if b0 == 0:
            fpb0 = fp_to_bound(b0)
            if b0 < fpb0[1]:
                temp_bds.append([b0, fpb0[1]])
            temp_b0 = fpb0[1]
            for i in range(e0 + 1, e1):
                temp_b1 = div_to_fp(s0, i + 1, 1.0)
                temp_bds.append([temp_b0, temp_b1])
                temp_b0 = temp_b1
            if b1 > temp_b0:
                temp_bds.append([temp_b0, b1])
        else:
            fpb0 = fp_to_bound(b0)
            if b0 < fpb0[1]:
                temp_bds.append([b0, fpb0[1]])
            temp_b0 = fpb0[1]
            for i in range(1, e0 - e1):
                temp_b1 = div_to_fp(s0, e0 - i, 1.0)
                temp_bds.append([temp_b0, temp_b1])
                temp_b0 = temp_b1
            if b1 > temp_b0:
                temp_bds.append([temp_b0, b1])
    return temp_bds

# print fp_to_bound(-1.56169917611e+308)
# print bound_fpDiv([0.3,1.7])