
# coding: utf-8

# In[2]:

import angle_noise
import stationary_noise


# In[3]:

class ColourNoise:
    def __init__(self,colour_converter=lambda x:x,
                 hue_circumference=360.0,
                 hue_wrap_args={}, hue_stationary_args={},
                 saturation_args={},
                 lightness_args={}):
        self.hue = angle_noise.AngleNoise(hue_circumference,hue_wrap_args,hue_stationary_args)
        self.saturation = stationary_noise.StationaryNoise(**saturation_args)
        self.lightness = stationary_noise.StationaryNoise(**lightness_args)
        self.colour_converter=colour_converter
    def value(self,t):
        return self.colour_converter((self.hue.value(t),
                                      self.saturation.value(t),
                                      self.lightness.value(t)))

