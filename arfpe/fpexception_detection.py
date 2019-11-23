from gen_drivfunc import *
import basic_func as bf
import random
from mpmath import *
import itertools
from scipy.optimize import basinhopping
import time
import signal
class TimeoutError (RuntimeError):
    pass

def handler (signum, frame):
    raise TimeoutError()
signal.signal(signal.SIGALRM, handler)


def extract_noempty_bound(bound):
    mp.dps = 30
    # bf.fpartition(bound)
    ret_lst = []
    if bound[0]==0:
        ret_lst.append(bf.f64min)
    else:
        ret_lst.append(bound[0] + bf.getulp(bound[0]))
    if bound[1] == 0:
        ret_lst.append(bf.f64min)
    else:
        ret_lst.append(bound[1] - bf.getulp(bound[1]))
    fpart_bound = bf.fdistribution_partition(bound[0],bound[1])
    a = int(max(len(fpart_bound)/10.0,1))
    if a == 0:
        a = 1
    for i in range(0,len(fpart_bound),a):
        ret_lst.append(random.uniform(fpart_bound[i][0],fpart_bound[i][1]))
    # step = [random.uniform(0,1) for i in range(0,10)]
    # mpf1 = mpf(bound[1])
    # mpf0 = mpf(bound[0])
    # distance = mpf1-mpf0

    # for i in step:
    #     ret_lst.append(float(mpf0+distance*i))
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


def bdary_fun(pf,x):
    try:
        x = list(x)
    except TypeError:
        x = [x]
    pf_res = pf(*x)
    return pf_res

def reduce_lst(ovfps_lst):
    temp_lst = []
    cont = 0
    for i in ovfps_lst:
        cont = cont + 1
        if i not in ovfps_lst[cont:]:
            temp_lst.append(i)
    return temp_lst


def FPexp_detect(fun_exe,widx_lst,bound,max_iter,num_exp):
    # print bound
    points_lst = get_testing_point(bound)
    ovfps_lst = []
    temp_bound = []
    for i in bound:
        if i == []:
            temp_bound.append([-bf.f64max,bf.f64max])
            # temp_bound.append([])
        else:
            temp_bound.append(i)
    glob_fitness_fun = lambda x: bdary_fun(fun_exe, bf.reduce_x(temp_bound, x))
    # glob_fitness_fun = lambda x: bdary_fun(fun_exe, x)
    # minimizer_kwargs = {"method": "Powell"}
    # minimizer_kwargs = {"method": "TNC"}
    minimizer_kwargs = {"method": "Nelder-Mead"}
    # max_iter = widx_lst[4].value
    # print max_iter
    # print num_exp
    # bar = progressbar.ProgressBar(maxval=max_iter, \
    #                               widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    # bar.start()
    st = time.time()
    temp_points = []
    temp_ovfps_lst = []
    for i in points_lst:
        res = glob_fitness_fun(i)
        widx_lst[3].value = 0
        if res != 1e100:
            temp_points.append(i)
    st_flag = 0
    for j in range(0, max_iter):
        # print j
        # print ovfps_lst
        for i in temp_points:
            # print i
            try:
                signal.alarm(5)
                temp_i = bf.generate_x(temp_bound, i)
                # temp_i = i
                res = basinhopping(glob_fitness_fun, temp_i, minimizer_kwargs=minimizer_kwargs, niter_success=1)
                if res.fun == 0:
                    try:
                        inp = list(res.x)
                    except TypeError:
                        inp = [res.x]
                    # print "inp"
                    # print res.x
                    # ovfps_lst.append(bf.reduce_x(temp_bound,res.x))
                    ovfps_lst.append(bf.reduce_x(temp_bound, inp))
                    break
            except TimeoutError:
                break
        signal.alarm(60)
        widx_lst[2][j] = widx_lst[3].value
        widx_lst[1].value = j + 1
        widx_lst[3].value = 0
        et = time.time() - st
        ovfps_lst = reduce_lst(ovfps_lst)
        if len(temp_ovfps_lst) == len(ovfps_lst):
            st_flag = st_flag + 1
        else:
            st_flag = 0
        if st_flag > 30:
            break
        if len(ovfps_lst)>num_exp:
            break
        if et > 600:
            break
        temp_ovfps_lst = ovfps_lst + []

    # bar.finish()
    temp_lst = []
    cont = 0
    for i in ovfps_lst:
        cont = cont + 1
        if i not in ovfps_lst[cont:]:
            temp_lst.append(i)
    return temp_lst


def get_random_point(bound):
    points_lst = []
    bounds_lst = []
    for i in bound:
        bound_lst = bf.bound_fpDiv(i)
        temp_pst = []
        for j in bound_lst:
            if 0.0 in j:
                temp_pst.append(j[0])
                temp_pst.append(j[1])
            else:
                if j[0]>0:
                    temp_pst.append(j[1])
                else:
                    temp_pst.append(j[0])
        points_lst.append(temp_pst)
        bounds_lst.append(bound_lst)
    ret_lst = []
    ret_lst2 = []
    for element in itertools.product(*points_lst):
        ret_lst.append(list(element))
    for element in itertools.product(*bounds_lst):
        ret_lst2.append(list(element))
    return ret_lst,ret_lst2

# ret_lst,ret_lst2 = get_random_point([[0,10],[0,10]])
# print ret_lst[0]
# print ret_lst2[0]
def issubnormal(res):
    if (res!=0)&(fabs(res)<bf.f64min):
        return 1
    else:
        return 0

def pure_fun_test(pf,x):
    sf_res = pf(*x)
    pf_res = sf_res.val
    return pf_res

def random_sample_test(fun_exe,stat_fun,bound,num_exp):
    # print bound
    points_lst,bounds_lst = get_random_point(bound)
    ovfps_lst = []
    temp_bound = []
    for i in bound:
        if i == []:
            temp_bound.append([-bf.f64max, bf.f64max])
            # temp_bound.append([])
        else:
            temp_bound.append(i)
    # glob_fitness_fun = lambda x: bdary_fun(fun_exe, bf.reduce_x(temp_bound, x))
    glob_fitness_fun = lambda x: pure_fun_test(fun_exe, x)
    nan_res = []
    of_res = []
    uf_res = []
    temp_dect_lst = []
    print len(points_lst)
    print len(bounds_lst)
    for i,j in zip(points_lst,bounds_lst):
        res = glob_fitness_fun(i)
        stat = stat_fun()
        flag = 0
        if isnan(res):
            nan_res.append(i)
            flag = 1
        if isinf(res):
            of_res.append(i)
            flag = 1
        if issubnormal(res):
            uf_res.append(i)
            flag = 1
        if (flag == 1)&(stat == 0):
            flag = 1
        else:
            flag = 0
        if flag == 1:
            temp_dect_lst.append([j,nan_res, of_res, uf_res])
    return temp_dect_lst


def FPoverflow_detector(fun_exe,widx_lst,bound):
    print bound
    points_lst = get_testing_point(bound)
    minimizer_kwargs = {"method": "Powell"}
    ovfps_lst = []
    temp_bound = []
    for i in bound:
        if i == []:
            temp_bound.append([-bf.f64max,bf.f64max])
        else:
            temp_bound.append(i)
    # glob_fitness_fun = lambda x: bdary_fun(fun_exe, bf.reduce_x(temp_bound, x))
    glob_fitness_fun = lambda x: bdary_fun(fun_exe, x)
    print len(points_lst)
    for i in points_lst:
        # print i
        # print glob_fitness_fun(i)
        # temp_i = bf.generate_x(temp_bound,i)
        temp_i = i
        res = basinhopping(glob_fitness_fun, temp_i, minimizer_kwargs=minimizer_kwargs, niter_success=1, niter=200)
        if res.fun == 0:
            widx_lst[3].value = 0
            # ovfps_lst.append(bf.reduce_x(temp_bound,res.x))
            ovfps_lst.append(res.x)
    return ovfps_lst

# x = x >> 53
# print x
# print np.nan < bf.f64max
# print fabs(np.nan)
def Oflow_fun(pf,x):
    fpmax = bf.f64max
    sf_res = pf(*x)
    pf_res = fabs(sf_res.val)
    if(pf_res<fpmax):
        w = fpmax - pf_res
    else:
        w = 0.0
    return w

def FPexcption_detector_whole(fun_exe,stat_fun,bound):
    points_lst = get_testing_point(bound)
    minimizer_kwargs = {"method": "Powell"}
    ovfps_lst = []
    temp_bound = []
    for i in bound:
        if i == []:
            temp_bound.append([-bf.f64max,bf.f64max])
        else:
            temp_bound.append(i)
    glob_fitness_fun = lambda x: Oflow_fun(fun_exe, bf.reduce_x(temp_bound, x))
    # print len(points_lst)
    for i in points_lst:
        # print i
        try:
            temp_i = bf.generate_x(temp_bound, i)
            res = basinhopping(glob_fitness_fun, temp_i, minimizer_kwargs=minimizer_kwargs, niter_success=1, niter=200)
            # print res.fun
            if res.fun == 0:
                inp = bf.reduce_x(temp_bound, res.x)
                glob_fitness_fun(inp)
                stat = stat_fun()
                if stat == 0:
                    ovfps_lst.append(inp)
        except (TypeError,TimeoutError):
            continue
    temp_lst = []
    cont = 0
    for i in ovfps_lst:
        cont = cont + 1
        if i not in ovfps_lst[cont:]:
            temp_lst.append(i)
    return temp_lst


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


def append_noempty_lst(aplst,a):
    if a!=[]:
        aplst.append(a)
    return aplst


def detect_exception(fid,test_fun,eva_bound_lst):
    fun_dz, widx_lstdz = load_fpdz_fun(test_fun[0])
    fun_nan, widx_lstnan = load_fpnan_fun(test_fun[0])
    fun_of, widx_lstof = load_fpof_fun(test_fun[0])
    fun_uf, widx_lstuf = load_fpuf_fun(test_fun[0])
    # fun_pu, stat_fun = load_pure_fun(test_fun[0])
    detect_lst = []
    detect_lst.append(fid)
    detect_lst.append(test_fun[0])
    # print fun_dz(-1.8427611519777438)
    temp_res = []
    limit_time = 120
    st = time.time()
    for i in eva_bound_lst:
        # temp_res.append(i)
        ret_vals = i[0][1]
        num_excp = i[0][0]
        bt = get_bound_type(ret_vals, num_excp)
        # print bt
        temp_dect_lst = []
        temp_res.append(bt)
        bound = i[1]
        # print i
        dz_res= []
        nan_res= []
        uf_res= []
        of_res= []
        try:
            signal.alarm(limit_time)
            if bt == 3:
                if fid != 97:
                    # print "detect res"
                    dz_res = FPexp_detect(fun_dz, widx_lstdz, bound, widx_lstdz[4].value, num_excp)
                    nan_res = FPexp_detect(fun_nan, widx_lstnan, bound, widx_lstdz[4].value, num_excp)
                    of_res = FPexp_detect(fun_of, widx_lstof, bound, widx_lstdz[4].value, num_excp)
                    # uf_res =  FPexp_detect(fun_uf, widx_lstuf, bound, widx_lstuf[4].value, widx_lstuf[4].value)
                    temp_dect_lst.append([dz_res,nan_res,of_res])
                    temp_dect_lst.append(bound)
                else:
                    b00 = bound[0][0]
                    if b00 < -400:
                        bound[0][0] = -400
                    dz_res = FPexp_detect(fun_dz, widx_lstdz, bound, widx_lstdz[4].value, num_excp)
                    nan_res = FPexp_detect(fun_nan, widx_lstnan, bound, widx_lstdz[4].value, num_excp)
                    of_res = FPexp_detect(fun_of, widx_lstof, bound, widx_lstdz[4].value, num_excp)
                    uf_res =  FPexp_detect(fun_uf, widx_lstuf, bound, widx_lstuf[4].value, widx_lstuf[4].value)
                    temp_dect_lst.append([dz_res, nan_res, of_res],bound)
                    temp_dect_lst.append(bound)
        except TimeoutError:
            temp_dect_lst.append([dz_res, nan_res, of_res])
        signal.alarm(0)
        temp_res.append(temp_dect_lst)
    et = time.time() - st
    detect_lst.append(temp_res)
    # detect_lst.append(et)
    return detect_lst


def detect_underflow(fid,test_fun,eva_bound_lst):
    fun_dz, widx_lstdz = load_fpdz_fun(test_fun[0])
    fun_nan, widx_lstnan = load_fpnan_fun(test_fun[0])
    fun_of, widx_lstof = load_fpof_fun(test_fun[0])
    fun_uf, widx_lstuf = load_fpuf_fun(test_fun[0])
    # fun_pu, stat_fun = load_pure_fun(test_fun[0])
    detect_lst = []
    detect_lst.append(fid)
    detect_lst.append(test_fun[0])
    # print fun_dz(-1.8427611519777438)
    temp_res = []
    limit_time = 60
    print widx_lstuf
    st = time.time()
    for i in eva_bound_lst:
        # temp_res.append(i)
        ret_vals = i[0][1]
        num_excp = i[0][0]
        bt = get_bound_type(ret_vals, num_excp)
        # print bt
        temp_dect_lst = []
        temp_res.append(bt)
        bound = i[1]
        # print i
        dz_res= []
        nan_res= []
        uf_res= []
        of_res= []
        try:
            signal.alarm(limit_time)
            if bt == 3:
                if fid != 97:
                    # print "detect res"
                    # dz_res = FPexp_detect(fun_dz, widx_lstdz, bound, widx_lstdz[4].value, num_excp)
                    # nan_res = FPexp_detect(fun_nan, widx_lstnan, bound, widx_lstdz[4].value, num_excp)
                    # of_res = FPexp_detect(fun_of, widx_lstof, bound, widx_lstdz[4].value, num_excp)
                    uf_res =  FPexp_detect(fun_uf, widx_lstuf, bound, widx_lstuf[4].value, widx_lstuf[4].value)
                    temp_dect_lst.append(uf_res)
                else:
                    b00 = bound[0][0]
                    if b00 < -400:
                        bound[0][0] = -400
                    # dz_res = FPexp_detect(fun_dz, widx_lstdz, bound, widx_lstdz[4].value, num_excp)
                    # nan_res = FPexp_detect(fun_nan, widx_lstnan, bound, widx_lstdz[4].value, num_excp)
                    # of_res = FPexp_detect(fun_of, widx_lstof, bound, widx_lstdz[4].value, num_excp)
                    uf_res =  FPexp_detect(fun_uf, widx_lstuf, bound, widx_lstuf[4].value, widx_lstuf[4].value)
                    temp_dect_lst.append(uf_res)
            else:
                if bt in [1,4]:
                    uf_res = FPexp_detect(fun_uf, widx_lstuf, bound, widx_lstuf[4].value, widx_lstuf[4].value)
                    temp_dect_lst.append(uf_res)
        except TimeoutError:
            temp_dect_lst.append(uf_res)
        signal.alarm(0)
        temp_res.append(temp_dect_lst)
    et = time.time() - st
    detect_lst.append(temp_res)
    # detect_lst.append(et)
    return detect_lst




