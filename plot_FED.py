#------------------------------------------
#   Importing the required packages
#------------------------------------------
get_ipython().run_line_magic('matplotlib', 'auto')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import UnivariateSpline

#------------------------------------------
#   Making the figure object
#------------------------------------------
fig, ax = plt.subplots(figsize=(9,7))
ax1=ax.twiny()

##define the function for plotting FEDs
def plot_energies(reaction_energies, activation_energies,  ax, color, ls, label):
    """plots free energy diagrams given reaction energies and activation
        energies,
    which should be same-length lists and a matploblit axes object 
    """
    half_width = 0.3
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    rxn_pathway = np.arange(len(reaction_energies)) # for stoichiometry
    #IS_energy = 0.
    IS_energy = 0.
    for i, rxn_number in enumerate(rxn_pathway):
        if i == 0:
            ax.plot([-half_width, half_width], [IS_energy, IS_energy], ls, color=color,label = label)
        FS_energy = IS_energy + reaction_energies[rxn_number] 
        TS_energy = IS_energy + activation_energies[rxn_number] 
        ax.plot([i + 1 - half_width, i + 1 + half_width], [FS_energy, FS_energy], ls, color=color)
        if abs(TS_energy - IS_energy) < 0.001 or abs(TS_energy - FS_energy) < 0.001:
            ax.plot([i + half_width, i + 1 - half_width], [IS_energy, FS_energy], ls, color=color)
        else:
            A = UnivariateSpline([i + half_width, i + 0.5, i + 1 - half_width], 
                                 [IS_energy, TS_energy, FS_energy],k=2) 
            x = np.linspace(i + half_width, i + 1 - half_width)
            ax.plot(x, A(x), ls, color=color) 
        IS_energy = FS_energy
    return ax

G_oer = [0,0.02,0.93,1.23,3.65,4.92]
G_kol = [1.62,1.6,3.9,0.21,1.71,0.69]
g_oer = np.array(G_oer)
g_kol = np.array(G_kol)

#print(g_oer)

dE1,dE2,dE3,dE4,dE5 = g_oer[1:]-g_oer[:-1]
#print(dE1,dE2,dE3,dE4,dE5)

color1 = 'r'
color2 = 'black'
ls1 = '-'
ls2 = '--'

#field parameters:mu and alpha
#oer
f_h2o=[-0.08,-0.07]
f_oh=[-0.08,-0.09]
f_o=[-0.13,-0.07]
f_ooh=[-0.14,-0.16]
#kolbe
f_ch3coo=[0.02,-0.26]
f_ch3=[0.3,-0.06]
f_ch3_co2=[0.1,-0.28]
f_ch3_ch3=[0.4,-0.19]


CH = 1.41
pzc = 0.3
u = 0
uu = 0.9


def field(para,u):
    PZC = pzc
    U = u
    fe = para[0]*(U-PZC)*CH+para[1]*np.square((U-PZC)*CH)
    return fe

print(field(f_ch3_ch3,u),field(f_ch3_ch3,uu))

pH = 4.6
ph = 0.059*pH


colors=['r','black','royalblue']
for i,u in enumerate([0,1,2]):
    Ea1 = [0, 0, 0.15+field(f_ch3_co2,u)-field(f_ch3coo,u),0.15+field(f_ch3_co2,u)-field(f_ch3coo,u), 0.93+field(f_ch3_ch3,u)-2*field(f_ch3,u)]
    print(Ea1)
    Er1 = [2.03-u+field(f_ch3coo,u)-ph, 2.03-u+field(f_ch3coo,u)-ph, -2.09+field(f_ch3,u)-field(f_ch3coo,u), -2.09+field(f_ch3,u)-field(f_ch3coo,u), -0.23-2*field(f_ch3,u)]
    Ea2 = [ 0, 0, 0, 0, 0]
    Er2 = [ 0.17+field(f_h2o,u), 2.36+field(f_oh,u)-field(f_h2o,u)-u-ph, 0.56+field(f_o,u)-field(f_oh,u)-u-ph, 1.94+field(f_ooh,u)-field(f_o,u)-u-ph, -0.11-u-field(f_ooh,u)-u-ph]
    ax = plot_energies(Er1, Ea1, ax,  color=colors[i], ls='-', label='Kolbe@'+str(u)+'V vs SHE')
    ax1 = plot_energies(Er2, Ea2, ax1,  color=colors[i], ls='--', label='OER@'+str(u)+'V vs SHE')
    print(Er1[0])

ax.set_ylim(-7,7)
ax.set_xlim(-0.2,5.2)
ax.set_xticks([0, 1, 2, 3, 4, 5]) 
ax.set_xticklabels(['2$CH_3COOH$(l)','*$CH_3COO$+$CH_3COOH$(l)','2$CH_3COO*$','$CH_3*$+$CH_3COO*$+$CO_2$(g)','2$CH_3*$+2$CO_2$(g)','$C_2H_6$(g)+2$CO_2$(g)'], rotation=12.)
ax.tick_params(labelsize=12)

#ax1.xaxis.tick_top()
ax1.set_xlim(-0.2,5.2)
ax1.spines['top'].set_color('r')
ax1.set_xticks([0, 1, 2, 3, 4, 5])
ax1.set_xticklabels(['$H_2O$ (l)','*$H_2O$','*OH','*O','*OOH','$O_2$ (g)'], rotation=0.)
ax1.tick_params(labelsize=12, axis = 'x', direction='out', colors='r',pad=10)

ax.legend(loc=2, frameon=False)
ax1.legend(loc=1, frameon=False)

ax.set_ylabel('Free energy (eV)', fontsize=20)

###PtO2_with_field_SHE
