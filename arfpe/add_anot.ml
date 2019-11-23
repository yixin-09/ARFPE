open Cil_types
open Cil


let emitter = Emitter.create "addnotat" [ Emitter.Funspec ]
    ~correctness:[] ~tuning:[]

let count = ref 0
let floats_of_string s = List.map float_of_string (Str.split (Str.regexp "[, \t]+") s)

class print_adnt fn a = object
   inherit Visitor.frama_c_inplace
   method! vglob_aux g =
       match g with
        | GFun(f, _) ->
           let gfn = f.svar.vname in
           let kf2 = Globals.Functions.get f.svar in
           if (Kernel_function.is_definition kf2)&(gfn=fn)&(!count=0)  then
           begin
            let formals_var = Kernel_function.get_formals kf2 in
            let rec add_pre kf ss_var = match ss_var with
              | [] -> ()
              | c_var::c_vars ->
                match c_var.vtype with
                | TFloat _ ->
                    if (!count <= (List.length a))&(a!=[]) then
                    begin
                        let l_var = Cil.cvar_to_lvar c_var in
                        let var_term = Logic_const.tvar l_var in
                        let flval = List.nth a !count in
                        let add_idx = !count + 1 in
                        let flval2 = List.nth a add_idx in
                        let cnst_term = Logic_const.treal flval in
                        let cnst_term2 = Logic_const.treal flval2 in
                        let eq_pred = Logic_const.prel (Cil_types.Rgt, var_term, cnst_term) in
                        let eq_pred2 = Logic_const.prel (Cil_types.Rlt, var_term, cnst_term2) in
                        let pred = Logic_const.new_predicate eq_pred in
                        let pred2 = Logic_const.new_predicate eq_pred2 in
                        let bname = Cil.default_behavior_name in
                        count := !count + 2;
                        Annotations.add_requires emitter kf ~behavior:bname [pred;pred2];
                    end;
                        add_pre kf c_vars
                | TInt _ ->
                    if (!count <= (List.length a))&(a!=[]) then
                    begin
                        let l_var = Cil.cvar_to_lvar c_var in
                        let var_term = Logic_const.tvar l_var in
                        let flval = List.nth a !count in
                        let add_idx = !count + 1 in
                        let flval2 = List.nth a add_idx in
                        let cnst_term = Logic_const.tinteger (int_of_float flval) in
                        let cnst_term2 = Logic_const.tinteger (int_of_float flval2) in
                        let eq_pred = Logic_const.prel (Cil_types.Rgt, var_term, cnst_term) in
                        let eq_pred2 = Logic_const.prel (Cil_types.Rlt, var_term, cnst_term2) in
                        let pred = Logic_const.new_predicate eq_pred in
                        let pred2 = Logic_const.new_predicate eq_pred2 in
                        let bname = Cil.default_behavior_name in
                        count := !count + 2;
                        Annotations.add_requires emitter kf ~behavior:bname [pred;pred2];
                    end;
                        add_pre kf c_vars
                | _ ->
                    if c_var.vname = "mode" then
                    begin
                        let l_var = Cil.cvar_to_lvar c_var in
                        let var_term = Logic_const.tvar l_var in
                        let cnst_term = Logic_const.tinteger 0 in
                        let eq_pred = Logic_const.prel (Cil_types.Req, var_term, cnst_term) in
                        let pred = Logic_const.new_predicate eq_pred in
                        let bname = Cil.default_behavior_name in
                        Annotations.add_requires emitter kf ~behavior:bname [pred];
                    end;
                        add_pre kf c_vars
            in
            add_pre kf2 formals_var;Cil.DoChildren
           end
           else
           begin
           (*Format.fprintf out "%s and %s \n" gfn fn;*)
           Cil.DoChildren
           end
        | _ -> Cil.SkipChildren
end
(*Callgraph.Uses.iter_on_callees (fun cae -> fmt Cil_types_debug.pp_kernel_function  cae) kf; Cil.SkipChildren*)
(*fmtt Cvalue.Model.pretty_filter  (Locations.zone_of_varinfo s);*)
(*(Cil_types_debug.pp_kernel_function Callgraph.Cg_viewer.get_current_function () <> None);*)
module Self = Plugin.Register(struct
    let name = "addnotat"
    let shortname = "addnotat"
    let help = "add requires for eva analysis"
end)
module Enabled = Self.False(struct
    let option_name = "-adnt"
    let help =
        "when on (off by default), add requires for eva analysis"
end)
module DomainStr = Self.String(struct
    let option_name = "-DomainStr"
    let default = " "
    let arg_name = "domain string"
    let help = "domain list in string"
end)

module MainName = Self.String(struct
    let option_name = "-adnt-fun"
    let default = "main"
    let arg_name = "fun-name"
    let help = "main function name"
end)

let run () =
    if Enabled.get() then
        let domainStr = DomainStr.get () in
        let domain_list = floats_of_string domainStr in
        let funname = MainName.get () in
        Visitor.visitFramacFileSameGlobals (new print_adnt funname domain_list) (Ast.get ())

let () = Db.Main.extend run
