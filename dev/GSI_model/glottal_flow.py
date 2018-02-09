#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 17:41:22 2018

@author: victorw
"""

from pyphs import Core
import os
from pyphs import signalgenerator
from sympy import Heaviside

#%%
# Main system
label = 'glottal_flow'
core = Core(label)

#%% Adding storage components
# Fluid speed
v0, h, rho, l, L = core.symbols(['v_O',
                                 'h',
                                 'rho',
                                 'l',
                                 'L'])
mh = 2*rho*l*L*h
m3 = mh*(1 + 4*l**2/h**2)/12
Hv0 = mh *v0**2/2
core.add_storages(v0, Hv0)

#
dym = core.symbols('dy_m')
Hdym= mh/2 * dym**2
core.add_storages(dym, Hdym)

#
dh = core.symbols('dh')
Hdh = m3/2*dh**2
core.add_storages(dh, Hdh)

#
Hh = mh *v0**2/2 + mh/2 * dym**2 + m3/2*dh**2
core.add_storages(h, Hh)

#%% Dissipative components
w_g, Qp = core.symbols([ 'w_g','Q_p' ])
w_g = Qp
z_g = rho / 2 *(w_g/(L*h))**2 * Heaviside(w_g)
core.add_dissipations(w_g, z_g)

#%% Ports

