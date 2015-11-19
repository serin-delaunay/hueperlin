
# coding: utf-8

# In[17]:

import wrap_noise
import mpmath
import math
import stationary_noise


# In[15]:

class AngleNoise:
    def __init__(self,circumference=2*mpmath.pi,wrap_args={},stationary_args={}):
        self.stationary = stationary_noise.StationaryNoise(**stationary_args)
        self.wrap = wrap_noise.WrapNoise(**wrap_args)
        self._tau = 2*mpmath.pi
        self.circumference=circumference
    def value(self,t):
        w = self.wrap.value(t)*self.circumference/self._tau
        s = self.stationary.value(t)
        return float(mpmath.fmod(w + s, self.circumference))

