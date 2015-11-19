
# coding: utf-8

# In[1]:

import mpmath
import random


# In[4]:

scurve_1=lambda x:x
scurve_inf=lambda x:0.5*(1-mpmath.cos(x*mpmath.pi))
class WrapNoise:
    def __init__(self, kappa=0.001, frequency=1.0,
                 scurve=scurve_inf, seed=0):
        self._kappa = mpmath.mpf(kappa)
        self._period = 1.0/self._kappa
        self.frequency = frequency
        self._tau = 2*mpmath.pi
        self._seed = seed
        self._rng = random.Random(self._seed)
        self.scurve = scurve
        self.initialise_cache()
    def scale_t(self,t):
        return t*self.frequency
    def tau(self):
        return self._tau
    def initialise_cache(self):
        self._angle_cache = {}
        self._wrap_cache = {}
        self._angle_cache_last_access = {}
        self._wrap_cache_last_access = {}
        self._angle_cache_count = 0
        self._wrap_cache_count = 0
    def get_kappa(self):
        return self._kappa
    def set_kappa(self,kappa):
        self._kappa = kappa
        self.initialise_cache()
    def get_period(self):
        return self._period
    def get_seed(self):
        return self._seed
    def set_seed(self,seed):
        self._seed = seed
        self.initialise_cache()
    def node_number(self, t):
        return int(mpmath.floor(self.scale_t(t)/self._period))
    def node_angle(self, n):
        try:
            angle = self._angle_cache[n]
        except KeyError:
            self._rng.seed(self._seed+n)
            angle = self._rng.random()*self._tau
            self._angle_cache[n] = angle
        self._angle_cache_last_access[n] = self._angle_cache_count
        self._angle_cache_count += 1
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
            wrap = self._wrap_cache[n]
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
        self._wrap_cache_last_access[n] = self._wrap_cache_count
        self._wrap_cache_count += 1
        return wrap
    def value(self,t):
        st = self.scale_t(t)
        n = self.node_number(st)
        angle_minus = self.node_angle(n)
        angle_plus = self.node_angle(n+1)
        wrap = self.wrap_number(n)
        offset = angle_plus-angle_minus+self._tau*wrap
        ratio = (st-n*self._period)/self._period
        value = self.scurve(ratio)*offset + angle_minus
        return mpmath.fmod(value,self._tau)
    def cache_cleanup(self,threshold=100):
        angles_to_delete = [n for n in self._angle_cache.keys()
                            if self._angle_cache_count - self._angle_cache_last_access[n] > threshold]
        wraps_to_delete = [n for n in self._wrap_cache.keys()
                           if self._wrap_cache_count - self._wrap_cache_last_access[n] > threshold]
        for n in angles_to_delete:
            del self._angle_cache[n]
            del self._angle_cache_last_access[n]
        for n in wraps_to_delete:
            del self._wrap_cache[n]
            del self._wrap_cache_last_access[n]

