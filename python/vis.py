import matplotlib.pyplot as plt
import os

class dataPoint:
	epoch = None
	m_demand_misses = None

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
					tmp = line.split(" ")
					tmp = list(filter(len, tmp))
					tmpDataPoint = dataPoint()
					tmpDataPoint.epoch = epoch
					tmpDataPoint.m_demand_misses = int(tmp[1])
					dict[splitFile[1]].append(tmpDataPoint)
					epoch += 1

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

lem_dict = {}
lem_dir = "./data/lem-in/"

extractData(lem_dict,lem_dir)
inst_total_miss_graph(lem_dict, "lem-in", "Epoch (100 million instructions)")

fait_dict = {}
fait_dir = "./data/fait/"

extractData(fait_dict,fait_dir)
inst_total_miss_graph(fait_dict, "fait-maison-spmv", "Epoch (1 million instructions)")
	#		print(line)
#p1 = ax.scatter()
