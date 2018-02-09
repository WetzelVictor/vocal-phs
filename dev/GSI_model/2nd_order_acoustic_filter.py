#-*-encoding:utf-8-*-

import os
from pyphs import Core
from pyphs import signalgenerator
import sympy

#%%
# Main system
label = '2nd order acoustical resonator'
core = Core(label)

#%% Storage components
p1,int_p1, a1, w1, q1, t = core.symbols(['p1','int_p1','a1','w1', 'q1','t'])
x1 = p1/a1
Hx1 = p1**2/a1
core.add_storages(x1, Hx1)

x2 = int_p1 ### Je sais pas comment lui demander de prendre l'intégrale de p
Hx2 = x2**2 *w1**2/a1
core.add_storages(x2, Hx2)

#%% Dissipative components
w = p1
zw = q1*w1/a1*w
core.add_dissipations(w, zw)

#%% Ports
Pac, Qac = core.symbols(['Pac','Qac'])
core.add_ports(Qac, -Pac)

#%% Connections
core.set_Jxx([ [0,-1],
               [1, 0]])

core.set_Jxw([[-1],
              [0]])

core.set_Jxy([[1],
              [0]])

core.set_Jwy([[0]])
core.set_Jww([[0]])
core.set_Jyy([[0]])

core.pprint()

