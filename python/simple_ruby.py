# -*- coding: utf-8 -*-
# Copyright (c) 2015 Jason Power
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

""" This file creates a barebones system and executes 'hello', a simple Hello
World application.
See Part 1, Chapter 2: Creating a simple configuration script in the
learning_gem5 book for more information about this script.

IMPORTANT: If you modify this file, it's likely that the Learning gem5 book
           also needs to be updated. For now, email Jason <power.jg@gmail.com>

"""

# File modified to use Ruby


gem5Path="/home/hayden/proj/cs752/cache/gem5Public/gem5/configs"

import sys
sys.path.insert(0, gem5Path)

import m5
import argparse
from m5.objects import *
from ruby_caches import MyCacheSystem
from common.ObjectList import ObjectList

# Make a list of all replcacement policies
rp_list = ObjectList(m5.objects.BaseReplacementPolicy)

# Add argparse
parser = argparse.ArgumentParser(description='Test replacement policies',
                                 formatter_class=argparse.RawTextHelpFormatter)

# Help messages for replacement policies
rp_help = '''Replacement policies for ruby/classic system. Optional
replacement policies are:
'''
rp_help += '\n'.join(rp_list.get_names())
parser.add_argument("binary", default="", nargs="+", type=str, help="Binary to execute.")
parser.add_argument("--cpu", type=str, help="CPU type. Default: DerivO3CPU.")
parser.add_argument('--rp', metavar='rp', help=rp_help, default='LRURP')
parser.add_argument("--options", type=str, help="Command line args")
args = parser.parse_args()
# create the system we are going to simulate
system = System()

# Set the clock fequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('512MB')] # Create an address range

# Create a simple CPU
if not args.cpu:
    system.cpu = DerivO3CPU()
else:
    system.cpu = eval(args.cpu + "()")

# create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]

# Create the (Ruby based) cache system and set up all of the caches
system.caches = MyCacheSystem()
system.caches.setup(system, system.cpu, [system.mem_ctrl],
                                                    rp_list.get(args.rp)())

# get ISA for the binary to run.
isa = str(m5.defines.buildEnv['TARGET_ISA']).lower()

# Default to running 'hello', use the compiled ISA to find the binary
# grab the specific path to the binary
thispath = os.path.dirname(os.path.realpath(__file__))

binary = None
if args.binary:
    binary = args.binary

if args.options:
    binary = binary + [args.options]


#binary = os.path.join(thispath, '../../',
#                      'tests/test-progs/hello/bin/', isa, 'linux/hello')
system.workload = SEWorkload.init_compatible(binary[0])

# Create a process for a simple "Hello World" application
process = Process()
# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = [binary[0]]
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))