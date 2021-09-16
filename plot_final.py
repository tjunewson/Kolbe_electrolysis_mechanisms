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
color_list = ['#BF3F3F','#F47A33','#FFE228','#7FBF3F','#3FBFBF','#3F7FBF','#3F3FBF','#7F3FBF','#BF3F7F','#BF3F3F','#333333','#000000']
#pH = ['13']
#pH = ['0','1','2','2.5','3','4','7','10','12','14']
#voltages = [(-0.7,-2.0),(0.2,-0.7),(1.1,0.2),(2.0,1.1)]
pH = 4.6
voltages = [(1.9,2.8)]
#voltages = [(-1,-0.8),(-0.8, -0.6),(-0.6, -0.4),(-0.4, -0.2), (-0.2, 0), (0, 0.2)]
#voltages = [(-1,-0.6),(-0.6, -0.2),(-0.2, 0.2)]
# all pH
alpha = 1
for i, item in enumerate(voltages):
    lower_, upper_ = item
    log_file = 'kolbe_pH'+str(pH)+'_'+str(alpha)+'.log'
    model = ReactionModel(setup_file = log_file)
    pickle_file = 'kolbe_pH'+str(pH)+'_'+str(alpha)+'.pkl'
    phX = get_data(pickle_file)

    # plot partial current densities for different  products
    products = ['O2_g','C2H6_g']
    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    for product in products:
        idx=phX.prod_names.index(product)
        print(idx)
        if product == 'O2_g':
            data=np.column_stack((phX.voltage, phX.production_rate[:,idx]))
	    #pol_file = 'pol_fur_pH'+str(pH)+'_'+product+'.tsv'
            x=data[np.argsort(data[:, 0])][:,0]
            y=convert_TOF(data[np.argsort(data[:, 0])][:,1])
            ax.plot(x,np.log10(y), linewidth=1.8,color='orange',ls='-', label='OER, this work')				
        if product == 'C2H6_g':
            data=np.column_stack((phX.voltage, 0.5*phX.production_rate[:,idx]))
            #pol_file = 'pol_fur_pH'+str(pH)+'_'+product+'.tsv'
            x=data[np.argsort(data[:, 0])][:,0]
            y=convert_TOF(data[np.argsort(data[:, 0])][:,1])
            ax.plot(x,np.log10(y), linewidth=1.8,color='black',ls='-', label='Kolbe, this work')

E = [2.1,2.23,2.34,2.48]
i_kolbe = [0.0005, 0.13, 9.00, 110.11]
i_oer = [1.49, 2.07, 5.80, 28.39]

rhe = 4.9*0.059

E11 = [2.19,2.29,2.34,2.40,2.45,2.49,2.58]
E1 = [e-rhe for e in E11]
E12 = [2.30,2.50,2.56]
E2 = [e-rhe for e in E12]

i_kolbe_1 = [0.004,0.156,0.728,2.245,4.134,4.852,9.485]
i_oer_1 = [1.552,3.281,4.339]

xx = np.linspace(0,3,100)

ax.scatter(E, np.log10(i_oer), color='orange')
ax.plot(E, np.log10(i_oer),ls ='--', lw=1, color='orange',label='OER, Exp. by Dickinson and Wynne-Jones')

for i,e in enumerate(E):
    if i < 3:
        ax.scatter(e, np.log10(i_kolbe[i]),edgecolor='black',facecolor='black')
    else:
        ax.scatter(e, np.log10(i_kolbe[i]),edgecolor='black',facecolor='white')

#plot tafel
a,b = np.polyfit(E[:3],[np.log10(i) for i in i_kolbe[:3]],1)
ax.plot(xx, a*xx+b, color='black', ls ='--', lw=1,label='Kolbe, Exp. by Dickinson and Wynne-Jones')
print(1/a*1000)

ax.scatter(E2, np.log10(i_oer_1), marker='s', color='orange')
ax.plot(E2, np.log10(i_oer_1), ls ='--', lw=1,color='orange',label='OER, Exp. by Cervino et al.')

for i,e in enumerate(E1):
    if i < 3:
        ax.scatter(e, np.log10(i_kolbe_1[i]),marker='s',edgecolor='black',facecolor='black')
    else:
        ax.scatter(e, np.log10(i_kolbe_1[i]),marker='s',edgecolor='black',facecolor='white')

a,b = np.polyfit(E1[:3],[np.log10(i) for i in i_kolbe_1[:3]],1)
ax.plot(xx, a*xx+b, color='black', ls ='--', lw=1,label='Kolbe, Exp. by Cervino et al.')
print(1/a*1000)



#ax, fig = plt.figure(1, figsize=(10, 8))
leg = plt.legend(loc='upper left', ncol=1, prop={'size':8}, fancybox=True, shadow=False)
leg.get_frame().set_facecolor('none')
leg.get_frame().set_linewidth(0.0)
plt.gcf().subplots_adjust(bottom=0.18, left=0.18)
plt.xlim((1.5,2.5))
plt.ylim((-2,3))
plt.xlabel(r'U (V vs. SHE)', fontsize=16)
plt.ylabel(r'log(j (mA/cm$^{2}$))', fontsize=16)
#plt.title('Simulated tafel plots on PtO2, 1M acetate, pH = 4.6', fontsize=20)
fig_name = 'partial_tafel_small.png'
fig.savefig(fig_name,dpi=300,bbox_inches='tight')
plt.close()
