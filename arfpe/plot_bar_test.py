import numpy as np
import matplotlib.pyplot as plt
import basic_func as bf
import matplotlib
fid_lc = [2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 63, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]
fid_de = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 95, 96, 98, 99, 100, 101, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 127, 128, 129, 130, 131, 132, 133, 135, 136, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157]
print len(fid_de)
matplotlib.rcParams['text.usetex'] = True
def get_detecting_time():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    time_lst = []
    repair_time = []
    for i in fid_de:
        test_fun = inter_funcs[i]
        # print test_fun
        var_num = bf.get_var_num(test_fun)
        name2 = "final_res_files/" + test_fun[0] + ".pkl"
        det_res = bf.load_pickle(name2)
        # print det_res[-1]
        time_lst.append(det_res[-1])
    sum_time_lst = []
    count = 0
    for i in time_lst:
        sum_time = 0
        for j in i:
            sum_time = sum_time + j
        sum_time_lst.append(sum_time)
        if sum_time > 1000:
            print sum_time
            # print inter_funcs[fid_lc[count]]
        count = count + 1

    print np.max(sum_time_lst)
    print np.min(sum_time_lst)
    count = 0
    for i in sum_time_lst:
        if i < 1000:
            count = count + 1
    print count
    print count-len(sum_time_lst)
    tot_time = 0
    for i in sum_time_lst:
        tot_time = i + tot_time
    print tot_time

    # fig1, ax1 = plt.subplots() 0-20 51 20-100 67 100-1000 19 1000-2500 5
    # fig1, ax1 = plt.subplots() 0-20 13 20-100 21 100-1000 7 1000-2500 2
    # ax1.set_title('Basic Plot')118
    # ax1.boxplot(sum_time_lst)
    # plt.show()

# get_detecting_time()

def get_repairing_time():
    inter_funcs = bf.load_pickle('fun_index.pkl')
    time_lst = []
    repair_time = []
    for i in fid_lc:
        test_fun = inter_funcs[i]
        print test_fun
        var_num = bf.get_var_num(test_fun)
        name2 = "final_res_files/" + test_fun[0] + ".pkl"
        name3 = "localize_res_files/" + test_fun[0] + ".pkl"
        name4 = "repair_res_files/" + test_fun[0] + ".pkl"
        det_res = bf.load_pickle(name2)
        loc_res = bf.load_pickle(name3)
        rep_res = bf.load_pickle(name4)
        for ri in rep_res[0:-1]:
            print ri[-1]
        temp_t = det_res[-1] + [loc_res[-1] , rep_res[-1]]
        # print temp_t
        time_lst.append(temp_t)
    sum_time_lst = []
    count = 0
    for i in time_lst:
        sum_time = 0
        for j in i:
            sum_time = sum_time + j
        sum_time_lst.append(sum_time)
        # if sum_time > 1000:
        print sum_time
        print inter_funcs[fid_lc[count]]
        count = count + 1
    print np.max(sum_time_lst)
    print np.min(sum_time_lst)
    count = 0
    for i in sum_time_lst:
        if i < 1000:
            count = count + 1
    print count
    print count-len(sum_time_lst)
    tot_time = 0
    for i in sum_time_lst:
        tot_time = i + tot_time
    print tot_time
    # fig1, ax1 = plt.subplots()
    # ax1.set_title('Basic Plot')
    # ax1.boxplot(sum_time_lst)
    # plt.show()

get_repairing_time()
def plot_detectsum_bar():
    N = 4
    menMeans = (51, 67, 19, 5)
    # plt.figure(figsize=(12, 14))
    fig,ax = plt.subplots()
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    bar_tick_label = [str(i) for i in menMeans]
    bar_plot = plt.bar(ind, menMeans, width,zorder=3)
    # p2 = plt.bar(ind, womenMeans, width,
    #              bottom=menMeans, yerr=womenStd)
    def autolabel(rects):
        for idx, rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    bar_tick_label[idx],
                    ha='center', va='bottom', rotation=0,fontsize=14)

    autolabel(bar_plot)
    plt.ylabel('Number of functions',fontsize=18)
    plt.xlabel('Time overhead(seconds)',fontsize=18)
    # plt.title('Scores by group and gender')
    plt.xticks(ind, ('[0,20]', '[20,100]', '[100,1000]', '[1000,2200]'),fontsize=18)
    plt.yticks(np.arange(0, 81, 10))
    # plt.grid()
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))
    plt.tight_layout()
    plt.savefig("papergraph/timedetect.pdf", format="pdf")
    plt.show()

def plot_repair_bar():
    N = 4
    menMeans = (13, 21, 7, 2)
    # plt.figure(figsize=(12, 14))
    fig,ax = plt.subplots()
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35  # the width of the bars: can also be len(x) sequence
    bar_tick_label = [str(i) for i in menMeans]
    bar_plot = plt.bar(ind, menMeans, width,zorder=3)
    # p2 = plt.bar(ind, womenMeans, width,
    #              bottom=menMeans, yerr=womenStd)
    def autolabel(rects):
        for idx, rect in enumerate(bar_plot):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    bar_tick_label[idx],
                    ha='center', va='bottom', rotation=0,fontsize=14)

    autolabel(bar_plot)
    plt.ylabel('Number of functions',fontsize=18)
    plt.xlabel('Time overhead(seconds)',fontsize=18)
    # plt.title('Scores by group and gender')
    plt.xticks(ind, ('[0,20]', '[20,100]', '[100,1000]', '[1000,2200]'),fontsize=18)
    plt.yticks(np.arange(0, 31, 10))
    # plt.grid()
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))
    plt.tight_layout()
    plt.savefig("papergraph/repair.pdf", format="pdf")
    plt.show()
# plot_detectsum_bar()
# plot_repair_bar()