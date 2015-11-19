
# coding: utf-8

# In[85]:

import mpmath
import pylab as pl
import random


# In[45]:

tau = 2*mpmath.pi
# expression is factor*exp(exponent*factor_exponent)
def gaussian_pdf(variance, offset):
    factor = mpmath.sqrt(1/(variance*tau))
    factor_exponent=mpmath.mpf(-1.0)/(2*variance)
    exponent = mpmath.mpf(offset)*offset
    base = mpmath.exp(factor_exponent)
    return factor*mpmath.power(base, exponent)


# In[46]:

gaussian_pdf(1,0)


# In[80]:

def sum_gaussian(variance, offset, interval, nmax):
    return sum(gaussian_pdf(variance,offset+interval*n) for n in range(-nmax,nmax+1))

# expression is factor*exp(exponent_factor*factor_exponent) * 
# sum_n(exp(exponent_interval*n*n*factor_exponent) * 
#       exp(exponent_offset*n*factor_exponent)
# )
def sum_gaussian_theta(variance, offset, interval):
    factor = mpmath.sqrt(1.0/(variance*tau))
    factor_exponent=mpmath.mpf(-1.0)/(2*variance)
    exponent_factor = mpmath.mpf(offset)*offset
    factor_full = factor*mpmath.exp(exponent_factor*factor_exponent)
    exponent_interval = interval*interval
    exponent_offset = 2*interval*offset
    q = mpmath.exp(factor_exponent*exponent_interval)
    z = factor_exponent*exponent_offset/(2*mpmath.j)
    theta = mpmath.jtheta(3,z,q)
    return factor_full*theta


# In[81]:

sum_gaussian(1.0,0.7,tau,100)


# In[82]:

sum_gaussian_theta(1.0,0.7,tau)


# In[3]:

mpmath.jtheta(3,0,mpmath.exp(-1))


# In[5]:

mpmath.sqrt(mpmath.pi)


# In[63]:

def von_Mises_entropy_max():
    return mpmath.ln(2*mpmath.pi)
def von_Mises_entropy_fraction(kappa):
    I0_kappa = mpmath.besseli(0,kappa)
    I1_kappa = mpmath.besseli(1,kappa)
    kappa_entropy = mpmath.ln(2*mpmath.pi*I0_kappa) - kappa*(I1_kappa/I0_kappa)
    return 1-(kappa_entropy/von_Mises_entropy_max())
xs = pl.linspace(0,float(2*mpmath.pi),100)
def von_Mises_pdf_range(kappa):
    y = [von_Mises_pdf(x,kappa) for x in xs]
    return (max(y)-min(y))/mean(y)
def von_Mises_pdf(x,kappa,mu=mpmath.pi):
    return (mpmath.exp(kappa*mpmath.cos(x-mu))/
            (2*mpmath.pi*mpmath.besseli(0,kappa)))


# In[19]:

print von_Mises_entropy_ratio(0.05)
print von_Mises_pdf(3,0.05)


# In[41]:

float(2*mpmath.pi)
def mean(L):
    return sum(L)/len(L)


# In[55]:

def vm_stats(kappa):
    return (von_Mises_entropy_fraction(kappa),von_Mises_pdf_range(kappa))


# In[64]:

ks = pl.exp(pl.log(10)*pl.linspace(-1,-5,15))
ss = [vm_stats(k) for k in ks]
pl.plot(ks,[von_Mises_pdf_range(k) for k in ks])
pl.show()


# In[31]:

tau = 2*mpmath.pi
kappa0 = 0.1


# In[32]:

def relative_wrap_probability(angle,t,n):
    difference = angle + tau*n
    return mpmath.sqrt(1/(t*tau))*mpmath.exp(-pow(difference,2)/(2*t))


# In[33]:

print relative_wrap_probability(0,1/kappa0,2)


# In[54]:

#def sum_relative_wrap_probabilities(angle,t,nmax):
#    return sum(relative_wrap_probability(angle,t,i) for i in range(-nmax,nmax+1))
def sum_relative_wrap_probabilities(angle,t,nmax):
    return sum_gaussian(t,angle,tau,nmax)


# In[55]:

#def wrap_probability_total(angle,t):
#    z = tau*angle*mpmath.j/(2*t)
#    q = mpmath.exp(-tau*tau/t)
#    factor = mpmath.sqrt(1/(tau*t))*mpmath.exp(-angle*angle/(2*t))
#    theta = mpmath.jtheta(3,z,q)
#    print z,q,factor,theta
#    return factor*theta
def wrap_probability_total(angle,t):
    return sum_gaussian_theta(t,angle,tau)


# In[83]:

sum_relative_wrap_probabilities_a(0,1/kappa0,100)


# In[84]:

wrap_probability_total_a(0,1/kappa0)


# In[129]:

class WrapNumberSource:
    def __init__(self, kappa, seed=0):
        self._kappa = mpmath.mpf(kappa)
        self._period = 1.0/self._kappa
        self._tau = 2*mpmath.pi
        self._seed = seed
        self._rng = random.Random(self._seed)
        self._angle_cache = {}
        self._wrap_cache = {}
    def tau(self):
        return self._tau
    def kappa(self):
        return self._kappa
    def period(self):
        return self._period
    def seed(self):
        return self._seed
    def node_number(self, t):
        return int(mpmath.floor(t/self._period))
    def node_angle(self, n):
        try:
            return self._angle_cache[n]
        except KeyError:
            self._rng.seed(self._seed+n)
            angle = self._rng.random()*self._tau
            self._angle_cache[n] = angle
            return angle
    def gaussian_pdf(self, offset):
        factor = mpmath.sqrt(1.0/(self._period*self._tau))
        factor_exponent=-1.0/(2*self._period)
        exponent = mpmath.mpf(offset)*offset
        return factor*mpmath.exp(factor_exponent*exponent)
    def gaussian_total(self,offset):
        factor = mpmath.sqrt(1.0/(self._period*self._tau))
        factor_exponent = -1.0/(2*self._period)
        exponent_factor = mpmath.mpf(offset)*offset
        exponent_interval = self._tau*self._tau
        exponent_offset = 2*self._tau*offset
        factor_full = factor*mpmath.exp(exponent_factor*factor_exponent)
        q = mpmath.exp(factor_exponent*exponent_interval)
        z = factor_exponent*exponent_offset/(2*mpmath.j)
        theta = mpmath.jtheta(3,z,q).real
        return factor_full*theta
    def wrap_sequence(self):
        yield 0
        n = 1
        while True:
            yield n
            yield -n
            n += 1
    def wrap_number(self, n):
        try:
            return self._wrap_cache[n]
        except KeyError:
            angle_minus = self.node_angle(n)
            angle_plus = self.node_angle(n+1)
            offset = angle_plus-angle_minus
            relative_probability_total = self.gaussian_total(offset)
            self._rng.seed(self._seed+n)
            self._rng.random()
            r = self._rng.random()*relative_probability_total
            relative_probability_sum = mpmath.mpf(0.0)
            for wrap in self.wrap_sequence():
                relative_probability_sum += self.gaussian_pdf(offset + wrap*self._tau)
                if relative_probability_sum >= r:
                    break
            self._wrap_cache[n] = wrap
            return wrap
    def value(self,t,scurve):
        n = self.node_number(t)
        angle_minus = self.node_angle(n)
        angle_plus = self.node_angle(n+1)
        wrap = self.wrap_number(n)
        offset = angle_plus-angle_minus+self._tau*wrap
        ratio = (t-n*self._period)/self._period
        value = scurve(ratio)*offset + angle_minus
        return mpmath.fmod(value,self._tau)
    def amplitude(self):
        
        


# In[155]:

wns = WrapNumberSource(0.005)
scurve_1=lambda x:x
scurve_inf=lambda x:0.5*(1-mpmath.cos(x*mpmath.pi))


# In[133]:

#[wns.wrap_number(i) for i in range(100)]


# In[173]:

n = 3000
tmin = 0
tmax = 2000
dt = tmax/n
ts = pl.linspace(tmin,tmax,n)
vs = [float(wns.value(t,scurve_inf)) for t in ts]
hs = [v1-v2 for v1,v2 in zip(vs[:-1],vs[1:]) if abs(v1-v2)< 4]
rs = pl.linspace(0,1,n)
#xs = pl.cos(vs)*rs
#ys = pl.sin(vs)*rs
pl.plot(ts[:len(hs)],hs)
#pl.plot(xs,ys)
pl.show()


# In[169]:

len(hs)

