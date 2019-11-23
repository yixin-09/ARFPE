import basic_func as bf
from plot_domain import plot_2vfunc_domain
from plot_domain import plot_1func_domain
import random
from math_lib import rfl
from mpmath import *
import numpy as np
import signal
from gen_drivfunc import load_pure_fun
# load localization res
mp.dps = 30
class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()

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
    return resf

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
print get_random_points1v([[0,10]])


def try_poly_approximation(rfp,bound):
    for i in range(0,10):
        poly,err = chebyfit(rfp, bound, i+1, error=True)
        if err == 0:
            break
    return poly


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
        for j in bounds[0]:
            print j[0]
            print j
            print rfp(j[0])
            print rfp(j[1])
            repair_code_lst.append(try_poly_approximation(rfp,j))
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

fid_lc = [1, 2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]


def gen_patch1v():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    fid_lst = []
    for i in fid_lc:
        if i not in [62, 97, 104, 119]:
            test_fun = inter_funcs[i]
            print test_fun
            var_num = bf.get_var_num(test_fun)
            name = "localize_res_files/" + test_fun[0] + ".pkl"
            rfp = lambda x: rf_f(i, x)
            temp_lst = bf.load_pickle(name)
            print len(temp_lst[-2][0])
            print len(temp_lst[0])
            print len(temp_lst[0][-1][-1])
            try:
                temp_lst = bf.load_pickle(name)
                if var_num == 1:
                    print temp_lst
                    # print test_fun
                    for j in temp_lst[0]:
                        ori_bound = j[0]
                        type = j[1]
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
gen_patch1v()
# inter_funcs = bf.load_pickle('fun_index.pkl')
# test_fun = inter_funcs[63]
# fun_pu, stat_fun = load_pure_fun(test_fun[0])
# res = fun_pu(-3,13)
# print res.val
# print stat_fun()
# test_fun = inter_funcs[12]
# fun_pu, stat_fun = load_pure_fun(test_fun[0])
# res = fun_pu(0)
# print res.val
# print stat_fun()
# print log(1.0)
# def under_flow_res():
#     inter_funcs = bf.load_pickle('fun_index.pkl')
#     sum_lst = bf.load_pickle("detect_res_lst.pkl")
#     fid_lst = []
#     flow_num = 0
#     for i in range(0, len(inter_funcs)):
#         if i not in [62, 97, 104, 119]:
#             test_fun = inter_funcs[i]
#             fun_pu, stat_fun = load_pure_fun(test_fun[0])
#             var_num = bf.get_var_num(test_fun)
#             name = "underflow_res_files/" + test_fun[0] + ".pkl"
#             rf = lambda x: rf_f(i, x)
#             try:
#                 temp_lst = bf.load_pickle(name)
#                 print temp_lst
#                 print temp_lst[1]
#                 for j in range(0,len(temp_lst[1][2]),2):
#                     temp_j_id = temp_lst[1][2][j]
#                     # if temp_j_id in [3]:
#                     temp_j = temp_lst[1][2][j+1]
#                     for tj in temp_j:
#                         flow_num = flow_num + len(tj)
#                         for ij in tj:
#                             print ij
#                             res = fun_pu(*ij)
#                             print res.val
#                             print stat_fun()
#                         if len(tj)!=0:
#                             fid_lst.append(i)
#             except IOError:
#                 continue
#     print bf.rm_dump_lst(fid_lst)
#     print len(bf.rm_dump_lst(fid_lst))
#     print flow_num
# gen_patch1v()
# test_fid = [1, 2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]
# for i in test_fid:
#     test_fun = inter_funcs[i]
#     print test_fun
# print len(test_fid)
# gen_patch()