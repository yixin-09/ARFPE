import basic_func as bf
import os
import sys
import ctypes
from subprocess import Popen, PIPE
from numpy.ctypeslib import ndpointer

src_path = '../benchmark/gsl-2.6/specfunc/'


def found_funbyName(fun_name, inter_funcs):
    for i in inter_funcs:
        if i[0] == fun_name:
            return i
    return []

def find_file4func(fun_name):
    # gsl_26_calls store depends analysis results produced by produce_call_dps function in proprecess
    calls_lst = bf.load_pickle('gsl_26_calls')
    file_list = []
    count = 0
    for i in calls_lst:
        if fun_name == i[0]:
            file_list = i[2]
            break
    return file_list[0]

def write2file(new_lines,file_name):
    f = open(file_name, 'w')
    orig_stdout = sys.stdout
    sys.stdout = f
    for i in new_lines:
        print i
    sys.stdout = orig_stdout
    f.close()


def gen_boudary_test_function_debug(test_fun):
    file_fun = find_file4func(test_fun[0])
    ### get the bitcode file
    bc_file = '.' + file_fun[0:-2] + '.o.bc'
    bc_file = '../../../gsl-bc-2.6/specfunc/bitcode/' + bc_file
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/boudary_analysis/'
    os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str = ''
    var_str_lst = []
    var_name = ''
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'double ' + 'gslfdr(' + var_str + '){'
    str11 = 'double ' + 'gslfdr(' + var_str + ');'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[2]
    str2 = '    double res_fun = ' + fun_name + '(' + var_name + ');'
    new_lines[10] = str1
    new_lines[12] = str2
    # change test.sh
    fp = open(test_driver_path + '/test.sh')
    linesbc = fp.read().split("\n")
    fp.close()
    new_linesbc = list(linesbc)
    strbc1 = 'llvm-link wTo1.bc ' + bc_file + ' gslsfdr.bc -o gslbc.bc'
    strbc2 = 'opt -load ../../../../llvm_passes/boundvalue/obj/boundvalue/libboundvalue.so -boundvalue -dr_fun "' + test_fun[0] + '" <gslbc.bc> gslbc2.bc'
    new_linesbc[7] = strbc1
    new_linesbc[8] = strbc2
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_linesbc, test_driver_path + '/test.sh')
    write2file([str11], test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/boudary_analysis/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)

def gen_boudary_test_function(test_fun):
    # file_fun = find_file4func(test_fun[0])
    ### get the bitcode file
    bc_file = '../../../gsl-bc-2.6/specfunc/bitcode/gslsflib.bc'
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/boundary_analysis/'
    # os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str_lst = []
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'double ' + 'gslfdr(' + var_str + '){'
    str11 = 'double ' + 'gslfdr(' + var_str + ');'
    str12 = 'void ini_idx();'
    str13 = 'void BoundaryAnalysis(int cnt, double *w, int *didx, double subs, int *stflag);'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[2]
    str2 = '    double res_fun = ' + fun_name + '(' + var_name + ');'
    new_lines[14] = str1
    new_lines[16] = str2
    # change test.sh
    fp = open(test_driver_path + '/test.sh')
    linesbc = fp.read().split("\n")
    fp.close()
    new_linesbc = list(linesbc)
    strbc1 = 'llvm-link ' + bc_file + ' gslsfdr.bc -o gslbc.bc'
    strbc2 = 'opt -load ../../../../llvm_passes/boundvalue/obj/boundvalue/libboundvalue.so -boundvalue -dr_fun "' + test_fun[0] + '" <gslbc.bc> gslbc2.bc'
    new_linesbc[7] = strbc1
    new_linesbc[8] = strbc2
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_linesbc, test_driver_path + '/test.sh')
    write2file([str11,str12,str13], test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/boundary_analysis/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)

def gen_overflow_test_function(test_fun):
    # file_fun = find_file4func(test_fun[0])
    ### get the bitcode file
    bc_file = '../../../gsl-bc-2.6/specfunc/bitcode/gslsflib.bc'
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/exception_detect/'
    # os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str = ''
    var_str_lst = []
    var_name = ''
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'double ' + 'gslfdr(' + var_str + '){'
    str11 = 'double ' + 'gslfdr(' + var_str + ');'
    str12 = 'void ini_idx();'
    str13 = 'void fpOverFlow(int cnt, double *w, int *didx, double lval, int *stflag);'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[2]
    str2 = '    double res_fun = ' + fun_name + '(' + var_name + ');'
    new_lines[14] = str1
    new_lines[16] = str2
    # change test.sh
    fp = open(test_driver_path + '/test.sh')
    linesbc = fp.read().split("\n")
    fp.close()
    new_linesbc = list(linesbc)
    strbc1 = 'llvm-link ' + bc_file + ' gslsfdr.bc -o gslbc.bc'
    strbc2 = 'opt -load ../../../../llvm_passes/excpetionDetector/overflow/obj/overflow/liboverflow.so -overflow -dr_fun "' + test_fun[0] + '" <gslbc.bc> gslbc2.bc'
    new_linesbc[7] = strbc1
    new_linesbc[8] = strbc2
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_linesbc, test_driver_path + '/test.sh')
    write2file([str11,str12,str13], test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/exception_detect/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)

def gen_underflow_test_function(test_fun):
    # file_fun = find_file4func(test_fun[0])
    ### get the bitcode file
    bc_file = '../../../gsl-bc-2.6/specfunc/bitcode/gslsflib.bc'
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/underflow_detect/'
    # os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str = ''
    var_str_lst = []
    var_name = ''
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'double ' + 'gslfdr(' + var_str + '){'
    str11 = 'double ' + 'gslfdr(' + var_str + ');'
    str12 = 'void ini_idx();'
    str13 = 'void fpUnderflow(int cnt, double *w, int *didx, double lval, int *stflag);'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[2]
    str2 = '    double res_fun = ' + fun_name + '(' + var_name + ');'
    new_lines[14] = str1
    new_lines[16] = str2
    # change test.sh
    fp = open(test_driver_path + '/test.sh')
    linesbc = fp.read().split("\n")
    fp.close()
    new_linesbc = list(linesbc)
    strbc1 = 'llvm-link ' + bc_file + ' gslsfdr.bc -o gslbc.bc'
    strbc2 = 'opt -load ../../../../llvm_passes/excpetionDetector/underflow/obj/underflow/libunderflow.so -Underflow -dr_fun "' + test_fun[0] + '" <gslbc.bc> gslbc2.bc'
    new_linesbc[7] = strbc1
    new_linesbc[8] = strbc2
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_linesbc, test_driver_path + '/test.sh')
    write2file([str11,str12,str13], test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/underflow_detect/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)


def gen_divzero_test_function(test_fun):
    # file_fun = find_file4func(test_fun[0])
    ### get the bitcode file
    bc_file = '../../../gsl-bc-2.6/specfunc/bitcode/gslsflib.bc'
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/div_zero/'
    # os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str = ''
    var_str_lst = []
    var_name = ''
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'double ' + 'gslfdr(' + var_str + '){'
    str11 = 'double ' + 'gslfdr(' + var_str + ');'
    str12 = 'void ini_idx();'
    str13 = 'void divzero(int cnt, double *w, int *didx, double lval, int *stflag);'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[2]
    str2 = '    double res_fun = ' + fun_name + '(' + var_name + ');'
    new_lines[14] = str1
    new_lines[16] = str2
    # change test.sh
    fp = open(test_driver_path + '/test.sh')
    linesbc = fp.read().split("\n")
    fp.close()
    new_linesbc = list(linesbc)
    strbc1 = 'llvm-link ' + bc_file + ' gslsfdr.bc -o gslbc.bc'
    strbc2 = 'opt -load ../../../../llvm_passes/excpetionDetector/dividezero/obj/dividezero/libdividezero.so -dividezero -dr_fun "' + test_fun[0] + '" <gslbc.bc> gslbc2.bc'
    new_linesbc[7] = strbc1
    new_linesbc[8] = strbc2
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_linesbc, test_driver_path + '/test.sh')
    write2file([str11,str12,str13], test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/div_zero/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)


def gen_fpnan_test_function(test_fun):
    # file_fun = find_file4func(test_fun[0])
    ### get the bitcode file
    bc_file = '../../../gsl-bc-2.6/specfunc/bitcode/gslsflib.bc'
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/nan_dect/'
    # os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str = ''
    var_str_lst = []
    var_name = ''
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'double ' + 'gslfdr(' + var_str + '){'
    str11 = 'double ' + 'gslfdr(' + var_str + ');'
    str12 = 'void ini_idx();'
    str13 = 'void fpnan(int cnt, double *w, int *didx, double arg1,double arg2,int fid, int *stflag);'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[2]
    str2 = '    double res_fun = ' + fun_name + '(' + var_name + ');'
    new_lines[14] = str1
    new_lines[16] = str2
    # change test.sh
    fp = open(test_driver_path + '/test.sh')
    linesbc = fp.read().split("\n")
    fp.close()
    new_linesbc = list(linesbc)
    strbc1 = 'llvm-link ' + bc_file + ' gslsfdr.bc -o gslbc.bc'
    strbc2 = 'opt -load ../../../../llvm_passes/excpetionDetector/fpnan/obj/fpnan/libfpnan.so -fpnan -dr_fun "' + test_fun[0] + '" <gslbc.bc> gslbc2.bc'
    new_linesbc[7] = strbc1
    new_linesbc[8] = strbc2
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_linesbc, test_driver_path + '/test.sh')
    write2file([str11,str12,str13], test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/nan_dect/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)


def gen_pure_test_function(test_fun):
    ### generate driver_funcs
    driver_path = '../benchmark/driver_funcs/pure_exe/'
    # os.system('rm -R ' + driver_path + test_fun[0])
    os.system('cp -R ' + driver_path + 'driver_template/. ' + driver_path + test_fun[0])
    test_driver_path = driver_path + test_fun[0]
    # change template of
    fp = open(test_driver_path + '/gslsfdr.c')
    lines = fp.read().split("\n")
    fp.close()
    new_lines = list(lines)
    var_str = " ".join(test_fun[1][0])
    var_name = test_fun[1][0][1]
    for i in test_fun[1][1:]:
        temp_str = " ".join(i)
        temp_var_name = i[1]
        var_str = var_str + ',' + temp_str
        var_name = var_name + ',' + temp_var_name
    var_str_lst = []
    var_name_lst = []
    for i in test_fun[1]:
        if i[0]=='double':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='int':
            var_str_lst.append(" ".join(i))
            var_name_lst.append(i[1])
        if i[0]=='gsl_mode_t':
            var_name_lst.append('0')
    var_str = ",".join(var_str_lst)
    var_name = ",".join(var_name_lst)
    str1 = 'gsl_sf_result ' + 'gslfdr(' + var_str + '){'
    str11 = 'gsl_sf_result ' + 'gslfdr(' + var_str + ');'
    # if test_fun[0].endswith('_e'):
    fun_name = test_fun[0]
    str2 = '    status = ' + fun_name + '(' + var_name + ',&result);'
    new_lines[13] = str1
    new_lines[17] = str2
    fp = open(test_driver_path + '/gslsfdr.h')
    lines = fp.read().split("\n")
    fp.close()
    new_lines2 = list(lines)
    new_lines2[7] = str11
    write2file(new_lines, test_driver_path + '/gslsfdr.c')
    write2file(new_lines2, test_driver_path + '/gslsfdr.h')
    pwd = os.getcwd()
    os.chdir('../benchmark/driver_funcs/pure_exe/' + test_fun[0])
    os.system('./test.sh')
    os.chdir(pwd)


def load_fun_debug(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/boudary_analysis/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    lib_idx = ctypes.c_int.in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = ctypes.c_double
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,[lib_w,lib_idx]

def load_fpbd_fun(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/boundary_analysis/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_ini = lib_ld.ini_idx
    lib_ini()
    lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    lib_cidx = ctypes.c_int.in_dll(lib_ld, "cidx")
    lib_stflag = ctypes.c_int.in_dll(lib_ld, "stflag")
    lib_sumins = ctypes.c_int.in_dll(lib_ld, "sum_ins")
    lib_idx = ctypes.POINTER(ctypes.c_int).in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = ctypes.c_double
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,[lib_w,lib_cidx,lib_idx,lib_stflag,lib_sumins]

def load_fpof_fun(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/exception_detect/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_ini = lib_ld.ini_idx
    lib_ini()
    lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    lib_cidx = ctypes.c_int.in_dll(lib_ld, "cidx")
    lib_stflag = ctypes.c_int.in_dll(lib_ld, "stflag")
    lib_sumins = ctypes.c_int.in_dll(lib_ld, "sum_ins")
    lib_idx = ctypes.POINTER(ctypes.c_int).in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = ctypes.c_double
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,[lib_w,lib_cidx,lib_idx,lib_stflag,lib_sumins]

def load_fpuf_fun(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/underflow_detect/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_ini = lib_ld.ini_idx
    lib_ini()
    lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    lib_cidx = ctypes.c_int.in_dll(lib_ld, "cidx")
    lib_stflag = ctypes.c_int.in_dll(lib_ld, "stflag")
    lib_sumins = ctypes.c_int.in_dll(lib_ld, "sum_ins")
    lib_idx = ctypes.POINTER(ctypes.c_int).in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = ctypes.c_double
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,[lib_w,lib_cidx,lib_idx,lib_stflag,lib_sumins]


def load_fpdz_fun(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/div_zero/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_ini = lib_ld.ini_idx
    lib_ini()
    lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    lib_cidx = ctypes.c_int.in_dll(lib_ld, "cidx")
    lib_stflag = ctypes.c_int.in_dll(lib_ld, "stflag")
    lib_sumins = ctypes.c_int.in_dll(lib_ld, "sum_ins")
    lib_idx = ctypes.POINTER(ctypes.c_int).in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = ctypes.c_double
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,[lib_w,lib_cidx,lib_idx,lib_stflag,lib_sumins]
def load_fpnan_fun(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/nan_dect/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_ini = lib_ld.ini_idx
    lib_ini()
    lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    lib_cidx = ctypes.c_int.in_dll(lib_ld, "cidx")
    lib_stflag = ctypes.c_int.in_dll(lib_ld, "stflag")
    lib_sumins = ctypes.c_int.in_dll(lib_ld, "sum_ins")
    lib_idx = ctypes.POINTER(ctypes.c_int).in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = ctypes.c_double
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,[lib_w,lib_cidx,lib_idx,lib_stflag,lib_sumins]

def load_pure_fun(fun_name):
    inter_funcs = bf.load_pickle('fun_index.pkl')
    ### [fun_name, [[var_typ,var_name]..]]
    test_fun = found_funbyName(fun_name, inter_funcs)
    # print os.path.dirname(__file__)
    lib_ld = ctypes.CDLL('../benchmark/driver_funcs/pure_exe/' + test_fun[0] + '/libgslbc.so')
    lib_fun = lib_ld.gslfdr
    lib_stat = lib_ld.get_status
    class gsl_sf_result(ctypes.Structure):
        _fields_ = [('val', ctypes.c_double),
                    ('err', ctypes.c_double)]
    # lib_idx = ctypes.POINTER(ctypes.c_int).in_dll(lib_ld, "idx")
    lib_ld.gslfdr.restype = gsl_sf_result
    lib_ld.get_status.restype = ctypes.c_int
    vartyp_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            vartyp_lst.append(ctypes.c_double)
        if i[0] == 'int':
            vartyp_lst.append(ctypes.c_int)
    lib_ld.gslfdr.argtypes = vartyp_lst
    return lib_fun,lib_stat


# generate boudary test fun for all interface function
def gen_boudary_test4allfuncs():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    count = 0
    for i in inter_funcs:
        print i
        print count
        count = count + 1
        # gen_boudary_test_function(i)
        # gen_divzero_test_function(i)
        gen_pure_test_function(i)
        # gen_overflow_test_function(i)
        # gen_underflow_test_function(i)
        # gen_fpnan_test_function(i)

if __name__ == "__main__":
    gen_boudary_test4allfuncs()
    # lib_ld = ctypes.CDLL('../benchmark/driver_funcs/exception_detect/libgslbc.so')
    # out = Popen(
    #     args="nm ../benchmark/driver_funcs/exception_detect/libgslbc.so",
    #     shell=True,
    #     stdout=PIPE
    # ).communicate()[0].decode("utf-8")
    #
    # attrs = [
    #     i.split(" ")[-1].replace("\r", "")
    #     for i in out.split("\n") if " T " in i
    # ]
    # lib_idx = ctypes.c_int.in_dll(lib_ld, "idx")
    # lib_w = ctypes.c_double.in_dll(lib_ld, "w")
    # functions = [i for i in attrs if hasattr(ctypes.CDLL("../benchmark/driver_funcs/exception_detect/libgslbc.so"), i)]
    # close_fun = lib_ld.gslfdr
    # airy_fun = lib_ld.gsl_sf_debye_3
    # airy_fun.restype = ctypes.c_double
    # airy_fun.argtypes = [ctypes.c_double]
    # close_fun()
    # print airy_fun(-4.0)
    # print lib_idx
    # print lib_w
    # print(functions)
    # print len(functions)
