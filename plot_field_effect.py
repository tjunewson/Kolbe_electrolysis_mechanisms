import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#excel path
xpath='/dft_results_kolbe.xlsx'

fig, ax = plt.subplots(figsize=(8,6))
ax1 = ax.twiny()

#location of data
df = pd.read_excel(xpath, 'field_effect')


def fit_func(x, a, b, c): #a = mu, b = alpha
    return a*x**2 + b*x + c

sp=['O','OH','OOH','H2O','CH3','CH3COO','CH3-CO2','CH3-CH3','O2']

x = df['E_Pt111'][0:11]
zz = np.linspace(-1, 1)


for s in sp:
    y = df[s][0:11]-df[s][5]
    params = curve_fit(fit_func, x, y)
    [a, b, c] = params[0]
    z = a*zz**2 + b*zz + c
    mu = b
    alpha = -2*a
    ax.scatter(x,y)
    ax.plot(zz,z,label = s,linestyle='-')
    print(s,round(mu,2),round(a,2))
    #print(s,round(mu,2),round(alpha,2))
    

ax1.set_xlim(-0.709,0.709)
#ax1.xaxis.label.set_color('b')
ax.set_xlabel('E (V/$\AA$)', fontsize=20)
ax1.set_xlabel('U$_{SHE}$ (V)', fontsize=20)
#ax1.spines['top'].set_color('b')

ax.tick_params(labelsize=15)
ax1.tick_params(labelsize=15, direction='out', pad=0)


ax.set_ylabel('G$_{ads}$ - G$_{ads}$(E = 0)(eV)', fontsize=20)
ax.set_xlim(-1,1)
ax1.set_xlim(-0.409,1.009)

plt.ylim(-0.4, 0.4)
plt.title('Field effect on adsorption energy on Pt(111)\n', fontsize=20)
ax.legend(frameon=False)
plt.show()

