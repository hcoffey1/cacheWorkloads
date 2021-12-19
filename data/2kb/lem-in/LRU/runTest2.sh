#!/bin/bash

~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../../python/simple_ruby.py ../../lem-in --input="../../maps/big_superposition" --rp=LRURP

mv m5out lem_LRU_2KB

#~/proj/cs752/cache/gem5Public/gem5/build/X86/gem5.opt ../../../python/simple_ruby.py ../lem-in --input="../maps/big_superposition" --rp=TreePLRURP

#mv m5out lem_TREEPLRU
