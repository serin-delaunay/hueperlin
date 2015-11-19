
# coding: utf-8

# In[9]:

import angle_noise
reload(angle_noise)
import pylab as pl


# In[10]:

an = angle_noise.AngleNoise()


# In[28]:




# In[75]:

get_ipython().magic(u'matplotlib inline')
pl.rcParams['figure.figsize'] = 16,16
an.stationary_amplitude=3*pl.pi
an.stationary_frequency=0.01
an.wrap_frequency=0.01
an.value(0.0)
n = 3000
tmin = pl.randint(-100000,100000)
trange=30
tmax = tmin+trange
ts = pl.linspace(tmin,tmax,n)
vs = [float(an.value(t)) for t in ts]
rs = pl.linspace(0,1,n)
xs = pl.cos(vs)*rs
ys = pl.sin(vs)*rs
pl.plot(xs,ys)
pl.show()


# In[70]:

len(an._wns._angle_cache)

