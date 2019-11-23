import sys
import basic_func as bf

fid_lc = [2, 3, 5, 10, 26, 34, 35, 36, 37, 39, 40, 41, 42, 45, 46, 47, 48, 49, 50, 51, 52, 53, 59, 63, 66, 67, 69, 70, 73, 74, 75, 80, 84, 85, 92, 100, 101, 102, 108, 118, 128, 132, 147]




def convertToC_1v(repair_lst,name,var_name):
    print "Cover To C code"
    orig_stdout = sys.stdout
    fun_name = name + ''
    name = 'patch_of_'+name
    f = open('patches/'+name+'.c', 'w')
    name = name.split("gsl_")[1]
    sys.stdout = f
    idx = 1
    for rep_lst in repair_lst[:-1]:
        lcbds = rep_lst[1]
        len_bd = len(lcbds)*2
        print 'static double array_idx_'+name+'_'+str(idx)+'[' + str(len_bd) + '] = {'
        for lbd in lcbds:
            print "%.18e," % lbd[0][0]
            print "%.18e," % lbd[0][1]
        print "};"
        print "int find_bd_" + name + '_' + str(idx) + "(double x)"
        print "{"
        print " int len_glob = " + str(len_bd) + ";"
        print " int idx = 0;"
        print " while((idx>=0)&&(idx<len_glob)){"
        print "     if((x>=array_idx_" + name + '_' + str(idx) + "[idx])&&(x<=array_idx_" + name + '_' + str(idx) + "[idx+1])){"
        print "         return 1;"
        print "     }"
        print "     idx = idx + 2;"
        print " }"
        print " return 0;"
        print "}"
        idx = idx + 1
    idx = 1
    print "int find_id_"+name+"(double x)"
    print "{"
    for rep_lst in repair_lst[:-1]:
        bound = rep_lst[0]
        # lcbds = rep_lst[1]
        # rep_code = rep_lst[2]
        print "if((x<=" + repr(bound[0][1]) + ")&&(x>=" + repr(bound[0][0]) + ")){"
        print " return " + str(idx) + ";"
        print "}"
        idx = idx + 1
    print "}"
    sys.stdout = orig_stdout
    f.close()
    f = open('patches/insert_code/' + fun_name + '.c', 'w')
    sys.stdout = f
    print "int axs = find_id_"+name+"(" + var_name + ");"
    idx = 1
    for rep_lst in repair_lst[:-1]:
        print "if(axs=="+repr(idx)+"){"
        print " if(find_bd_" + name + '_' + str(idx) + "(" + var_name + ")){"
        for rep_str in rep_lst[2]:
            print "    " + rep_str
        print " }"
        print "}"
        idx = idx + 1
    sys.stdout = orig_stdout
    f.close()




def convertToC_2v(repair_lst,name,var_name):
    print "Cover To C code"
    orig_stdout = sys.stdout
    fun_name = name
    name = 'patch_of_'+name
    f = open('patches/'+name+'.c', 'w')
    name = name.split("gsl_")[1]
    sys.stdout = f
    idx = 1
    for rep_lst in repair_lst[:-1]:
        lcbds = rep_lst[1]
        len_bd = len(lcbds)*2
        print 'static double array_idx_'+name+'_'+str(idx)+'[' + str(len_bd) + '] = {'
        for lbd in lcbds:
            print "%.18e," % lbd[0][0]
            print "%.18e," % lbd[0][1]
        print "};"
        print 'static double array_idy_' + name + '_' + str(idx) + '[' + str(len_bd) + '] = {'
        for lbd in lcbds:
            print "%.18e," % lbd[1][0]
            print "%.18e," % lbd[1][1]
        print "};"
        print "int find_bd_" + name + '_' + str(idx) + "(double x,double y)"
        print "{"
        print " int len_glob = " + str(len_bd) + ";"
        print " int idx = 0;"
        print " while((idx>=0)&&(idx<len_glob)){"
        print "     if((x>=array_idx_" + name + '_' + str(idx) + "[idx])&&(x<=array_idx_" + name + '_' + str(idx) + "[idx+1])){"
        print "     if((y>=array_idy_" + name + '_' + str(idx) + "[idx])&&(y<=array_idy_" + name + '_' + str(idx) + "[idx+1])){"
        print "         return 1;"
        print "     }"
        print "     idx = idx + 2;"
        print " }"
        print " return 0;"
        print "}"
        print "}"
        idx = idx + 1
    idx = 1
    print "int find_id_"+name+"(double x, double y)"
    print "{"
    for rep_lst in repair_lst[:-1]:
        bound = rep_lst[0]
        # lcbds = rep_lst[1]
        # rep_code = rep_lst[2]
        print "if((x<=" + repr(bound[0][1]) + ")&&(x>=" + repr(bound[0][0]) + ")){"
        print " if((y<=" + repr(bound[1][1]) + ")&&(y>=" + repr(bound[1][0]) + ")){"
        print "     return " + str(idx) + ";"
        print " }"
        print "}"
        idx = idx + 1
    print "}"
    sys.stdout = orig_stdout
    f.close()
    f = open('patches/insert_code/' + fun_name + '.c', 'w')
    sys.stdout = f
    print "int axs = find_id_" + name + "(" + var_name + ");"
    idx = 1
    for rep_lst in repair_lst[:-1]:
        print "if(axs==" + repr(idx) + "){"
        print " if(find_bd_" + name + '_' + str(idx) + "(" + var_name + ")){"
        for rep_str in rep_lst[2]:
            print "    " + rep_str
        print " }"
        print "}"
        idx = idx + 1
    sys.stdout = orig_stdout
    f.close()



inter_funcs = bf.load_pickle('fun_index.pkl')
for i in fid_lc:
    test_fun = inter_funcs[i]
    print test_fun
    var_num = bf.get_var_num(test_fun)
    name = "localize_res_files/" + test_fun[0] + ".pkl"
    name2 = "repair_res_files/" + test_fun[0] + ".pkl"
    repair_res = bf.load_pickle(name2)
    print len(repair_res)
    print repair_res

    if var_num == 1:
        var_name = test_fun[1][0][1]
        convertToC_1v(repair_res, test_fun[0],var_name)
    else:
        var_name = test_fun[1][0][1] + "," + test_fun[1][1][1]
        if (test_fun[0] == "gsl_sf_lnbeta_e") | (test_fun[0] == "gsl_sf_beta_e"):
            var_name = 'x,y'
        convertToC_2v(repair_res, test_fun[0],var_name)