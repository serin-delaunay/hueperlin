
# coding: utf-8

# In[1]:

from __future__ import division
import sfml


# In[3]:

class GradientBox(sfml.TransformableDrawable):
    def __init__(self, nodes):
        assert nodes > 1
        self.nodes = nodes
        self.vertices = sfml.VertexArray(sfml.PrimitiveType.TRIANGLES_STRIP,nodes*2)
        for i in range(nodes):
            x = i/(nodes-1)
            self.vertices[2*i].position = sfml.Vector2(x,0.0)
            self.vertices[2*i+1].position = sfml.Vector2(x,1.0)
    def colourise(self,colouriser):
        for i in range(self.nodes):
            colour = colouriser(i/(self.nodes-1))
            self.vertices[2*i].color = colour
            self.vertices[2*i+1].color = colour
    def draw(self,target,states):
        states.transform *= self.transform
        target.draw(self.vertices,states)

