
# coding: utf-8

# In[53]:

from __future__ import division
import sfml
import gradient_box
import angle_noise
import colour_tools
import math


# In[81]:

class ColourHistory(sfml.TransformableDrawable):
    def __init__(self,colour_source,interval,tail_length):
        self._colour_source = colour_source
        self._interval = interval
        self.update_length(tail_length)
        self._it = None
    def build_box(self):
        self._box = gradient_box.GradientBox(self._length-2)
    def update_length(self,tail_length):
        self._tail_length = tail_length
        self._length = 2*tail_length+1
        self.initialise_history()
        self.build_box()
    def initialise_history(self):
        self._history = [sfml.Color.BLACK]*self._length
    def it(self,t):
        return int(math.floor(t/self._interval))
    def t(self,it):
        return float(it*self._interval)
    def slot(self,it):
        return ((it%self._length)+self._length)%self._length
    def update_slot(self,it):
        slot = self.slot(it)
        t = self.t(it)
        colour = self._colour_source(t)
        self._history[slot] = colour_tools.husl_to_rgba(*colour)
    def update_all(self,t):
        self._it = self.it(t)
        for i in range(self._it-self._tail_length,
                       self._it+self._tail_length+1):
            self.update_slot(i)
    def value(self,t):
        assert t <= self.t(self._it+self._tail_length)
        assert t >= self.t(self._it-self._tail_length)
        it = self.it(t)
        r = t/self._interval - it
        slot = self.slot(it)
        return colour_tools.blend_colours(self._history[slot],
                                          self._history[(slot+1)%self._length],
                                          r, True)
    def update_t(self,t):
        it = self.it(t)
        dit = it-self._it
        if dit != 0:
            new_max = it + self._tail_length
            new_min = it - self._tail_length
            if dit > 0:
                new_min = max(new_min,new_max-dit+1)
            else:
                new_max = min(new_max,new_min-dit-1)
        else:
            return
        for i in range(new_min,new_max+1):
            self.update_slot(i)
        self._it = it
    def update_gradient(self,t):
        self.update_t(t)
        for i in range(-self._tail_length+1,self._tail_length):
            tt = t + i*self._interval
            colour = self.value(tt)
            step = i + self._tail_length-1
            self._box.vertices[2*step].color = colour
            self._box.vertices[2*step+1].color = colour
    def draw(self,target,states):
        states.transform *= self.transform
        target.draw(self._box,states)

