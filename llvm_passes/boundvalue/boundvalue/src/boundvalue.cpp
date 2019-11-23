/*
1. add index for each floating-point instruction
2. check overflow after each floating-point instruction

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
  struct BoundaryAnalysisPass : public ModulePass {
  public:
    static char ID;

    BoundaryAnalysisPass() : ModulePass(ID) {
    }

    ~BoundaryAnalysisPass() {
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
        Function &gl_boundaryFun, GlobalVariable &gl_stflag,
        std::string scallsFuncs[],int call_size, int call_num) {
      std::string funcName = "NONAME";
      int flag = 0;
      if(currFunc.hasName()) {
        funcName = currFunc.getName();
      }
      int stop_call_flag = 0;
      dbgs() << "[+] Insert boundary analysis code in function:" << funcName << "\n";
      int call_limit = 1;
      if((w_ids == 1)&&(call_num==1)){
        call_limit = 2;
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
      LoopInfo &LI = getAnalysis<LoopInfoWrapperPass>(currFunc).getLoopInfo();
      for(auto &currBB: currFunc) {
        int flag = 0;
        for(LoopInfo::iterator L = LI.begin(), e = LI.end(); L!=e; ++L) {
            Loop *L2=*L;
            if(L2 -> contains(&currBB)){
              flag = 1;
            }
        }
        if(flag==0){
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
                    if(CallfuncName.compare("BoundaryAnalysis")!=0){
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
                        callsFuncs2[call_size] = CallfuncName;
                        call_size2 = call_size + 1;
                        if((stop_call_flag!=1)&&(call_size2<call_limit)){
                            cnt_idx = checkFunction(*callFunc, w_ids, gl_w, gl_idx, gl_cidx, gl_boundaryFun,gl_stflag,callsFuncs2,call_size2,call_num);
                        }
                    }
                }

              }
              if (auto *op = dyn_cast<FCmpInst>(&currIns)) {
                IRBuilder<> builder(op);
                builder.SetInsertPoint(&currBB, builder.GetInsertPoint());
                Type * DouType = builder.getDoubleTy();
                Type * IntType = builder.getInt32Ty();
                Value * pt_glw = gl_w.stripPointerCasts();
                Value * pt_glidx = gl_idx.stripPointerCasts();
                Value* lhs = op->getOperand(0);
                Value* rhs = op->getOperand(1);
                Value* s1 = builder.CreateFSub(lhs, rhs);
                one = ConstantInt::get(builder.getInt32Ty(), cnt_idx);
                builder.CreateCall(&gl_boundaryFun, ArrayRef< Value* > {one,&gl_w,&gl_cidx,s1,&gl_stflag});
                cnt_idx = cnt_idx + 1;
              }
            }
        }
       }
      return cnt_idx;
    }
    int getCallees(Function &currFunc){
        int call_num = 1;
        int call_num2 = 1;
        for(auto &currBB: currFunc) {
            for(auto &currIns: currBB) {
              if (auto *op = dyn_cast<FCmpInst>(&currIns)) {
                call_num = call_num + 1;
              }
              if (CallInst *callInst = dyn_cast<CallInst>(&currIns)) {
                Function *callFunc = callInst -> getCalledFunction();
                if(!(callFunc -> isDeclaration())) {
                    call_num2 = call_num2 + 1;
                }
              }

            }
        }
        if((call_num<=3)&&(call_num2<=3)){
            return 1;
        }else{
            return 0;
        }
//        return call_num;
    }

    bool runOnModule(Module &m) override {
      int w_ids = 1;
      int call_size = 0;
      int calls_num = 0;
      GlobalVariable *gl_w = m.getGlobalVariable("w");
      GlobalVariable *gl_idx = m.getGlobalVariable("idx");
      GlobalVariable *gl_cidx = m.getGlobalVariable("cidx");
      GlobalVariable *gl_stflag = m.getGlobalVariable("stflag");
      GlobalVariable *gl_sumins = m.getGlobalVariable("sum_ins");
      Function *gl_boundaryFun = m.getFunction("BoundaryAnalysis");
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
                calls_num = getCallees(currFunc);
                w_ids = checkFunction(currFunc, w_ids, *gl_w, *gl_idx, *gl_cidx, *gl_boundaryFun,*gl_stflag,callsFuncs,call_size,calls_num);
            }
        }
      }
      ConstantInt* const_int_val = ConstantInt::get(m.getContext(), APInt(32,w_ids));
      gl_sumins -> setInitializer(const_int_val);
      // we change the module.
      return true;
    }

  };

  char BoundaryAnalysisPass::ID = 0;
  // pass arg, pass desc, cfg_only, analysis only
  static RegisterPass<BoundaryAnalysisPass> x("boundvalue",
                                              "Identify all the direct access to struct members.",
                                                    true,
                                                    true);
}
