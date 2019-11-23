/*
1. add index for each floating-point instruction
2. check fpnan after each floating-point instruction

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
  struct FPfpnanPass : public ModulePass {
  public:
    static char ID;

    FPfpnanPass() : ModulePass(ID) {
    }

    ~FPfpnanPass() {
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
    int getFPmathFid(std::string funcName)
    {
        int fid = 0;
        if(funcName.compare("sqrt")==0){
            fid = 1;
        }
        if(funcName.compare("acos")==0){
            fid = 2;
        }
        if(funcName.compare("acosh")==0){
            fid = 3;
        }
        if(funcName.compare("asin")==0){
            fid = 4;
        }
        if(funcName.compare("atanh")==0){
            fid = 5;
        }
        if(funcName.compare("log")==0){
            fid = 6;
        }
        if(funcName.compare("log1p")==0){
            fid = 7;
        }
        if(funcName.compare("pow")==0){
            fid = 8;
        }
        return fid;
    }

    int checkFunction(Function &currFunc,
        int w_ids, GlobalVariable &gl_w,
        GlobalVariable &gl_idx, GlobalVariable &gl_cidx,
        Function &gl_fpnanFun, GlobalVariable &gl_stflag,
        std::string scallsFuncs[],int call_size) {
      std::string funcName = "NONAME";
      int flag = 0;
      if(currFunc.hasName()) {
        funcName = currFunc.getName();
      }
      int stop_call_flag = 0;
//      if(w_ids==1){
        dbgs() << "[+] Insert fpnan analysis code in function:" << funcName << "\n";
        dbgs() << "[-] w_ids:" << w_ids << "\n";
//      }

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
                    if(CallfuncName.compare("fpfpnan")!=0){
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
                            cnt_idx = checkFunction(*callFunc, w_ids, gl_w, gl_idx, gl_cidx, gl_fpnanFun,gl_stflag,callsFuncs2,call_size2);
                        }
                    }
                }

              }
              if (isCallFPOperation(inst)) {
                if (CallInst *callInst = dyn_cast<CallInst>(&currIns)) {
                    int fid = 0;
                    Function *callFunc = callInst -> getCalledFunction();
                    w_ids = cnt_idx;
                    std::string FPfuncName = "NONAME";
                    std::string temp_str = " ";
//                    if(callFunc -> isDeclaration()){
                        if(callFunc -> hasName()) {
                            FPfuncName = callFunc -> getName();
                        }
//                        dbgs() << "[-] isCallFPOperation:" << FPfuncName << "\n";
                        fid = getFPmathFid(FPfuncName);
//                        dbgs() << "[-] fid:" << fid << "\n";
                        if(fid!=0){
                            IRBuilder<> builder(inst);
                            builder.SetInsertPoint(&currBB, builder.GetInsertPoint());
                            one = ConstantInt::get(builder.getInt32Ty(), cnt_idx);
                            cnt = ConstantInt::get(builder.getInt32Ty(), fid);
                            Type * DouType = builder.getDoubleTy();
                            Value* arg1 = callInst->getArgOperand(0);
                            if(fid==8){
                                Value* arg2 = callInst->getOperand(1);
                                builder.CreateCall(&gl_fpnanFun, ArrayRef< Value* > {one,&gl_w,&gl_cidx,arg1,arg2,cnt,&gl_stflag});
                            }else{
                                builder.CreateCall(&gl_fpnanFun, ArrayRef< Value* > {one,&gl_w,&gl_cidx,arg1,zero,cnt,&gl_stflag});
                            }
                            cnt_idx = cnt_idx + 1;
                        }
//                    }
                }
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
      Function *gl_fpnanFun = m.getFunction("fpnan");
      GlobalVariable *gl_sumins = m.getGlobalVariable("sum_ins");
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
                w_ids = checkFunction(currFunc, w_ids, *gl_w, *gl_idx, *gl_cidx, *gl_fpnanFun,*gl_stflag,callsFuncs,call_size);
            }
        }
      }
      ConstantInt* const_int_val = ConstantInt::get(m.getContext(), APInt(32,w_ids));
      gl_sumins -> setInitializer(const_int_val);
      // we change the module.
      return true;
    }

  };

  char FPfpnanPass::ID = 0;
  // pass arg, pass desc, cfg_only, analysis only
  static RegisterPass<FPfpnanPass> x("fpnan",
                                              "Insert fpnan check for each fp instruction.",
                                                    true,
                                                    true);
}
