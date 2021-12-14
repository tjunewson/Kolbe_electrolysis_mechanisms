#!/usr/bin/env python
import numpy as np
import re
import sys
import os

from catmap import ReactionModel
from string import Template

include_rate_control = False
fed_setting = False

##reaction parameters
pH = 4.6
voltages = [(1, 3)]

##set up for run
for Alpha in [10,1,0.1,0.01,0.001]: ##initial concentration of acetic acid
    alpha = Alpha
    print(alpha)  
    for i, item in enumerate(voltages):
        lower_, upper_ = item
        text = Template(open('kolbe_template.mkm').read())
        text = text.substitute(lower = lower_, upper = upper_, alpha_new = alpha)

        # setup model
        mkm_file = 'kolbe_pH'+str(pH)+'_'+str(alpha)+'.mkm'
        with open(mkm_file,'w') as f:
            f.write(text)
        model = ReactionModel(setup_file = mkm_file)
        model.output_variables+=['production_rate', 'free_energy', 'selectivity', 'interacting_energy']
        model.run()

        # rates
        from catmap import analyze
        vm = analyze.VectorMap(model)
        vm.plot_variable = 'rate'
        vm.descriptor_labels = ['U vs. SHE (V)']
        vm.log_scale = True
        vm.min = 1e-6
        vm.max = 1e4
        fig = vm.plot(save=False)
        fig.savefig('rate'+'_'+str(alpha)+'.png')

        # coverages
        vm = analyze.VectorMap(model)
        vm.log_scale = True
        vm.plot_variable = 'coverage'
        vm.descriptor_labels = ['coverage (ML)']
        vm.min = 1e-9
        vm.max = 1.1
        fig = vm.plot(save=False)
        fig.savefig('coverage'+'_'+str(alpha)+'.png')
        
        # production rate
        vm.plot_variable = 'production_rate'
        vm.descriptor_labels = ['U vs. SHE (V)']
        vm.log_scale = True
        vm.min = 1e-6
        vm.max = 1e6
        fig = vm.plot(save=False)
        fig.savefig('production_rate'+'_'+str(alpha)+'.png')
# post-processing


