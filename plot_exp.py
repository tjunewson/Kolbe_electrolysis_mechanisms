import matplotlib.pyplot as  plt
import numpy as np
import pandas as pd

#excel path
xpath = 'dft_results_kolbe.xlsx'

ax.plot(df1['Pt_1M_U_SHE'], df1['Pt_1M_log(i)'],label = '$C_a$=1M', marker = 'o', markersize = 10, color = 'royalblue')
ax.plot(df1['Pt_0.5M_U_SHE'], df1['Pt_0.5M_log(i)'],label = '$C_a$=0.5M', marker = 'o', markersize = 10,color = 'cornflowerblue')
ax.plot(df1['Pt_0.1M_U_SHE'], df1['Pt_0.1M_log(i)'],label = '$C_a$=0.1M', marker = 'o', markersize = 10,color = 'deepskyblue')

print(list(df1['Pt_1M_U_SHE']), list(df1['Pt_1M_log(i)']))
plt.xlabel('U (V vs. SHE)', fontsize=16)
plt.ylabel('log(j (mA/cm$^2$))', fontsize=16)
plt.legend(fontsize=12,frameon=False)
#plt.title('Kolbe electrolysis on Pt anode', fontsize=16)
plt.xlim(1.5,2.5)
plt.ylim(-2.1,3)
ax.tick_params(labelsize=16)
ax.patch.set_color('palegoldenrod') # or whatever color you like
ax.patch.set_alpha(.0)
fig.savefig('kolbe_exp_tafel.png',dpi=250)
plt.show()

#location of data
df = pd.read_excel(xpath, 'product')
fig, ax = plt.subplots(figsize =(5.5, 5.5))
#ax1= ax.twinx()
#plot
u = [2.10,2.23,2.34,2.48]
print(df['O2'][5:9])
ax.scatter(u, df['O2'][4:9], s=80, color = 'tab:blue')
ax.plot(u, df['O2'][4:9], label='OER',lw = 3,  color = 'tab:blue')
ax.scatter(u, df['CO2'][4:9], s=80, color = 'tab:orange')
ax.plot(u, df['CO2'][4:9], label='Kolbe',lw = 3,  color = 'tab:orange')

# Adding Xticks  
ax.set_ylabel('Selectivity (%)',fontsize=16)
ax.set_xlabel('U (V vs. SHE)',fontsize=16) 

ax.tick_params(labelsize=15)
ax.set_xticks(u)
ax.set_xticklabels(['2.10','2.23','2.34','2.48'])
ax.set_ylim(0,100)
ax.set_xlim(2.08,2.50)

ax.legend(fontsize=12,frameon=False,ncol=1,loc='upper center')
fig.savefig('kolbe_exp_select_small.png',dpi=250,bbox_inches='tight')
plt.show()
