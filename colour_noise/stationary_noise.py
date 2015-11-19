
# coding: utf-8

# In[1]:

import noise


# In[ ]:

class StationaryNoise:
    def __init__(self,
                 frequency=1.0,amplitude=1.0,mean=0.0,
                 lacunarity=2.0,persistence=0.5,octaves=16,
                 repeat=2**20,base=0):
        self.frequency = frequency
        self.amplitude = amplitude
        self.mean = mean
        self.lacunarity = lacunarity
        self.persistence = persistence
        self.octaves = octaves
        self.repeat = repeat
        self.base = base
    def value(self,t):
        p = noise.pnoise1(t*self.frequency,
                          octaves=self.octaves,
                          lacunarity=self.lacunarity,
                          persistence = self.persistence,
                          repeat = self.repeat,
                          base=self.base)
        return self.mean + self.amplitude*p

