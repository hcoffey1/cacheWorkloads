import matplotlib.pyplot as plt
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

def extractData(dict, dir):
	for file in os.listdir(dir):
		target_dir = dir + file
		target_file = target_dir + "/stats.txt"

		splitFile = file.split("_")
		dict[splitFile[1]] = []

		epoch=0
		with open(target_file) as dataFile:
			for line in dataFile:
				if "m_demand_misses" in line:
					tmpDataPoint = dataPoint()
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					tmpDataPoint.epoch = epoch
					tmpDataPoint.m_demand_misses = int(tmp[1])
					dict[splitFile[1]].append(tmpDataPoint)
					epoch += 1
				if "m_demand_accesses" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					dict[splitFile[1]][-1].m_demand_accesses = int(tmp[1])
				if "cpu.ipc" in line:
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					dict[splitFile[1]][-1].ipc = float(tmp[1])

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

lem_dict = {}
lem_dir = "./data/lem-in/"

extractData(lem_dict,lem_dir)
#inst_total_miss_graph(lem_dict, "lem-in", "Epoch (100 million instructions)")
#inst_epoch_missrate_graph(lem_dict, "lem-in", "Epoch (100 million instructions)")
#inst_epoch_ipc(lem_dict, "lem-in", "Epoch (100 million instructions)")

fait_dict = {}
fait_dir = "./data/fait/"

extractData(fait_dict,fait_dir)
inst_total_miss_graph(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
inst_epoch_missrate_graph(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
inst_epoch_ipc(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
	#		print(line)
#p1 = ax.scatter()
