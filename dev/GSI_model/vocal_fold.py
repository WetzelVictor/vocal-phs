#-*-encoding:utf-8-*-

from pyphs import Core
import os
from pyphs import signalgenerator

#%%
# Main system
label = 'vocal fold'
core = Core(label)

#%% Adding storage components
# Masse m
pii = core.symbols('pi_i')
m = core.symbols('m')
Hm = pii**2/(2.*m)
core.add_storages(pii,Hm)

# Spring
xk, k = core.symbols([ 'xi_i','k' ])
Hk = k*xk**2/2.
core.add_storages(xk, Hk)

# Pure spring
xKappa, kappa = core.symbols(['sigma_i','kappa'])
Hkappa = kappa*xKappa**2/2.
core.add_storages(xKappa, Hkappa)

#%% Adding dissipative component
wa, a = core.symbols(['w_a','a'])
za = a * wa
core.add_dissipations(wa, za)

#%% Adding ports
f_I,v_O = core.symbols(['f_I','v_O'])
core.add_ports(f_I, v_O)


#%% Add connections
core.set_Jxx([[0, -1 ,1,],
              [+1, 0 ,0,],
              [-1, 0, 0,]])
core.set_Jxw([ [-1],
               [0],
               [0]])
core.set_Jxy([ [0],
               [0],
               [1]])

core.pprint()

#%% Initializing our system
m_g = 0.2
f0 = 440 #fundamental frequency (Hz)
k_Npm = m_g*(2*3.14157*f0)
kappa_Npm = 5
a_Nspm = 1.

vals = {m:m_g,
        k:k_Npm,
        a: a_Nspm,
        kappa:kappa_Npm}
core.subs.update(vals)

#%% Simulation
config = {'fs':44100,
          'path':os.path.join(os.getcwd(), label)
         }
T = 1.
nt = int(T*config['fs'])


config_isig = {'which': 'noise',         # signal type is noise (amplitude 1)
               'tsig': T,                # signal duration (s)
               'fs': config['fs']}       # signal sample rate (Hz)
isig = signalgenerator(**config_isig)    # build Python generator


# Setting up simulation
simu = core.to_simulation(config=config)
simu.method.u

# generator passed as an argument to `Simulation.init`
def f():
    """
    Generator (0, f_I) for f_I in isig
    """
    for f_I in isig():
        yield [f_I]

        
simu.init(u=f(), nt=nt)     # initialize `Data` object

simu.process()

simu.data.plot_powerbal()
