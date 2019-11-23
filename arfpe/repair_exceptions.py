import basic_func as bf
from plot_domain import plot_2vfunc_domain
from plot_domain import plot_1func_domain
import random
from math_lib import rfl
from mpmath import *
import numpy as np
import signal
from gen_drivfunc import load_pure_fun
import itertools
import time
# load localization res
mp.dps = 30
class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()

fid_lc = [2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 63, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]


signal.signal (signal.SIGALRM, handler)
NoConvergence = mp.NoConvergence
def rf_f(fid,inp):
    if type(inp) != list:
        inp = [inp]
    try:
        signal.alarm(1)
        resf = rfl[fid](*inp)
        # print "resf"
        # print resf
    except (TimeoutError, ValueError, ZeroDivisionError, TypeError, OverflowError,NoConvergence):
        resf = np.nan
    signal.alarm(0)
    return float(resf)

def load_local_res():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    for i in range(0, len(inter_funcs)):
        if i not in [62, 97, 104, 119]:
            test_fun = inter_funcs[i]
            name = "localize_res_files/" + test_fun[0] + ".pkl"
            try:
                temp_lst = bf.load_pickle(name)
                print test_fun
                # print len(temp_lst)
                # print len(temp_lst[0])
                print i
                for j in temp_lst[0]:
                    print len(j[3])
                    if len(j[3])>10:
                        for idj in j[3][0:10]:
                            print idj
                    else:
                        for idj in j[3]:
                            print idj
            except IOError:
                continue
def plot_local_res():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    for i in range(0, len(inter_funcs)):
        if i not in [62, 97, 104, 119]:
            test_fun = inter_funcs[i]
            var_num = bf.get_var_num(test_fun)
            name = "plot_bounds_res/" + test_fun[0] + ".pkl"
            name2 = "localize_res_files/" + test_fun[0] + ".pkl"
            try:
                print test_fun
                temp_lst = bf.load_pickle(name)
                temp_lst2 = bf.load_pickle(name2)
                if var_num == 1:
                    plot_1func_domain(temp_lst)
                else:
                    plot_2vfunc_domain(temp_lst)
            except IOError:
                continue

# patch generate
# input: local domain, program
# output: patch code

def get_random_points1v(bounds):
    points_lst = []
    for i in bounds:
        points = []
        for j in range(0,100):
            points.append(random.uniform(i[0],i[1]))
        points_lst.append(points)
    return points_lst
def extract_noempty_bound(bound):
    mp.dps = 30
    # bf.fpartition(bound)
    ret_lst = []
    if bound[0]==bound[1]:
        ret_lst.append(bound[0])
        return ret_lst
    if bound[0]==0:
        ret_lst.append(bf.f64min)
    else:
        ret_lst.append(bound[0] + bf.getulp(bound[0]))
    if bound[1] == 0:
        ret_lst.append(-bf.f64min)
    else:
        ret_lst.append(bound[1] - bf.getulp(bound[1]))
    fpart_bound = bf.fdistribution_partition(bound[0],bound[1])
    a = int(max(len(fpart_bound)/10.0,1))
    if a == 0:
        a = 1
    for i in range(0,len(fpart_bound),a):
        ret_lst.append(random.uniform(fpart_bound[i][0],fpart_bound[i][1]))
    return ret_lst

def get_testing_point(bound):
    points_lst = []
    bl = len(bound)
    for i in bound:
        if i == []:
            points_lst.append(bf.get_double_random())
        else:
            points_lst.append(extract_noempty_bound(i))
    ret_lst = []
    # for i in points_lst:
    #     print len(i)
    for element in itertools.product(*points_lst):
        ret_lst.append(list(element))
    return ret_lst

def isfloat(x):
    if isnan(x):
        return 0
    if isinf(x):
        return 0
    return 1

def classifer(res,fres,stat):
    if isfloat(fres):
        return 1
    else:
        if isinf(res):
            if isinf(fres):
                return 2
            else:
                return 3
        else:
            return 4

def classify_bound(bound,rff,pf,stat_fun):
    inp_lst = get_testing_point(bound)
    typ_i = 1
    # print len(inp_lst)
    for i in inp_lst:
        fres = float(rff(i))
        res = pf(*i)
        stat = stat_fun()
        temp_typ = classifer(res.val,fres,stat)
        if temp_typ > typ_i:
            typ_i = temp_typ
        # typ_i = typ_i * classifer(res.val,fres,stat)
    return typ_i

def poly_fun(polylst,x):
    a0 = polylst[0]
    temp_res = a0
    for i in polylst[1:]:
        temp_res = x*temp_res + i
    return temp_res

def evaluate_poly(polylst,bound,rfp):
    inp_lst = []
    for i in range(0,100):
        inp_lst.append(random.uniform(bound[0],bound[1]))
    max_err = 0
    pf = lambda x: poly_fun(polylst,x)
    for i in inp_lst:
        temp_err = bf.getUlpError(float(rfp([i])),pf(i))
        if temp_err > max_err:
            max_err = temp_err
    return temp_err


def poly2str(new_poly):
    polystr = repr(new_poly[0])
    print new_poly[1:]
    for i in new_poly[1:]:
        polystr = "(x*"+polystr+"+"+repr(i)+")"
    str1 = "result -> val = " + polystr + ";"
    str2 = "result -> err = 0;"
    str3 = "return GSL_SUCCESS;"
    return [str1,str2,str3]


def try_poly_approximation(rfp,bound):
    for i in range(0,10):
        polylst,err = chebyfit(rfp, bound, i+1, error=True)
        if err == 1:
            break
    fpoly = [float(i) for i in polylst]
    new_poly = []
    flag = 1
    for i in fpoly[0:-1]:
        if i!=0:
            new_poly.append(i)
    new_poly.append(fpoly[-1])
    err = evaluate_poly(new_poly,bound,rfp)
    if err == 1:
        return poly2str(new_poly)
    else:
        return ["DOMAIN_ERROR(result);"]


# flag 0 not need to repair 0 f
# flag 1 may need to repair 1 inf/nan f
# flag 2,3 overflow handle 2 inf inf 3 inf nan "OVERFLOW_ERROR(result);"
# flag 4 domain error handle 4 nan nan "DOMAIN_ERROR(result);"
def generate_1v_patch(bounds,ori_bound,code_type,rfp):
    # poinst_lst = get_random_points1v(bounds)
    repair_code_lst = []
    if code_type in [2,3]:
        repair_code_lst = ["OVERFLOW_ERROR(result);"]
    if code_type in [4]:
        repair_code_lst = ["DOMAIN_ERROR(result);"]
    if code_type in [1]:
        repair_code_lst = try_poly_approximation(rfp,bounds[0])
    return repair_code_lst
def generate_2v_patch(code_type):
    # poinst_lst = get_random_points1v(bounds)
    repair_code_lst = []
    if code_type in [1,2,3]:
        repair_code_lst = ["OVERFLOW_ERROR(result);"]
    if code_type in [4]:
        repair_code_lst = ["DOMAIN_ERROR(result);"]
    return repair_code_lst

def gen_patch():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    fid_lst = []
    for i in range(0, len(inter_funcs)):
        if i not in [62, 97, 104, 119]:
            test_fun = inter_funcs[i]
            var_num = bf.get_var_num(test_fun)
            name = "localize_res_files/" + test_fun[0] + ".pkl"
            try:
                temp_lst = bf.load_pickle(name)
                if var_num == 1:
                    for j in temp_lst[0]:
                        print len(j[3])
                        if len(j[3]) > 10:
                            for idj in j[3][0:10]:
                                print idj
                        else:
                            for idj in j[3]:
                                print idj
                    fid_lst.append(i)
            except IOError:
                continue
    print len(fid_lst)


def repair4all():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    for i in fid_lc:
        test_fun = inter_funcs[i]
        print test_fun
        var_num = bf.get_var_num(test_fun)
        name = "localize_res_files/" + test_fun[0] + ".pkl"
        name2 = "repair_res_files/" + test_fun[0] + ".pkl"
        rfp = lambda x: rf_f(i, x)
        fun_pu, stat_fun = load_pure_fun(test_fun[0])
        temp_lst = bf.load_pickle(name)
        st_time = time.time()
        repair_lst = []
        if var_num == 2:
            for j in temp_lst[0]:
                print j[0]
                print j[1]
                print len(j[-1])
                if len(j[-1])>=2:
                    repair_code = generate_2v_patch(4)
                    repair_lst.append([j[0], j[-1],repair_code])
                else:
                    typ_j = classify_bound(j[-1][0], rfp, fun_pu, stat_fun)
                    repair_code = generate_2v_patch(typ_j)
                    repair_lst.append([j[0], j[-1], repair_code])
        else:
            for j in temp_lst[0]:
                if len(j[-1]) >= 2:
                    repair_code = generate_2v_patch(4)
                    repair_lst.append([j[0], j[-1], repair_code])
                else:
                    typ_j = classify_bound(j[-1][0], rfp, fun_pu, stat_fun)
                    repair_code = generate_1v_patch(j[-1][0], j[0], typ_j, rfp)
                    print "repair_code"
                    print repair_code
                    repair_lst.append([j[0], j[-1], repair_code])
        et = time.time() - st_time
        repair_lst.append(et)
        bf.pickle_fun(name2,repair_lst)

repair4all()
def gen_patch1v():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    fid_lst = []
    for i in [1]:
        if i not in [62, 97, 104, 119]:
            test_fun = inter_funcs[i]
            print test_fun
            var_num = bf.get_var_num(test_fun)
            name = "localize_res_files/" + test_fun[0] + ".pkl"
            rfp = lambda x: rf_f(i, x)
            fun_pu, stat_fun = load_pure_fun(test_fun[0])
            temp_lst = bf.load_pickle(name)
            print len(temp_lst[-2][0])
            print len(temp_lst[0])
            print len(temp_lst[0][-1][-1])
            try:
                temp_lst = bf.load_pickle(name)
                if var_num == 2:
                    print temp_lst
                    # print test_fun
                    for j in temp_lst[0]:
                        ori_bound = j[0]
                        type = j[1]
                        print j[-1]
                        print classify_bound(j[-1][0],rfp,fun_pu,stat_fun)
                        print generate_1v_patch(j[-1], ori_bound, type, rfp)
                    #     print len(j[3])
                    #     if len(j[3]) > 10:
                    #         for idj in j[3][0:10]:
                    #             print idj
                    #     else:
                    #         for idj in j[3]:
                    #             print idj
                fid_lst.append(i)
            except IOError:
                continue
    print fid_lst
# gen_patch1v()
