import basic_func as bf
from gen_drivfunc import *
from fpexception_detection import FPexcption_detector_whole
from fpexception_detection import get_testing_point
from math_lib import rfl
from plot_domain import plot_2vfunc_domain
from plot_domain import plot_1func_domain
from mpmath import *
import itertools
import numpy as np
import random
import signal
class TimeoutError (RuntimeError):
    pass

def handler(signum, frame):
    raise TimeoutError()

signal.signal(signal.SIGALRM, handler)

def get_bound_type(ret_vals,num_excp):
    if 0 not in ret_vals:
        bound_type = 2
    else:
        if len(ret_vals) == 1:
            if num_excp == 0:
                bound_type = 1
            else:
                bound_type = 3
        else:
            if num_excp == 0:
                bound_type = 4
            else:
                bound_type = 3
    return bound_type

NoConvergence = mp.NoConvergence
def rf_f(fid,inp):
    try:
        signal.alarm(1)
        resf = re(rfl[fid](*inp))
    except (TimeoutError, ValueError, ZeroDivisionError, TypeError, OverflowError,NoConvergence):
        resf = np.nan
    signal.alarm(0)
    return resf

def isfloat(x):
    if isnan(x):
        return 0
    if isinf(x):
        return 0
    return 1

# flag 0 not need to repair 0 f
# flag 1 may need to repair 1 inf/nan f
# flag 2,3 overflow handle 2 inf inf 3 inf nan
# flag 4 domain error handle 4 nan nan
def classifer(res,fres,stat):
    flag = 0
    if stat != 0:
        return flag
    if isfloat(res):
        return flag
    else:
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




def point_in_bound(point,bound):
    flag = 1
    for i,j in zip(point,bound):
        if (i<=j[1])&(i>=j[0]):
            flag = 1*flag
        else:
            flag = 0*flag
    return flag

def get_random_points(bound):
    n = 4
    ps_lst = []
    for i in bound:
        points = []
        print i
        for j in range(0,n):
             points.append(random.uniform(i[0],i[1]))
        ps_lst.append(points)
    ret_lst = []
    # for i in points_lst:
    #     print len(i)
    for element in itertools.product(*ps_lst):
        ret_lst.append(list(element))
    return ret_lst

def random_bound_test(bound,fun_pu):
    points = get_random_points(bound)
    flag = 1
    for i in points:
        res = fun_pu(*i)
        if isfloat(res.val):
            return 0
    return flag


def accuracy_bound_search_lb(ubp,lbp,test_fun,mid_p,idx):
    for i in range(0, 2000):
        mid_i = float(fadd(lbp, fsub(ubp, lbp) / 2.0))
        mid_p[idx] = mid_i
        res = test_fun(*mid_p)
        if isfloat(res.val):
            lbp = mid_i
        else:
            ubp = mid_i
        dis_lu = bf.getUlpError(lbp, ubp)
        # print dis_lu
        if dis_lu <= 2:
            break
    return lbp

def accuracy_bound_search_ub(ubp,lbp,test_fun,mid_p,idx):
    for i in range(0, 2000):
        mid_i = float(fadd(lbp, fsub(ubp, lbp) / 2.0))
        mid_p[idx] = mid_i
        res = test_fun(*mid_p)
        if isfloat(res.val):
            ubp = mid_i
        else:
            lbp = mid_i
        dis_lu = bf.getUlpError(lbp, ubp)
        # print dis_lu
        if dis_lu <= 2:
            break
    return ubp

def binary_find_bound(sinp,bound,inp,test_fun,idx):
    mid_p = list(inp)
    # print "binary_find_bound"
    # print sinp
    # print bound
    lbp = bound[0]
    ubp = sinp
    max_step = bf.getUlpError(sinp,bound[0])
    ini_step = np.min([40,max_step])
    st_p = sinp + 0
    temp_p = sinp
    for i in range(0,2000):
        # print "hello"
        # print sinp
        # print st_p
        # print ini_step
        # print float(max_step)
        # print bound[0]
        if ini_step >= max_step:
            lbp = accuracy_bound_search_lb(temp_p, bound[0], test_fun, list(inp), idx)
            break
        st_p = bf.get_next_point(sinp,ini_step,-1)
        mid_p[idx] = st_p
        if st_p < bound[0]:
            lbp = bound[0]
            break
        res = test_fun(*mid_p)
        # print res.val
        if not isfloat(res.val):
            ini_step = ini_step * 2.0
        else:
            lbp = accuracy_bound_search_lb(temp_p,st_p,test_fun,list(inp),idx)
            break
        temp_p = st_p
        # dis_lu = bf.getUlpError(lbp,ubp)
        # if dis_lu <= 2:
        #     break
    fl_lbp = lbp
    lbp = sinp
    ubp = bound[1]
    max_step = bf.getUlpError(sinp, bound[1])
    ini_step = np.min([40, max_step])
    st_p = sinp + 0
    mid_p = list(inp)
    temp_p = sinp
    for i in range(0, 2000):
        if ini_step >= max_step:
            ubp = accuracy_bound_search_lb(temp_p, bound[1], test_fun, list(inp), idx)
            break
        st_p = bf.get_next_point(sinp, ini_step, 1)
        mid_p[idx] = st_p
        if st_p > bound[1]:
            ubp = bound[1]
            break
        res = test_fun(*mid_p)
        if not isfloat(res.val):
            ini_step = ini_step * 2.0
        else:
            ubp = accuracy_bound_search_ub(temp_p,st_p,test_fun,list(inp),idx)
            break
        temp_p = st_p
        # mid_i = float(fadd(lbp, fsub(ubp, lbp) / 2.0))
        # mid_p[idx] = mid_i
        # res = test_fun(*mid_p)
        # if isfloat(res.val):
        #     ubp = mid_i
        # else:
        #     lbp = mid_i
        # dis_lu = bf.getUlpError(lbp, ubp)
        # if dis_lu <= 2:
        #     break
    fl_ubp = ubp
    return [fl_lbp,fl_ubp]

def generate_mix_bound(old_bound,new_bound):
    mix_bound = []
    for i,j in zip(old_bound,new_bound):
        mix_bd = []
        if i[0]<j[0]:
            mix_bd.append(i[0])
        else:
            mix_bd.append(j[0])
        if i[1]<j[1]:
            mix_bd.append(j[1])
        else:
            mix_bd.append(i[1])
        mix_bound.append(mix_bd)
    return mix_bound


def localize_inbound(bound,fun_pu,stat_fun,inps_lst):
    lc_bound = []
    for i in bound:
        lc_bound.append([])
    temp_bound = list(lc_bound)
    # print "inps_lst"
    # print inps_lst
    flag = 0
    lc_bds_lst = []
    for i in inps_lst:
        if lc_bound[0] != []:
            for lbi in lc_bds_lst:
                flag = point_in_bound(i,lbi)
                if flag == 1:
                    break
        # print flag
        if flag==0:
            idx = 0
            fpb_i = []
            temp_inp = i
            for j in i:
                idx_bd = bound[idx]
                lc_bound[idx] = binary_find_bound(temp_inp[idx], idx_bd, temp_inp, fun_pu, idx)
                # print "idx"
                # print temp_bound
                # print lc_bound
                idx = idx + 1
            lc_bds_lst.append(lc_bound)
        # if temp_bound[0] != []:
        #     lc_bound = generate_mix_bound(lc_bound,temp_bound)
        # temp_bound = list(lc_bound)
    return bf.rm_dump_lst(lc_bds_lst)

def bound_equal(bd1,bd2):
    flag = 1
    for i,j in zip(bd1,bd2):
        if i == j:
            flag = flag*1
        else:
            flag = flag*0
    return flag


def bound_find2v(lc_bound,inp,test_fun,bound):
    bd0 = lc_bound[0]
    bds_lst = bf.bound_fpDiv(bd0)
    inps_lst = []
    lc_bds_lst = []
    temp_inp = list(inp)
    for i in bds_lst:
        inps_lst.append(random.uniform(i[0],i[1]))
    # print "len inps"
    for j in range(0,len(inps_lst)):
        temp_bd = []
        # print "temp_bd"
        # print j
        temp_bd.append(bf.fp_to_bound(inps_lst[j]))
        temp_inp[0]=inps_lst[j]
        # print temp_inp
        temp_bd.append(binary_find_bound(temp_inp[1], bound[1], temp_inp, test_fun, 1))
        lc_bds_lst.append(temp_bd)
    new_lc_bds = []
    merge_bd = lc_bds_lst[0]
    for i in lc_bds_lst[1:]:
        if bound_equal(merge_bd[1],i[1])==1:
            merge_bd = generate_mix_bound(merge_bd,i)
        else:
            new_lc_bds.append(merge_bd)
            merge_bd = i
    new_lc_bds.append(merge_bd)
    return new_lc_bds


def localize_inbound2v(bound,fun_pu,stat_fun,inps_lst):
    lc_bound = []
    for i in bound:
        lc_bound.append([])
    temp_bound = list(lc_bound)
    # print "inps_lst"
    # print inps_lst
    flag = 0
    lc_bds_lst = []
    final_bds_lst = []
    for i in inps_lst:
        if lc_bound[0] != []:
            for lbi in final_bds_lst:
                flag = point_in_bound(i,lbi)
                if flag == 1:
                    break
        # print flag
        if flag==0:
            idx = 0
            fpb_i = []
            temp_inp = i
            for j in i:
                idx_bd = bound[idx]
                lc_bound[idx] = binary_find_bound(temp_inp[idx], idx_bd, temp_inp, fun_pu, idx)
                # print "idx"
                # print temp_bound
                # print lc_bound
                idx = idx + 1
            lc_bds_lst = bound_find2v(lc_bound, i, fun_pu, bound)
            final_bds_lst = final_bds_lst + lc_bds_lst
    #     if temp_bound[0] != []:
    #         lc_bound = generate_mix_bound(lc_bound,temp_bound)
    #     temp_bound = list(lc_bound)
    # for i in lc_bound:
    #     print i
    return bf.rm_dump_lst(final_bds_lst)



def localize4exceptions(fid, test_fun, detect_res,eva_bound_lst,limit_time):
    fun_pu, stat_fun = load_pure_fun(test_fun[0])
    i = detect_res
    print detect_res
    print eva_bound_lst
    # print test_fun
    fpe_lst = []
    for j in range(0, len(i), 2):
        bt = i[j]
        res_lst = i[j + 1]
        if bt == 3:
            fpe_lst.append(res_lst[0][0] + res_lst[0][1] + res_lst[0][2])
    count = 0
    rf = lambda x: rf_f(fid, x)
    new_bounds = []
    print fpe_lst
    # new_bounds.append(fid)
    # new_bounds.append(test_fun[0])
    repair_bounds_final = []
    var_num = bf.get_var_num(test_fun)
    for i in eva_bound_lst:
        repair_bounds = []
        # print i
        ret_vals = i[0][1]
        num_excp = i[0][0]
        bt = get_bound_type(ret_vals, num_excp)
        bound = i[1]
        inp_lst = []
        loc_inps = []
        ty_f = 0
        if (bt == 3) & (fid != 97):
            # inp_lst = FPexcption_detector_whole(fun_pu, stat_fun, bound)
            inp_lst = inp_lst + fpe_lst[count]
            count = count + 1
            for ti in inp_lst:
                res_p = fun_pu(*ti)
                res_rf = float(rf(ti))
                signal.alarm(limit_time)
                ty_f = classifer(res_p.val, res_rf, stat_fun())
                print "ty_f"
                print ty_f
                if ty_f != 0:
                    loc_inps.append(ti)
            if loc_inps == []:
                new_bounds.append([(0, [-1]), bound])
            else:
                repair_bounds.append(bound)
                repair_bounds.append(ty_f)
                repair_bounds.append(loc_inps)
                new_bounds.append(i)
                if var_num == 1:
                    loc_bound_lst = localize_inbound(bound, fun_pu, stat_fun, loc_inps)
                    for lcb in loc_bound_lst:
                        new_bounds.append([(0, [-2]), lcb])
                    repair_bounds.append(loc_bound_lst)
                else:
                    loc_bound_lst = localize_inbound2v(bound, fun_pu, stat_fun, loc_inps)
                    for lcb in loc_bound_lst:
                        new_bounds.append([(0, [-2]), lcb])
                    repair_bounds.append(loc_bound_lst)
                repair_bounds_final.append(repair_bounds)
        else:
            new_bounds.append(i)
    return new_bounds,repair_bounds_final


def cal_exceptions():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    eva_bound_lst = bf.load_pickle("eva_bound_lst.plk")
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    cal_num = 0
    name_lst = []
    for fid in range(0,len(inter_funcs)):
        # fid = 14
        flag = 0
        test_fun = inter_funcs[fid]
        fun_pu, stat_fun = load_pure_fun(test_fun[0])
        i = sum_lst[fid]
        print test_fun
        fpe_lst = []
        for j in range(0, len(i[2]), 2):
            bt = i[2][j]
            res_lst = i[2][j + 1]
            if bt == 3:
                fpe_lst.append(res_lst[0][0] + res_lst[0][1] + res_lst[0][2])
        count = 0
        rf = lambda x: rf_f(fid,x)
        new_bounds = []
        # new_bounds.append(fid)
        # new_bounds.append(test_fun[0])
        var_num = bf.get_var_num(test_fun)
        print eva_bound_lst[fid]
        for i in eva_bound_lst[fid][2:]:
            print i
            ret_vals = i[0][1]
            num_excp = i[0][0]
            bt = get_bound_type(ret_vals, num_excp)
            bound = i[1]
            inp_lst = []
            loc_inps = []
            # print bound
            if (bt == 3) & (fid != 97):
                inp_lst = FPexcption_detector_whole(fun_pu, stat_fun, bound)
                inp_lst = inp_lst + fpe_lst[count]
                count = count + 1
                for ti in inp_lst:
                    res_p = fun_pu(*ti)
                    res_rf = float(rf(ti))
                    ty_f = classifer(res_p.val,res_rf,stat_fun())
                    if ty_f!=0:
                        loc_inps.append(ti)
                        flag = 1
        if flag == 1:
            name_lst.append([fid,test_fun[1]])
            cal_num = cal_num + 1
    print cal_num
    print cal_num
    for nai in name_lst:
        print nai


def localize_exceptions():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    eva_bound_lst = bf.load_pickle("eva_bound_lst.plk")
    sum_lst = bf.load_pickle("detect_res_lst.pkl")
    for fid in range(74,75):
        # fid = 14
        test_fun = inter_funcs[fid]
        fun_pu, stat_fun = load_pure_fun(test_fun[0])
        i = sum_lst[fid]
        print test_fun
        fpe_lst = []
        for j in range(0, len(i[2]), 2):
            bt = i[2][j]
            res_lst = i[2][j + 1]
            if bt == 3:
                fpe_lst.append(res_lst[0][0] + res_lst[0][1] + res_lst[0][2])
        count = 0
        rf = lambda x: rf_f(fid,x)
        new_bounds = []
        # new_bounds.append(fid)
        # new_bounds.append(test_fun[0])
        var_num = bf.get_var_num(test_fun)
        print eva_bound_lst[fid]
        for i in eva_bound_lst[fid][2:]:
            print i
            ret_vals = i[0][1]
            num_excp = i[0][0]
            bt = get_bound_type(ret_vals, num_excp)
            bound = i[1]
            inp_lst = []
            loc_inps = []
            # print bound
            if (bt == 3) & (fid != 97):
                inp_lst = FPexcption_detector_whole(fun_pu, stat_fun, bound)
                inp_lst = inp_lst + fpe_lst[count]
                count = count + 1
                for ti in inp_lst:
                    res_p = fun_pu(*ti)
                    res_rf = float(rf(ti))
                    ty_f = classifer(res_p.val,res_rf,stat_fun())
                    if ty_f!=0:
                        loc_inps.append(ti)
                if loc_inps == []:
                    new_bounds.append([(0,[-1]),bound])
                else:
                    new_bounds.append(i)
                    if var_num == 1:
                        loc_bound_lst = localize_inbound(bound, fun_pu, stat_fun, loc_inps)
                        print "loc_bound_lst"
                        print bound
                        print loc_bound_lst
                        for lcb in loc_bound_lst:
                            new_bounds.append([(0, [-2]), lcb])
                    else:
                        loc_bound_lst = localize_inbound2v(bound, fun_pu, stat_fun, loc_inps)
                        print "loc_bound_lst"
                        # print loc_bound_lst
                        print len(loc_bound_lst)
                        for lcb in loc_bound_lst:
                            new_bounds.append([(0, [-2]), lcb])
            else:
                new_bounds.append(i)
        if var_num == 1:
            plot_1func_domain(new_bounds)
        if var_num == 2:
            plot_2vfunc_domain(new_bounds)
        print new_bounds


if __name__ == "__main__":
    cal_exceptions()

