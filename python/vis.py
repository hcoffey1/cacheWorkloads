import matplotlib.pyplot as plt
import numpy as np
import os

font = {'family' : 'normal',
	'weight' : 'normal',
	'size' : 12}

plt.rc('font', **font)

class dataPoint:
	epoch = None
	m_demand_misses = None
	m_demand_accesses = None
	ipc = None
	simInsts = None
	simTicks = None
	committedInsts = None

def extractData(dict, dir):
	for file in os.listdir(dir):
		target_dir = dir + file
		target_file = target_dir + "/stats.txt"

		splitFile = file.split("_")
		nameIndex = 0
		if len(splitFile) > 1:
			nameIndex = 1

		dict[splitFile[nameIndex]] = []

		epoch=0
		with open(target_file) as dataFile:
			for line in dataFile:
				if "simTicks" in line:
					tmpDataPoint = dataPoint()
					dict[splitFile[nameIndex]].append(tmpDataPoint)

					tmp = line.split(" ")
					tmp = list(filter(len, tmp))

					dict[splitFile[nameIndex]][-1].simTicks = int(tmp[1])
					
				elif "cpu.committedInsts" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))

					dict[splitFile[nameIndex]][-1].committedInsts = int(tmp[1])

				elif "simInsts" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))

					dict[splitFile[nameIndex]][-1].simInsts = int(tmp[1])

				elif "m_demand_misses" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					dict[splitFile[nameIndex]][-1].epoch = epoch
					dict[splitFile[nameIndex]][-1].m_demand_misses = int(tmp[1])
					epoch += 1
				elif "m_demand_accesses" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					dict[splitFile[nameIndex]][-1].m_demand_accesses = int(tmp[1])
				elif "cpu.ipc" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					dict[splitFile[nameIndex]][-1].ipc = float(tmp[1])

def inst_epoch_ipc(dict, bench, xLabel):
	fig, ax = plt.subplots()
	for key in sorted(dict.keys()):
		print(key)
		x = []
		y = []
		for dp in dict[key]:
			x.append(dp.epoch)
			y.append(dp.ipc)
		ax.plot(x,y, label=key)

	plt.title(bench + ": IPC vs executed instructions")
	plt.xlabel(xLabel)
	plt.ylabel("IPC")
	plt.legend()
	plt.show()


def inst_total_miss_graph(dict, bench, xLabel):
	fig, ax = plt.subplots()
	for key in sorted(dict.keys()):
		print(key)
		x = []
		y = []
		for dp in dict[key]:
			x.append(dp.epoch)
			y.append(dp.m_demand_misses)
		ax.plot(x,y, label=key)

	plt.title(bench + ": Total cache misses vs executed instructions")
	plt.xlabel(xLabel)
	plt.ylabel("Total Misses")
	plt.legend()
	plt.show()

def inst_epoch_missrate_graph(dict, bench, xLabel):
	fig, ax = plt.subplots()
	for key in sorted(dict.keys()):
		print(key)
		x = []
		tmpy = []
		y = []
		acc = []
		tmpAcc = []
		for dp in dict[key]:
			x.append(dp.epoch)
			tmpy.append(dp.m_demand_misses)
			y.append((dp.m_demand_misses))
			tmpAcc.append(dp.m_demand_accesses)
			acc.append(dp.m_demand_accesses)

		y[0] = (y[0]/acc[0])*100
		for i in x[1:]:
			y[i] = (tmpy[i] - tmpy[i-1])
			acc[i] = (tmpAcc[i] - tmpAcc[i-1])
			y[i] = (y[i]*1.0/acc[i])*100
		ax.plot(x,y, label=key)

	plt.title(bench + ": Miss rate (%) per executed epoch")
	plt.xlabel(xLabel)
	plt.ylabel("Miss Rate %")
	plt.legend()
	plt.show()

def inst_epoch_mpki_graph(dict, bench, xLabel):
	fig, ax = plt.subplots()
	for key in sorted(dict.keys()):
		print(key)
		x = []
		tmpy = []
		y = []
		acc = []
		tmpAcc = []
		for dp in dict[key]:
			x.append(dp.epoch)
			tmpy.append(dp.m_demand_misses)
			y.append((dp.m_demand_misses))
			tmpAcc.append(dp.simInsts)
			acc.append(dp.simInsts)

		y[0] = (y[0]/acc[0])*1000
		for i in x[1:]:
			y[i] = (tmpy[i] - tmpy[i-1])
			acc[i] = (tmpAcc[i] - tmpAcc[i-1])
			y[i] = (y[i]*1.0/acc[i])*1000
		ax.plot(x,y, label=key)

	plt.title(bench + ": MPKI per executed epoch")
	plt.xlabel(xLabel)
	plt.ylabel("MPKI")
	plt.legend()
	plt.show()

def bar_total_rel_miss_graph(dict, bench, xLabel):
	fig, ax = plt.subplots()
	y = []
	for key in sorted(dict.keys()):
		print(key)
		if key == "LRU":
			base = dict[key][-1].m_demand_misses
			continue
		#x = []
		y.append(dict[key][-1].m_demand_misses)

	for i in range(len(y)):
		y[i] = y[i]*1.0/base

	x = sorted(dict.keys())
	x.remove("LRU")

	ax.bar(x,y)
	ax.axhline(y=1, linestyle='--', color='k', label="LRU Baseline")
	ax.set_ybound(0.95,)
	plt.title(bench + ": Total cache miss ratio to LRU")
	plt.xlabel(xLabel)
	plt.ylabel("Total Misses")
	plt.legend()
	plt.show()

def bar_ipc_graph(dict, bench, xLabel):
	fig, ax = plt.subplots()
	y = []
	for key in sorted(dict.keys()):
		print(key)
		#x = []
	#		y.append(dict[key][-1].m_demand_misses)
		commitedInsts = 0
		simTicks = 0
		for dp in dict[key]:
			commitedInsts += dp.committedInsts
			simTicks += dp.simTicks

		y.append(1000*(1.0*commitedInsts/simTicks))


	x = sorted(dict.keys())

	ax.bar(x,y)
	plt.title(bench + ": IPC vs Replacement Policy")
	plt.xlabel(xLabel)
	plt.ylabel("IPC")
	plt.show()

def bar_mpki_graph(dict, bench, xLabel):
	fig, ax = plt.subplots()
	y = []
	for key in sorted(dict.keys()):
		print(key)
		simInst = (dict[key][-1].simInsts)
		misses = (dict[key][-1].m_demand_misses)
		y.append(1000*(misses*1.0/simInst))

	x = sorted(dict.keys())

	ax.bar(x,y)
	plt.title(bench + ": MPKI vs Replacement Policy")
	plt.xlabel(xLabel)
	plt.ylabel("MPKI")
	plt.show()

def bar_ipc_mpki_graph(dict, bench, xLabel):
	fig, ax1 = plt.subplots()
	width = 0.3
	y1 = []
	y2 = []
	for key in sorted(dict.keys()):
		print(key)
		simInst = (dict[key][-1].simInsts)
		misses = (dict[key][-1].m_demand_misses)
		y2.append(1000*(misses*1.0/simInst))

		commitedInsts = 0
		simTicks = 0
		for dp in dict[key]:
			commitedInsts += dp.committedInsts
			simTicks += dp.simTicks

		y1.append(1000*(1.0*commitedInsts/simTicks))

	x = sorted(dict.keys())

	x_index = np.arange(len(x))

	ax1.set_ylabel("IPC")
	ax1.bar(x_index,y1, width=width, label="IPC")

	ax2 = ax1.twinx()
	ax2.set_ylabel("MPKI")
	ax2.bar(x_index + width,y2, width=width, color='tab:orange', label="MPKI")

	lines,labels = ax1.get_legend_handles_labels()
	lines2,labels2 = ax2.get_legend_handles_labels()
	ax2.legend(lines + lines2, labels + labels2, loc=0)

	plt.xticks(x_index + width/2, x)

	plt.title(bench + ": IPC, MPKI vs Replacement Policy")
	plt.xlabel(xLabel)
	plt.show()

#IPC = 1000*(cpu.commitedInsts / simTicks)

lem_dict = {}
lem_dir = "./data/2kb/lem-in/"

extractData(lem_dict,lem_dir)
#inst_total_miss_graph(lem_dict, "lem-in", "Epoch (100 million instructions)")
#inst_epoch_missrate_graph(lem_dict, "lem-in", "Epoch (100 million instructions)")
#inst_epoch_ipc(lem_dict, "lem-in", "Epoch (100 million instructions)")
#inst_epoch_mpki_graph(lem_dict, "lem-in", "Epoch (100 million instructions)")
#bar_total_rel_miss_graph(lem_dict, "lem-in", "Replacement Policy")
#bar_ipc_graph(lem_dict, "lem-in", "Replacement Policy")
#bar_mpki_graph(lem_dict, "lem-in", "Replacement Policy")
#bar_ipc_mpki_graph(lem_dict, "lem-in", "Replacement Policy")

fait_dict = {}
fait_dir = "./data/2kb/fait/"

extractData(fait_dict,fait_dir)
#inst_total_miss_graph(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
#inst_epoch_missrate_graph(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
#inst_epoch_ipc(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
#inst_epoch_mpki_graph(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
#bar_total_rel_miss_graph(fait_dict, "fait-maison-spmv", "Replacement Policy")
#bar_ipc_graph(fait_dict, "fait-maison-spmv", "Replacement Policy")
#bar_mpki_graph(fait_dict, "fait-maison-spmv", "Replacement Policy")
#bar_ipc_mpki_graph(fait_dict, "fait-maison-spmv", "Replacement Policy")
	#		print(line)
#p1 = ax.scatter()
