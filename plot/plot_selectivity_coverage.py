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
import matplotlib.ticker as mtick
from matplotlib import ticker
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
color_list = ['#BF3F3F','#F47A33','#FFE228','#7FBF3F','#3FBFBF','#3F7FBF','#3F3FBF','#7F3FBF','#BF3F7F','#BF3F3F','#333333','#000000']
#pH = ['13']
#pH = ['0','1','2','2.5','3','4','7','10','12','14']
#voltages = [(-0.7,-2.0),(0.2,-0.7),(1.1,0.2),(2.0,1.1)]
pH = 4.6
voltages = [(1.5,2.8)]
#voltages = [(-1,-0.8),(-0.8, -0.6),(-0.6, -0.4),(-0.4, -0.2), (-0.2, 0), (0, 0.2)]
#voltages = [(-1,-0.6),(-0.6, -0.2),(-0.2, 0.2)]
# all pH
fig, ax = plt.subplots(figsize=(5.5, 5.5))
ax1=ax.twinx()

for i, item in enumerate(voltages):
    lower_, upper_ = item
    log_file = 'kolbe_pH'+str(pH)+'_'+str(i)+'.log'
    model = ReactionModel(setup_file = log_file)
    pickle_file = 'kolbe_pH'+str(pH)+'_'+str(i)+'.pkl'
    phX = get_data(pickle_file)

    # plot partial current densities for different  products
    products = ['O2_g','CO2_g','C2H6_g']
    #fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for product in products:
        idx=phX.prod_names.index(product)
        #print(idx)
        data=np.column_stack((phX.voltage, phX.production_rate[:,idx]))
	#pol_file = 'pol_fur_pH'+str(pH)+'_'+product+'.tsv'
        x=data[np.argsort(data[:, 0])][:,0]
        y=data[np.argsort(data[:, 0])][:,1]
        #print(Y,len(Y))
        if product == 'O2_g':
            j1 = 4*y
            print(j1)
        if product == 'CO2_g':
            j2 = y
            print(j2)
        else:
            print('not included')
    j = j1+j2
    s_oer = [float(a)/float(b) for a,b in zip(j1,j)]
    s_kolbe = [float(c)/float(d) for c,d in zip(j2,j)]
    ax.plot(x,s_oer,linewidth=3, label='OER')
    ax.plot(x,s_kolbe,linewidth=3, label='Kolbe')
   # for product in products:
   #     print(product)
   #     idx=phX.prod_names.index(product)
   #     data=np.column_stack((phX.voltage, phX.production_rate[:,idx]))
   #     x=data[np.argsort(data[:, 0])][:,0]
   #     y=convert_TOF(data[np.argsort(data[:, 0])][:,1])
   #     yy = [float(a)/float(b) for a,b in zip(y,Y)]
            #yy = [int(a)/int(b) for a, b in zip(y,Y)]
            #yy = [] #selectivity
            #for i in range(len(Y)):
            #    for a,b in zip(y,Y):
            #        if float(b) != 0:
            #            yy[i] += float(a)/float(b)
            #        else:
            #            yy[i] += 0
   #     ax.plot(x,yy, linewidth=1.2, label=product)	

#coverage
text = np.loadtxt('coverage_table.txt', skiprows=1)
text = text[text[:,0].argsort()]
newtext = np.array(text).transpose()

voltage, temperature, CH3COO_s,CH3_s,H2O_s,OH_s,OOH_s,O_s = newtext
v = voltage
labels=['*CH$_3$COO','CH$_3$','*H$_2$O','*OH','OOH','O']
#ax.plot(x, newtext[2:][0],linewidth=3, label=labels[0])
ax1.plot(v, newtext[2:][2],linewidth=1.5,ls='--',label=labels[2])
ax1.plot(v, newtext[2:][3],linewidth=1.5,ls='--',label=labels[3])
ax1.plot(v, newtext[2:][4],linewidth=1.5,ls='--',label=labels[4])
ax1.plot(v, newtext[2:][5],linewidth=1.5,ls='--',label=labels[5])
ax1.plot(v, newtext[2:][0],linewidth=1.5,ls='--',label=labels[0])
ax1.plot(v, newtext[2:][1],linewidth=1.5,ls='--',label=labels[1])

#fig settings
ax1.set_yscale('log', nonpositive ='clip')
ax1.set_ylim(bottom = 0.00000001)
#ax1.set_xlim(1.5,2.5)
#ax.set_title('Coverage', fontsize=20)
#ax.set_xlabel('Voltage vs SHE (V)',fontsize=20)
ax1.set_ylabel('Coverge',fontsize=16)

ax.legend(loc='upper left', ncol=1, prop={'size':10},frameon=False)
ax1.legend(loc='upper right', ncol=1, prop={'size':10}, frameon=False)
#leg.get_frame().set_facecolor('none')
#leg.get_frame().set_linewidth(0.0)
plt.gcf().subplots_adjust(bottom=0.18, left=0.18)
ax.set_xlim((1.5,2.5))
ax.set_ylim((0,1))
ax.set_xlabel(r'U (V vs. SHE)', fontsize=16)
ax.set_ylabel(r'Selectivity', fontsize=16)
ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=1,decimals=0))
fig_name = 'select_coverage.png'
fig.savefig(fig_name,bbox_inches='tight',dpi=250)
plt.close()
