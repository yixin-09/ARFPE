/*
1. add index for each floating-point instruction
2. check dividezero after each floating-point instruction

*/
#include <llvm/Pass.h>
#include <llvm/IR/Function.h>
#include <llvm/Support/raw_ostream.h>
#include <llvm/IR/LegacyPassManager.h>
#include <llvm/IR/Instructions.h>
#include <llvm/IR/ValueSymbolTable.h>
#include <iostream>
#include <string>
#include <llvm/Support/Debug.h>
#include <llvm/IR/Module.h>
#include "llvm/IR/IRBuilder.h"
#include "llvm/ADT/Statistic.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/InstrTypes.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include "llvm/IR/IntrinsicInst.h"
#include "llvm/IR/Module.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Analysis/LoopInfo.h"


using namespace llvm;

static llvm::cl::opt<std::string> InputFilename("dr_fun", cl::desc("Specify input filename for mypass"), cl::value_desc("filename"));

namespace {


  /***
   * This pass detects all direct accesses to struct members.
   */
  struct FPdividezeroPass : public ModulePass {
  public:
    static char ID;

    FPdividezeroPass() : ModulePass(ID) {
    }

    ~FPdividezeroPass() {
    }
    void getAnalysisUsage(AnalysisUsage &AU) const override {
      AU.addRequired<LoopInfoWrapperPass>();
    }
    IRBuilder<> createBuilderAfter(Instruction *inst)
    {
        // Get next instruction
      BasicBlock::iterator tmpIt(inst);
      tmpIt++;
      Instruction *nextInst = &(*(tmpIt));
      assert(nextInst && "Invalid instruction!");

        IRBuilder<> builder(nextInst);

        return builder;
    }
    bool isFPOperation(const Instruction *inst)
    {
        return (
                (inst->getOpcode() == Instruction::FMul) ||
                (inst->getOpcode() == Instruction::FDiv) ||
                (inst->getOpcode() == Instruction::FAdd) ||
                (inst->getOpcode() == Instruction::FSub)
                     );
    }

    bool isCallFPOperation(const Instruction *inst)
    {
        if(isa<CallInst>(inst)){
            return inst->getType()->isDoubleTy();
        }
        return 0;
    }

    int checkFunction(Function &currFunc,
        int w_ids, GlobalVariable &gl_w,
        GlobalVariable &gl_idx, GlobalVariable &gl_cidx,
        Function &gl_divzero, GlobalVariable &gl_stflag,
        std::string scallsFuncs[],int call_size) {
      std::string funcName = "NONAME";
      int flag = 0;
      if(currFunc.hasName()) {
        funcName = currFunc.getName();
      }
      int stop_call_flag = 0;
      if(w_ids==1){
        dbgs() << "[+] Insert dividezero analysis code in function:" << funcName << "\n";
        dbgs() << "[-] w_ids:" << w_ids << "\n";
      }

      BasicBlock &entblock = currFunc.getEntryBlock();
      Value *cnt, *one,*zero;
      int count = 0;
      for(auto &encurrIns: entblock) {
          if(count == 0){
              IRBuilder<> builder0(&encurrIns);
              builder0.SetInsertPoint(&encurrIns);
//              cnt = builder0.CreateAlloca(builder0.getInt32Ty(), nullptr, "cnt");
              one = ConstantInt::get(builder0.getInt32Ty(), w_ids);
              zero = ConstantFP::get(builder0.getDoubleTy(), 0.0);
//              builder0.CreateStore(one, cnt);
          }
          count = count + 1;
      }
      int cnt_idx = w_ids;
      for(auto &currBB: currFunc) {
            for(auto &currIns: currBB) {
              Instruction *inst = &currIns;
              Value * returnval;
              stop_call_flag = 0;
              if (CallInst *callInst = dyn_cast<CallInst>(&currIns)) {
                std::string callsFuncs2[100]={};
                int call_size2 = 0;
                Function *callFunc = callInst -> getCalledFunction();
                w_ids = cnt_idx;
                std::string CallfuncName = "NONAME";
                std::string temp_str = " ";
                if(callFunc -> hasName()) {
                    CallfuncName = callFunc -> getName();

                }
                if(!(callFunc -> isDeclaration())) {
                    if(CallfuncName.compare("fpdividezero")!=0){
//                        dbgs() << "[-] call_size:" << call_size << "\n";
//                        dbgs() << "[-] CallfuncName:" << CallfuncName << "\n";
                        for(int i=0;i<call_size;i++){
//                            dbgs() << "[-] calls functions:" << scallsFuncs[i] << "\n";
                            if(CallfuncName.compare(scallsFuncs[i])==0){
                                stop_call_flag = 1;
                            }
                            callsFuncs2[i] = scallsFuncs[i];
                        }
//                        dbgs() << "[-] stop_call_flag:" << stop_call_flag << "\n";
//                        scallsFuncs[call_size] = CallfuncName;
                        callsFuncs2[call_size] = CallfuncName;
                        call_size2 = call_size + 1;
//                        dbgs() << "[-] call_size:" << call_size2 << "\n";
                        if((stop_call_flag!=1)&&(call_size2<7)){
                            cnt_idx = checkFunction(*callFunc, w_ids, gl_w, gl_idx, gl_cidx, gl_divzero,gl_stflag,callsFuncs2,call_size2);
//                            for(int i=0;i<call_size2;i++){
//                                scallsFuncs[i] = " ";
//                            }
//                            scallsFuncs[call_size2] = "";
//                            call_size = call_size2 - 1;
                        }
                    }
                }

              }
              if (inst->getOpcode() == Instruction::FDiv) {
                IRBuilder<> builder(inst);
                builder.SetInsertPoint(&currBB, builder.GetInsertPoint());
                Type * DouType = builder.getDoubleTy();
                Value* lhs = inst->getOperand(0);
                Value* rhs = inst->getOperand(1);
//                builder.SetInsertPoint(&currBB, builder.GetInsertPoint());
//                Type * IntType = builder.getInt32Ty();
                one = ConstantInt::get(builder.getInt32Ty(), cnt_idx);
//                builder.CreateStore(one, cnt);
//                Value* scnt = builder.CreateLoad(IntType,cnt);&gl_idx,
//                returnval = cast<Value>(inst);
                int flag = 0;
                if (llvm::ConstantFP* CI = dyn_cast<llvm::ConstantFP>(rhs)) {
                  flag = 1;
                }
                if(flag == 0){
                    builder.CreateCall(&gl_divzero, ArrayRef< Value* > {one,&gl_w,&gl_cidx,rhs,&gl_stflag});
                }

//                Value * pt_glw = gl_w.stripPointerCasts();
//                Value* sw = builder.CreateLoad(DouType,pt_glw);
//                Value *cond = builder.CreateFCmpOEQ(sw,zero);
//                Type* rt = currFunc.getReturnType();
//                if(Type* rtt = dyn_cast<void>(&rt)){
//                    ret_stat = builder.CreateRet();
//                }else{
//                    if(Type* rtt = dyn_cast<double>(&rt)){
//                        ret_stat = builder.CreateRet(0.0);
//                    }
//                    if(Type* rtt = dyn_cast<int>(&rt)){
//                        ret_stat = builder.CreateRet(0);
//                    }
//                }
//                ReturnInst *ret_stat = builder.CreateRet(0);
//                Instruction *nextInstr = inst->getNextNode();
//                Function *TheFunction = builder.GetInsertBlock()->getParent();
//                LLVMContext& context = TheFunction -> getContext();
//                BasicBlock *ThenBB =
//                    BasicBlock::Create(context, "then", TheFunction);
//                SplitBlockAndInsertIfThen(cond,ret_stat,true);
                cnt_idx = cnt_idx + 1;
              }

            }
       }
      return cnt_idx;
    }

    bool runOnModule(Module &m) override {
      int w_ids = 1;
      int call_size = 0;
      GlobalVariable *gl_w = m.getGlobalVariable("w");
      GlobalVariable *gl_idx = m.getGlobalVariable("idx");
      GlobalVariable *gl_cidx = m.getGlobalVariable("cidx");
      GlobalVariable *gl_stflag = m.getGlobalVariable("stflag");
      GlobalVariable *gl_sumins = m.getGlobalVariable("sum_ins");
      Function *gl_divzero = m.getFunction("divzero");
      // iterate through all the functions.
      for (auto &currFunc: m) {
        std::string funcName = "NONAME";
        std::string callsFuncs[100]={};
        if(currFunc.hasName()) {
            funcName = currFunc.getName();
        }
        // if this is not a declaration.
        if(!currFunc.isDeclaration()) {
            if(funcName.compare(InputFilename)==0){
                w_ids = checkFunction(currFunc, w_ids, *gl_w, *gl_idx, *gl_cidx, *gl_divzero,*gl_stflag,callsFuncs,call_size);
            }
        }
      }
      ConstantInt* const_int_val = ConstantInt::get(m.getContext(), APInt(32,w_ids));
      gl_sumins -> setInitializer(const_int_val);
      // we change the module.
      return true;
    }

  };

  char FPdividezeroPass::ID = 0;
  // pass arg, pass desc, cfg_only, analysis only
  static RegisterPass<FPdividezeroPass> x("dividezero",
                                              "Insert dividezero check for each fp instruction.",
                                                    true,
                                                    true);
}
