
# coding: utf-8

# In[4]:

from __future__ import division
import math
import sfml
import colour_tools


# In[2]:

class GradientCircle(sfml.TransformableDrawable):
    def __init__(self,sectors,rings):
        va = sfml.VertexArray(sfml.PrimitiveType.TRIANGLES_FAN,2+sectors)
        va[0].position = (0,0)
        for j in range(sectors+1):
            angle = 2*math.pi*j/sectors
            r = 1.0/rings
            va[j+1].position = (r*math.cos(angle),r*math.sin(angle))
        self.rings = [va]
        for i in range(1,rings):
            rmin = 1.0/rings*i
            rmax = 1.0/rings*(i+1)
            va = sfml.VertexArray(sfml.PrimitiveType.TRIANGLES_STRIP,2*(sectors+1))
            for j in range(sectors+1):
                angle = 2*math.pi*j/sectors
                va[2*j].position = (rmin*math.cos(angle),rmin*math.sin(angle))
                va[2*j+1].position = (rmax*math.cos(angle),rmax*math.sin(angle))
            self.rings.append(va)
    def draw(self,target,states):
        states.transform *= self.transform
        for va in self.rings:
            target.draw(va,states)
    def colourise(self,colouriser):
        for va in self.rings:
            for v in va:
                v.color = colouriser(v.position)
    def get_colourisation(self,colouriser):
        colourisation=[]
        for va in self.rings:
            ring_colourisation = []
            for v in va:
                ring_colourisation.append(colouriser(v.position))
            colourisation.append(ring_colourisation)
        return colourisation
    def apply_colourisation(self,colourisation):
        for va, ring_colours in zip(self.rings,colourisation):
            for v,colour in zip(va,ring_colours):
                v.color = colour
    def blend_colourisations(self,col1,col2,r):
        for va, rcol1,rcol2 in zip(self.rings,col1,col2):
            for v,col1,col2 in zip(va,rcol1,rcol2):
                v.color = colour_tools.blend_colours(col1,col2,r)

