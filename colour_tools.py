
# coding: utf-8

# In[3]:

import sfml
import husl
from collections import namedtuple
import math


# In[5]:

argb=namedtuple('argb',['a','r','g','b'])

def rgba_to_sfml(rgba):
    return sfml.Color(rgba.r,rgba.g,rgba.b,rgba.a)
def husl_to_rgba(hue,saturation,lightness):
    return argb(255,*[255*x for x in husl.husl_to_rgb(hue,saturation,lightness)])
def husl_to_sfml(hue,saturation,lightness):
    return rgba_to_sfml(husl_to_rgba(hue,saturation,lightness))
def colouriser(xy,saturation=-1,lightness=-1):
    angle = math.atan2(xy.y,xy.x)*360/(2*math.pi)
    r = math.hypot(xy.x,xy.y)
    if saturation == -1:
        saturation = 100*r
    if lightness == -1:
        lightness = 100*r
    return husl_to_rgba(angle,saturation,lightness)
def blend_colours(c1,c2,ratio,verbose=False):
    epsilon=0.01
    ratiom = 1-ratio
    r = c1.r*ratiom+c2.r*ratio
    g = c1.g*ratiom+c2.g*ratio
    b = c1.b*ratiom+c2.b*ratio
    a = c1.a*ratiom+c2.a*ratio
    if (r<-epsilon or g < -epsilon or b < -epsilon or a < -epsilon) and verbose:
        print c1
        print c2
        print r,g,b,a, ratio
    return sfml.Color(int(r),int(g),int(b),int(a))

