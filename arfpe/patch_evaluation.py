import basic_func as bf
from gen_drivfunc import load_pure_fun
import os
import numpy as np
import itertools
import random
import time
import matplotlib
import matplotlib.pyplot as plt
import xlrd
import xlwt
from xlutils.copy import copy

inter_funcs = bf.load_pickle('fun_index.pkl')
sum_lst = bf.load_pickle("detect_res_lst.pkl")
fid_lst = []


fid_lc = [2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 63, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]


# for i in [40]:
#     test_fun = inter_funcs[i]
#     print test_fun
#     var_num = bf.get_var_num(test_fun)
#     name = "localize_res_files/" + test_fun[0] + ".pkl"
#     fun_pu, stat_fun = load_pure_fun(test_fun[0])
#     res = fun_pu(-1e100)
#     print res.val

def extract_noempty_bound(bound,num):
    ret_lst = []
    for i in range(0,num):
        ret_lst.append(random.uniform(bound[0],bound[1]))
    return ret_lst

def get_testing_point(bound,num):
    points_lst = []
    bl = len(bound)
    for i in bound:
        if i == []:
            points_lst.append(bf.get_double_random())
        else:
            points_lst.append(extract_noempty_bound(i,num))
    ret_lst = []
    # for i in points_lst:
    #     print len(i)
    for element in itertools.product(*points_lst):
        ret_lst.append(list(element))
    return ret_lst

def get_points(repair_res,fun_pu):
    test_num = 1000000
    len_r = len(repair_res)
    avg_num = test_num/len_r
    inps_lst = []
    for i in repair_res:
        temp_num = avg_num/len(i[-2])
        for ri in i[-2]:
            inps_lst = inps_lst + get_testing_point(ri,int(np.sqrt(temp_num)))
    return inps_lst




def run_time_evaluation():
    name = "papergraph/time_before_repair.pkl"
    time_lst = []
    for i in fid_lc:
        test_fun = inter_funcs[i]
        print test_fun
        name2 = "repair_res_files/" + test_fun[0] + ".pkl"
        repair_res = bf.load_pickle(name2)
        # print repair_res
        # print repair_res[0]
        fun_pu, stat_fun = load_pure_fun(test_fun[0])
        inps_lst = get_points(repair_res[0:-1], fun_pu)
        print "generate points"
        st = time.time()
        for inp in inps_lst:
            fun_pu(*inp)
        et = time.time() - st
        time_lst.append(et)
        print et
    bf.pickle_fun(name,time_lst)
    return 0
# run_time_evaluation()
def export2excel(patch_sz_lst,repair_res):
    table_name = "papergraph/patch_size.xls"
    old_excel = xlrd.open_workbook(table_name)
    table = old_excel.sheets()[0]
    new_excel = copy(old_excel)
    sheet = new_excel.get_sheet(0)
    for i in range(0,len(patch_sz_lst)):
        sheet.write(0, i, "P" + str(i+1))
    for i in range(0,len(patch_sz_lst)):
        sheet.write(1, i, repr(patch_sz_lst[i]))
    for i in range(0,len(repair_res)):
        sheet.write(2, i, repr(repair_res[i]))
    new_excel.save(table_name)

def patch_size_evaluation():
    patch_sz_lst = []
    repair_res = []
    cout = 0
    for i in fid_lc:
        test_fun = inter_funcs[i]
        print test_fun
        size_file = os.path.getsize('patches/patch_of_' + test_fun[0] + ".c")
        name2 = "repair_res_files/" + test_fun[0] + ".pkl"
        rep_res = bf.load_pickle(name2)
        sum_len = 0
        for ri in rep_res[0:-1]:
            sum_len = sum_len + len(ri[-2])
        tp_st = size_file/1024.0
        if tp_st < 1.0:
            cout = cout + 1
        patch_sz_lst.append(size_file/1024.0)
        repair_res.append(sum_len)
    print cout
    export2excel(patch_sz_lst, repair_res)

patch_size_evaluation()
def plot_time_overhead(z1):
    z1 = np.array(z1)
    z1 = np.sort(z1)
    y = np.arange(1, len(z1) + 1) / float(len(z1))
    return z1, y

def process_cumulative_dis_time(b, a):
    ratio_b = []
    for i, j in zip(b, a):
        ratio_b.append(j / i)
    z1 = []
    # z2 = []
    # z3 = []
    # k = 0
    z1 = list(ratio_b)
    # for i in range(0, 20):
    #     if i != 14:
    #         z1.append(ratio_b[i + k])
    #         z2.append(ratio_b[i + k + 1])
    #         z3.append(ratio_b[i + k + 2])
    #     k = k + 2
    # print z2
    z1, y1 = plot_time_overhead(z1)
    return z1,y1
matplotlib.rcParams['text.usetex'] = True

def plot_compare_timeoverhead():
    be_res_list = []
    af_res_list = []
    name = 'papergraph/time_overhead_whole'
    bbpf_time_l = bf.load_pickle("/home/yixin/PycharmProjects/ARFPE/arfpe/papergraph/time_before_repair.pkl")
    abpf_time_l = bf.load_pickle("/home/yixin/PycharmProjects/ARFPE/arfpe/papergraph/time_after_repair.pkl")
    z1, y1 = process_cumulative_dis_time(bbpf_time_l, abpf_time_l)
    be_res_list.append(z1)
    af_res_list.append(y1)

    count = 0
    color_type = ['k--', 'k-']
    tool_name = ['']
    # fig = plt.figure(figsize=(14, 12))
    ax = plt.subplot(111)
    # print be_res_list
    # print af_res_list
    for i, j in zip(be_res_list, af_res_list):
        ax.plot(i, j, color_type[count])
        count = count + 1
    ylabels = [r'0\%']
    for i in np.arange(0, 105, 20):
        ylabels.append(str(i) + "\%")
    ax.set_yticks(np.arange(0, 1.1, 0.2), ylabels)
    for tick in ax.xaxis.get_major_ticks():
        tick.label.set_fontsize(12)
        # ax.set_xticks(np.arange(0.5, 1.3, 0.1))
    # ax.set_xticklabels(['0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2'], fontsize=12)
    # plt.yticks(np.arange(0, 1.1, 0.2), ylabel)
    # plt.ylabel('% of benchmarks',fontsize=16)
    ax.set_yticklabels(ylabels, fontsize=12)
    ax.set_ylabel(r'\% of benchmarks', fontsize=16)
    # plt.xlabel('Time overhead ratio: Repair program/origin program',fontsize=20)
    ax.legend(loc=4, prop={'size': 14})
    ax.grid(True)
    # plt.ylim([0,1.1])
    plt.savefig(name + ".pdf", format="pdf")
    plt.show()
# plot_compare_timeoverhead()