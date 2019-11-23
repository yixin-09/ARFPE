open Cil_types
open Cil

class print_dps out fn = object
   inherit Visitor.frama_c_inplace
   method! vglob_aux g =
       match g with
        | GFun(f, _) ->Format.fprintf out " ";
           let gfn = f.svar.vname in
           if fn = gfn then
           begin
            let kf = Globals.Functions.get f.svar in
                Format.fprintf out "\n";
                Format.fprintf out "%s \n" fn;
                Format.printf "Error: ";
                Callgraph.Uses.iter_on_callees (fun cae -> Format.fprintf out "%a\n" Printer.pp_varinfo (Globals.Functions.get_vi cae)) kf; Cil.DoChildren
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
    let name = "control flow graph"
    let shortname = "viewcfg"
    let help = "control flow graph computation and display"
end)
module Enabled = Self.False(struct
    let option_name = "-dps"
    let help =
        "when on (off by default), computes the CFG of all functions."
end)
module OutputFile = Self.String(struct
    let option_name = "-dps-output"
    let default = "main.dps"
    let arg_name = "output-file"
    let help = "file where the graph is output, in dot format."
end)

module MainName = Self.String(struct
    let option_name = "-dps-fun"
    let default = "main"
    let arg_name = "fun-name"
    let help = "main function name"
end)

let run () =
    if Enabled.get() then
        let filename = OutputFile.get () in
        let funname = MainName.get () in
        let chan = open_out filename in
        let fmt = Format.formatter_of_out_channel chan in
        Visitor.visitFramacFileSameGlobals (new print_dps fmt funname) (Ast.get ());
        (*(Printer.pp_file fmt) (Ast.get ());*)
        close_out chan
let () = Db.Main.extend run
