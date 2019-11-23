import basic_func as bf
import numpy as np
from scipy.optimize import basinhopping
import time
import itertools
import random
import progressbar

src_path = '../benchmark/gsl-2.6/specfunc/'

def bdary_fun(pf,x):
    try:
        x = list(x)
    except TypeError:
        x = [x]
    pf_res = np.fabs(pf(*x))
    return pf_res

def gen_new_bdarylst(fres_1st,glob_fitness_fun,bdary_lst):
    for j in fres_1st:
        try:
            inp = list(j)
        except TypeError:
            inp = [j]
        idx = 0
        for i in inp:
            if i <= bf.f64max:
                i = float(i)
                temp_inp = list(inp)
                if i > 0:
                    temp_i = i - bf.getulp(i) * 1e12
                else:
                    temp_i = i + bf.getulp(i) * 1e12
                if i == 0:
                    temp_i = 1e-154
                temp_inp[idx] = temp_i
                temp_res = glob_fitness_fun(temp_inp)
                if temp_res != 0:
                    bdary_lst[idx].append(i)
                    if i != 0.0:
                        temp_i = -i
                        temp_inp[idx] = temp_i
                        temp_res = glob_fitness_fun(temp_inp)
                        if temp_res == 0:
                            bdary_lst[idx].append(-i)
                idx = idx + 1
    return bdary_lst


def gen_new_inps(bdary_lst):
    temp_lst = []
    inps_lst = []
    for i in bdary_lst:
        temp_lst.append([])
    idx = 0
    special_inps = [-1.4916681462400413e-154,1.4916681462400413e-154]
    # special_inps = []
    for i in bdary_lst:
        if i == []:
            rand_vals = bf.get_double_random_small()
            rd_idx = random.randint(0, len(rand_vals)-1)
            # rd_idx2 = random.randint(0, len(rand_vals)-1)
            temp_lst[idx].append(rand_vals[rd_idx])
            # temp_lst[idx].append(rand_vals[rd_idx2])
            # temp_lst[idx] = temp_lst[idx]+special_inps
        else:
            i.sort()
            if len(i)>1:
                temp_j = i[0]
                temp_lst[idx].append(temp_j - bf.getulp(temp_j) * 1e13)
                for j in i[1:]:
                    temp_lst[idx].append((j-temp_j)/2.0 + temp_j)
                    temp_j = j
                temp_lst[idx].append(i[-1] + bf.getulp(i[-1]) * 1e13)
            # else:
            for j in i:
                if j==0:
                    temp_lst[idx] = temp_lst[idx] + special_inps
                    # rand_vals = bf.get_double_random_small()
                    # rd_idx = random.randint(0, len(rand_vals)-1)
                    # special_inps
                    # temp_lst[idx].append(-np.fabs(rand_vals[rd_idx]))
                    # temp_lst[idx].append(np.fabs(rand_vals[rd_idx]))
                else:
                    temp_lst[idx].append(j + bf.getulp(j) * 1e12)
                    temp_lst[idx].append(j - bf.getulp(j) * 1e12)
                    rand_vals = bf.get_double_random_small()
                    rd_idx = random.randint(0, len(rand_vals) - 1)
                    temp_lst[idx].append(rand_vals[rd_idx])
                    temp_lst[idx].append(-rand_vals[rd_idx])
            # temp_lst[idx] = temp_lst[idx] + special_inps
        idx = idx+1
    for element in itertools.product(*temp_lst):
        inps_lst.append(list(element))
    return inps_lst

def extract_widx_lst(idx_lst,len_val):
    temp_lst = []
    for i in range(0,len_val):
        temp_lst.append(int(idx_lst[i]))
    return temp_lst
# boundary value analysis
# input:
# 1.function after insert boundary value analysis
# output:
# 1.boundary value
def boundary_val_produce(fun_exe,test_fun,widx_lst):
    glob_fitness_fun = lambda x: bdary_fun(fun_exe,x)
    var_lst = []
    for i in test_fun[1]:
        if i[0] == 'double':
            var_lst.append(bf.get_double_random_small())
    num_var = len(var_lst)
    fres_1st = []
    bdary_lst = []
    st = time.time()
    for i in range(0,num_var):
        bdary_lst.append([])
    inps_lst = gen_new_inps(bdary_lst)
    count = 0
    jump_flag = 1
    # print "Trying to calculate boudary values"
    empty_count = 0
    max_iter = widx_lst[4].value
    # print max_iter
    # bar = progressbar.ProgressBar(maxval=max_iter, \
    #                               widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    # bar.start()
    for i in range(0, max_iter):
        fres_1st = []
        # bar.update(i)
        temp_inps_lst = inps_lst + []
        random.shuffle(temp_inps_lst)
        for j in temp_inps_lst[0:100]:
            temp_res = bf.simple_root_search(fun_exe, list(j), bdary_lst)
            if temp_res!=[]:
                fres_1st.append(temp_res)
            else:
                minimizer_kwargs = {"method": "TNC"}
                res1 = basinhopping(glob_fitness_fun, j, minimizer_kwargs=minimizer_kwargs,
                                    niter_success=1)
                if res1.fun == 0:
                    fres_1st.append(list(res1.x))
                minimizer_kwargs = {"method": "Nelder-Mead"}
                res2 = basinhopping(glob_fitness_fun, j, minimizer_kwargs=minimizer_kwargs,
                                    niter_success=1)
                if res2.fun == 0:
                    fres_1st.append(list(res2.x))
            if (fres_1st!=[]):
                break
        if (fres_1st != []):
            temp_lst = []
            # print "bdary_lst"
            new_fres_1st = []
            for fi in range(0, len(fres_1st) - 1):
                if fres_1st[fi] not in fres_1st[fi + 1:]:
                    new_fres_1st.append(fres_1st[fi])
            new_fres_1st.append(fres_1st[-1])
            fres_1st = list(new_fres_1st)
            # print fres_1st
            bdary_lst = gen_new_bdarylst(fres_1st, glob_fitness_fun, bdary_lst)
            res_bound = []
            for bi in bdary_lst:
                bi.sort()
                temp_lst = bf.rm_duplicates(bi)
                res_bound.append(temp_lst)
            bdary_lst = list(res_bound)
            inps_lst = gen_new_inps(bdary_lst)
        widx_lst[2][i] = widx_lst[3].value
        widx_lst[1].value = i + 1
        widx_lst[3].value = 0
    # bar.finish()
    res_bound = []
    for i in bdary_lst:
        i.sort()
        temp_lst = bf.rm_duplicates(i)
        res_bound.append(temp_lst)
    return res_bound

