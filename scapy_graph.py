import argparse
from helpers import saveFigure
from plotter import Plotter
from sources import Source1
from scapy.all import rdpcap

if __name__ == "__main__":
    #Parse command line arguments
	parser = argparse.ArgumentParser(description='Script for analizing network packets.')
	parser.add_argument("file", help="Pcap formatted capture")
	args = parser.parse_args()

	pcap = rdpcap(args.file)
	S1 = Source1(pcap)
	plotter = Plotter(S1)
    
	saveFigure(plotter.probabilityPlot(),args.file)
	saveFigure(plotter.informationPlot(),args.file)
	saveFigure(plotter.distributionPlot(),args.file)

	S1 = Source1(pcap)
	plotter = Plotter(S1)
	
	saveFigure(plotter.probabilityPlot(),args.file)
	saveFigure(plotter.informationPlot(),args.file)
	saveFigure(plotter.distributionPlot(),args.file)
