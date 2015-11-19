
# coding: utf-8

# In[8]:

import noise
import pylab as pl
import math


# In[10]:

def gaussian_pdf(x,mean,variance):
    xx = x-mean
    return pl.sqrt(1.0/(2*pl.pi*variance))*pl.exp(-xx*xx/(2*variance))


# In[155]:

octaves = 24
lacunarity=2.0-0.5*(math.pi-3)
persistence=1.0/lacunarity
#base=72+math.sqrt(2)
base = 0
repeat=2**20
def p(x):
    return noise.pnoise1(x+base,
                         octaves=octaves,
                         lacunarity=lacunarity,
                         base=0,
                         repeat=repeat,
                         persistence=persistence
                        )


# In[86]:

xs = pl.linspace(0,10,1000)
ys = [p(x) for x in xs]
pl.plot(xs,ys)
pl.show()


# In[33]:

N = 1000000
bins=31


# In[49]:

ts = repeat*pl.rand(N)
#ts = pl.linspace(0,100,N)


# In[50]:

ps = [p(t) for t in ts]


# In[51]:

mean = pl.mean(ps)


# In[52]:

std = pl.std(ps)


# In[53]:

gauss_max = gaussian_pdf(0,mean,std*std)


# In[54]:

pl.hist(ps,bins=31)
xs = pl.linspace(-1,1,100)
ys = N*gaussian_pdf(xs,mean,std*std)/(bins/2.0)
pl.plot(xs,ys)
pl.show()


# In[87]:

print mean,std,std*std


# In[67]:

def perlin_stats(octaves,lacunarity,persistence,N=1000000):
    ts = repeat*pl.rand(N)
    ps = [p(t) for t in ts]
    return pl.mean(ps), pl.std(ps)


# In[70]:

xs = pl.linspace(1.5,3.5,21)
ys = pl.linspace(0.1,0.9,9)
ms = pl.ndarray((21,9))
stds = pl.ndarray((21,9))


# In[72]:

for i in range(21):
    for j in range(9):
        x,y = xs[i],ys[j]
        ms[i,j],stds[i,j] = perlin_stats(8,x,y,100000)
        print x,y


# In[88]:

pl.contourf(ys,xs,stds)
pl.colorbar()
pl.show()


# In[81]:

sigma = pl.mean(stds)


# In[89]:

sigma


# In[167]:

def perlin_covariance_corr(delta,N=1000000,bound=1):
    ts = bound*pl.rand(N)
    tds = ts+delta
    ps = [p(t) for t in ts]
    pds = [p(td) for td in tds]
    #cov = pl.mean([pp*pd for pp,pd in zip(ps,pds)])
    cov = pl.mean([(pp-pd)**2 for pp,pd in zip(ps,pds)])
    corr = pl.mean([pp*pd for pp,pd in zip(ps,pds)])
    return cov, corr


# In[157]:

deltas = pl.logspace(-8,1,46)


# In[168]:

cv_stats = [perlin_covariance_corr(d) for d in deltas]


# In[169]:

zip(deltas,cv_stats)


# In[170]:

[(d,cov/d) for (d,(cov,corr)) in zip(deltas,cv_stats)]


# In[165]:

deltas


# In[166]:

[(d,corr) for (d,(cov,corr)) in zip(deltas,cv_stats)]

