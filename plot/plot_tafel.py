#!/usr/bin/env python
import pickle
import sys
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from catmap.model import ReactionModel
from matplotlib.pyplot import cm
from matplotlib import rc
from matplotlib.ticker import NullFormatter
from pylab import *
from matplotlib.font_manager import FontProperties

class Object(object):
    pass

mathtext_prop = {'fontset' : 'custom',
                 'it' : 'serif:italic',
                 'sf' : 'Helvetica:bold',
                 'cal' : 'serif:italic:bold'}
rc('font', family='serif', serif='Helvetica')
rc('mathtext', **mathtext_prop)
rc('xtick', labelsize=15)
rc('ytick', labelsize=15)

def get_data(pickle_file):
    a = pickle.load(open(pickle_file,'rb'))
    data = Object()
    #COVERAGES
    data.coverage_names = model.output_labels['coverage']
    coverage_map = np.array(a['coverage_map'], dtype="object")
    data.voltage = []
    scaler_array = coverage_map[:,0]
    for s in scaler_array:
        data.voltage.append(s[0])
    coverage_mpf = coverage_map[:,1]
    data.coverage = np.zeros((len(coverage_mpf),len(data.coverage_names)))
    for i in range(0,len(coverage_mpf)):
        for j in range(0,len(coverage_mpf[i])):
            float_rate = float(coverage_mpf[i][j])
            data.coverage[i][j]=float_rate
    #PRODUCTION RATES
    data.prod_names = model.output_labels['production_rate']
    production_rate_map = np.array(a['production_rate_map'], dtype="object")
    production_rate_mpf = production_rate_map[:,1]
    data.production_rate = np.zeros((len(production_rate_mpf),len(data.prod_names)))
    data.voltage = np.zeros((len(production_rate_mpf),1))
    for i in range(0,len(production_rate_mpf)):
        data.voltage[i][0] = production_rate_map[:,0][i][0]
        for j in range(0,len(data.prod_names)):
            float_rate = float(production_rate_mpf[i][j])
            data.production_rate[i][j]=float_rate
    #RATES
    data.rate_names = model.output_labels['rate']
    rate_map = np.array(a['rate_map'], dtype="object")
    rate_mpf = rate_map[:,1]
    data.rate = np.zeros((len(rate_mpf),len(data.rate_names)))
    for i in range(0,len(rate_mpf)):
        for j in range(0,len(rate_mpf[i])):
            float_rate = float(rate_mpf[i][j])
            data.rate[i][j]=float_rate
    return data

def convert_TOF(A): # Given a list, convert all the TOF to j(mA/cm2) using 0.161*TOF(According to Heine's ORR paper)
    C = [1*rate for rate in A]
    print(C)
    B = [0.161*rate for rate in A]
    print(B)
    return B

# plots
#color_list = ['#BF3F3F','#F47A33','#FFE228','#7FBF3F','#3FBFBF','#3F7FBF','#3F3FBF','#7F3FBF','#BF3F7F','#BF3F3F','#333333','#000000']
#pH = ['13']
#pH = ['0','1','2','2.5','3','4','7','10','12','14']
#voltages = [(-0.7,-2.0),(0.2,-0.7),(1.1,0.2),(2.0,1.1)]
pH = 4.6
voltages = [(1.5,3)]
#voltages = [(-1,-0.8),(-0.8, -0.6),(-0.6, -0.4),(-0.4, -0.2), (-0.2, 0), (0, 0.2)]
#voltages = [(-1,-0.6),(-0.6, -0.2),(-0.2, 0.2)]
# all pH

for a, alpha in enumerate([1]):
    	colors = plt.cm.Blues(np.linspace(0,1,5))[::-1]
    	#colors = raw_colors.reversed()
    	print(colors)
    # all voltages
    	for i, item in enumerate(voltages):
        	lower_, upper_ = item
        	log_file = 'kolbe_pH'+str(pH)+'_'+str(alpha)+'.log'
        	model = ReactionModel(setup_file = log_file)
        	pickle_file = 'kolbe_pH'+str(pH)+'_'+str(alpha)+'.pkl'
        	phX = get_data(pickle_file)
        	#colors = plt.cm.jet(np.linspace(0,1,5))
        	#color=colors[i]
        # sum over relevant products
        	products = ['O2_g','CO2_g']
        	for k, product in enumerate(products):
            		idx=phX.prod_names.index(product)
            		if k == 0:
                		data=np.column_stack((phX.voltage, phX.production_rate[:,idx]))
            		else:
                		data_var=np.column_stack((phX.voltage, 0.5*phX.production_rate[:,idx]))
                		data[:,1] += data_var[:,1]
            		print('pH = 4.6'+'  ITERATION = '+str(k)+'  PRODUCT = '+product)
            		print('TOTAL TOF =' + str(np.sum(data[:,1])))

        # merge data
        	pol_file = 'pol_kolbe_pH'+str(pH)+'_'+str(alpha)+'.tsv'
        	x=data[np.argsort(data[:, 0])][:,0]
        	y=convert_TOF(data[np.argsort(data[:, 0])][:,1])
        	if i == 0:
            		with open(pol_file,'w') as f:
                		np.savetxt(f, np.array([x,y]).T, delimiter='\t')
        	else:
            		with open(pol_file,'a+') as f:
                		np.savetxt(f, np.array([x,y]).T, delimiter='\t')
                #colors = plt.cm.jet(np.linspace(0,1,5))
                #color=colors[i]
    # plot
        	pol_file = 'pol_kolbe_pH'+str(pH)+'_'+str(alpha)+'.tsv'
        	data = np.loadtxt(pol_file,delimiter='\t')
        	data = data[data[:,0].argsort()]
        	x = data[:,0]
        	y = list(np.log10(data[:,1]))
    	#colors = plt.cm.jet(np.linspace(0,1,5))
        	#for c in range(5):
        	#colors = plt.cm.jet(np.linspace(0,1,5))
        	plt.plot(x,y, color=colors[a],  label='pH'+str(pH)+'_'+str(alpha))

#xx = [1.90148803121453, 1.93341171583499, 1.96931287970387, 2.00524000623103, 2.04522249998145, 2.08729758398919, 2.10519624060708, 2.21911000007417, 2.25090387140324, 2.28063111513326, 2.30842154455563, 2.36787603201566, 2.40351756930175, 2.44122573418688]
#yy = [-1.99453671490775, -1.74436053972657, -1.45845974675281, -1.18146414556891, -0.895459501962035, -0.627213316618326, -0.466452536551714, -0.338872033766291, -0.0441698996357811, 0.259385500968036, 0.527268209095831, 1.13437901030346, 1.50933172117588, 1.8754311655749]

E = [2.1,2.23,2.34,2.48]
i_kolbe = [0.0001, 0.13, 9.00, 110.11]
i_oer = [1.50, 2.07, 5.80, 28.39]

plt.scatter(E, np.log10(i_kolbe), color='black')
plt.plot(E, np.log10(i_kolbe), color='black')
plt.scatter(E, np.log10(i_oer), color='orange')
plt.plot(E, np.log10(i_oer), color='orange')

#for i in range(0,14): 
#plt.scatter(E,color='black')
#plt.plot(xx,yy,color='black')

fig = plt.figure(1, figsize=(5.5, 5.5))
ax = fig.add_subplot(1,1,1)
#leg = plt.legend(loc='lower right', ncol=1, prop={'size':12},frameon=False, fancybox=False, shadow=False)
#leg.get_frame().set_facecolor('none')
#leg.get_frame().set_linewidth(0.0)
plt.gcf().subplots_adjust(bottom=0.18, left=0.18)
plt.xlim((1.5,2.5))
plt.ylim((-2,3))
plt.xlabel(r'U (V vs. SHE)', fontsize=16)
plt.ylabel(r'log(i (mA/cm$^{2}$))', fontsize=16)
fig_name = 'tafel_plot.png'
fig.savefig(fig_name)
plt.close()
