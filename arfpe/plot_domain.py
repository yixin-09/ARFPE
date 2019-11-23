import numpy as np
import basic_func as bf
import math
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axisartist.axislines import SubplotZero
import pylab
import matplotlib
matplotlib.rcParams['text.usetex'] = True

def partition_double(x):
    if math.isnan(x):
        return 1,2047,2.0
    val = np.fabs(x)
    valint = bf.floatToRawLongBits(val)
    # val = valint<<1
    if x<0:
        sign = -1
    else:
        sign = 1
    exponent = (valint>>52)
    significant =val/2.0/pow(2.0,exponent-1023)
    return sign,exponent,significant




# print partition_double(bf.f64max)
# print partition_double(1.5)
# print 1.375*np.power(2.0,3)

def get_bound_color(ret_vals,num_excp):
    bound_color = ''
    if -1 in ret_vals:
        return "blue"
    if -2 in ret_vals:
        return "green"
    if 0 not in ret_vals:
        bound_color = 'black'
    else:
        if len(ret_vals) == 1:
            if num_excp == 0:
                bound_color = 'green'
            else:
                bound_color = 'blue'
        else:
            if num_excp == 0:
                bound_color = 'yellow'
            else:
                bound_color = 'red'
    return bound_color
def get_Rectangle_xy(bound):
    rect_xy_lst = []
    for i in bound:
        s,e,m = partition_double(i[0])
        s2,e2,m2 = partition_double(i[1])
        xy = [s*e+s*m,-0.25]
        lgt = s2*e2-s*e
        hgt = 0.5
        rect_xy_lst.append([xy,lgt,hgt])
    return rect_xy_lst

def get_Rectangle_xy2v(bound):
    rect_xy_lst = []
    i = bound[0]
    s,e,m = partition_double(i[0])
    s2,e2,m2 = partition_double(i[1])
    x = s*e+s*m
    lgt = (s2*e2+s2*m2)-(s*e+s*m)
    i = bound[1]
    s, e, m = partition_double(i[0])
    s2, e2, m2 = partition_double(i[1])
    y = s * e + s * m
    hgt = (s2*e2+s2*m2)-(s*e+s*m)
    xy = [x,y]
    rect_xy_lst.append([xy,lgt,hgt])
    return rect_xy_lst

# plot_lst: [func_name,id,[(number_of_exception,[return_vals]),bound]*n]
# green: return_vals = [0], number_of_exception = 0
# black: 0 not in return_vals
# red: return_vals = [0], number_of_exception !=0
# yellow: return_vals = [0+ ...], number_of_exception !=0
# covert_lst = [func_name,id,[color,Rectangle[xy,length,height]*n]
def extract_information(plot_lst):
    covert_lst = []
    # covert_lst.append(plot_lst[0])
    # covert_lst.append(plot_lst[1])
    temp_lst = []
    for i in plot_lst:
        ret_vals = i[0][1]
        num_excp = i[0][0]
        bound_color = get_bound_color(ret_vals,num_excp)
        bound = i[1]
        rect_xy_lst = get_Rectangle_xy(bound)
        temp_lst.append([bound_color,rect_xy_lst])
    # covert_lst.append(temp_lst)
    return temp_lst

def extract_information2v(plot_lst):
    covert_lst = []
    # covert_lst.append(plot_lst[0])
    # covert_lst.append(plot_lst[1])
    temp_lst = []
    for i in plot_lst:
        ret_vals = i[0][1]
        num_excp = i[0][0]
        bound_color = get_bound_color(ret_vals,num_excp)
        bound = i[1]
        rect_xy_lst = get_Rectangle_xy2v(bound)
        temp_lst.append([bound_color,rect_xy_lst])
    # covert_lst.append(temp_lst)
    return temp_lst


# plot_lst_sum = bf.load_pickle('plot_lst_sum')
# print plot_lst_sum
# inf_lst = extract_information(plot_lst_sum[0])
# print inf_lst
def plot_1func_domain(plot_lst):
    inf_lst = extract_information(plot_lst)
    fig = plt.figure(figsize=(25, 2))
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)
    for i in inf_lst:
        bound_color = i[0]
        print i
        xy_x = i[1][0][0][0]
        xy_y = i[1][0][0][1]
        lgt = i[1][0][1]
        rect = plt.Rectangle((xy_x, xy_y), lgt, 0.5, fill=True, facecolor=bound_color, edgecolor=bound_color, linewidth=0)
        ax.add_patch(rect)
    plt.ylim((-0.25, 0.25))
    plt.xlim((-2150, 2150))
    plt.yticks([])
    # plt.savefig("graph2/" + fun_name + ".pdf", format="pdf")
    plt.savefig("papergraph/" + "erfbdvals.eps", format="eps")
    # plt.close()
    plt.show()


def plot_1func_domain_example(plot_lst):
    inf_lst = extract_information(plot_lst)
    fig = plt.figure(figsize=(40, 3))
    # ax = SubplotZero(fig, 111)
    ax = fig.add_subplot(111)
    for i in inf_lst:
        bound_color = i[0]
        print i
        xy_x = i[1][0][0][0]
        xy_y = i[1][0][0][1]
        lgt = i[1][0][1]
        rect = plt.Rectangle((xy_x, xy_y), lgt, 0.5, fill=True, facecolor=bound_color, edgecolor=bound_color, linewidth=0)
        ax.add_patch(rect)
    s, e, m = partition_double(10)
    s2, e2, m2 = partition_double(-10)
    plt.ylim((-0.25, 0.25))
    plt.xlim((-2150, 2150))
    plt.yticks([])
    plt.xticks([])
    plt.tight_layout()
    # plt.xticks([-2047,s*e+s*m,s2*e2+s2*m2,2047],[r"$-\Omega$","-10","10",r"$\Omega$"],fontsize = 18)
    # print s*e+s*m
    # print s2*e2+s2*m2
    # plt.savefig("graph2/" + fun_name + ".pdf", format="pdf")
    # plt.savefig("papergraph/" + "erfbdvals.svg", format="svg")
    # plt.savefig("papergraph/" + "erfbdvals_local.svg", format="svg")
    plt.savefig("papergraph/" + "erfbdvals_repair.svg", format="svg")
    # plt.close()
    plt.show()

# des_res = bf.load_pickle("detect_res_lst.pkl")
# print des_res[40]
# inter_funcs = bf.load_pickle('fun_index.pkl')
# test_fun = inter_funcs[40]
# print bf.boundary_test(test_fun[0],bf.extract_bound_str([[10,5.019472731517385e+61]]),1)
# name = "localize_res_files/"+test_fun[0]+".pkl"
# res = bf.load_pickle(name)
# a = bf.getulp(5.019472731517385e+61)+5.019472731517385e+61
# print "%.18e" % a
# print res
# eva_bound_lst = bf.load_pickle("eva_bound_lst.plk")
# print eva_bound_lst[40]
# eva_lst = eva_bound_lst[40][2:] + [[(0,[-2]),[[5.019472731517385e+61,bf.f64max]]],[(0,[-2]),[[-bf.f64max,-5.019472731517385e+61]]]]
# print partition_double(-10)
# print partition_double(bf.f64max)
# plot_1func_domain_example(eva_lst)
# plot_1func_domain_example(eva_bound_lst[40][2:])
def plot_2vfunc_domain(plot_lst):
    inf_lst = extract_information2v(plot_lst)
    fig = plt.figure(figsize=(10, 10))
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)
    # fun_name = inf_lst[1]
    for i in inf_lst:
        bound_color = i[0]
        # print i
        xy_x = i[1][0][0][0]
        xy_y = i[1][0][0][1]
        lgt = i[1][0][1]
        hgt = i[1][0][2]
        rect = plt.Rectangle((xy_x, xy_y), lgt, hgt, fill=True, facecolor=bound_color, edgecolor='red', linewidth=0)
        ax.add_patch(rect)
    # plt.ylim((-0.25, 0.25))
    plt.xlim((-2150, 2150))
    plt.ylim((-2150, 2150))
    plt.show()
    # plt.savefig("graph2/" + fun_name + ".pdf", format="pdf")
    # plt.savefig("graph/" + fun_name + ".png", format="png")
    # plt.close()
# plot_2vfunc_domain([14, 'gsl_sf_bessel_Jnu_e', [(0, [1]), [[-1.7976931348623157e+308, 0.0], [-1.7976931348623157e+308, -0.0]]], [(556, [0, 1, 11, 15, 16]), [[-1.7976931348623157e+308, 0.0], [-0.0, 1.7976931348623157e+308]]], [(0, [1]), [[0.0, 1.7976931348623157e+308], [-1.7976931348623157e+308, -0.0]]], [(439, [0, 11, 15, 16]), [[0.0, 1.7976931348623157e+308], [-0.0, 1.7976931348623157e+308]]]])


# plot_1func_domain(plot_lst_sum[0])
# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(1,1,1)
# rect = plt.Rectangle((0.1,0.1), 0.5, 0.3, fill=False, edgecolor = 'red',linewidth=1)
# ax.add_patch(rect)
# plt.show()



# fig = plt.figure(figsize=(30, 1))
# ax = SubplotZero(fig, 111)
# fig.add_subplot(ax)
# rect = plt.Rectangle((-2048,-0.25), 4096, 0.5, fill=True,facecolor = 'yellow', edgecolor = 'red',linewidth=0)
# ax.add_patch(rect)
# plt.ylim((-0.25,0.25))
# plt.xlim((-2150,2150))
# for direction in ["xzero", "yzero"]:
#     # adds arrows at the ends of each axis
#     ax.axis[direction].set_axisline_style("->")
#
#     # adds X and Y-axis from the origin
#     ax.axis[direction].set_visible(True)
# #
# for direction in ["left", "right", "bottom", "top"]:
#     # hides borders
#     ax.axis[direction].set_visible(False)
# ax.axis["yzero"].set_visible(True)
# # x = np.linspace(-0.5, 1., 100)
# # ax.plot(x, np.sin(x*np.pi))
# #
# plt.show()
#
# x=np.linspace(-3,3,50)
# y1=2*x+1
# y2=x**2
#
# plt.figure(num=3,figsize=(5,6))
# plt.plot(x,y2)
# plt.plot(x,y1,color='red',linewidth=1.0,linestyle='--')
# plt.xlim((-1,2))
# plt.ylim((-2,3))
# plt.xlabel('x')
# plt.ylabel('y')
#
# plt.xticks(np.linspace(-1,2,5))
# plt.yticks([-2,-1.8,0,1.5,3],\
#          [r'$really\ bad$',r'$bad$',r'$normal$',r'$good$',r'$perfect$'])
#
# ax=plt.gca()
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
#
# ax.xaxis.set_ticks_position('bottom')
# ax.yaxis.set_ticks_position('left')
#
# ax.spines['bottom'].set_position(('data',0 ))
# ax.spines['left'].set_position(('data',0))
# ax.spines['left'].set_axisline_style('->')
#
# plt.show()

