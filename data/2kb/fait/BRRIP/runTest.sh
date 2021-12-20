#!/bin/bash

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=BRRIPRP

mv m5out fait_BRRIP

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=LRURP

mv m5out fait_LRU

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=RandomRP

mv m5out fait_Random

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=SecondChanceRP

mv m5out fait_SecondChance

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=TreePLRURP

mv m5out fait_TreePLRU

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=RRIPRP

mv m5out fait_RRIP


~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../src/sequential/c/run_float --options="../matrices/bcspwr10/bcspwr10.mtx" --rp=LFURP

mv m5out fait_LFU
