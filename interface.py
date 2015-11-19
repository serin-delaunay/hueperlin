
# coding: utf-8

# In[1]:

import sfml
import math
import time
import cPickle as pickle
import colour_noise
import gradient_circle
import gradient_box
import colour_tools
import colour_history
reload(colour_history)


# In[2]:

c1centre = sfml.Vector2(200.0,300.0)
c2centre = sfml.Vector2(600.0,300.0)
cscale = 100
circle_count = 51
circle_step = 100.0/(circle_count-1)
crings = 8
csectors = 40
circle1 = gradient_circle.GradientCircle(csectors,crings)
circle1.move(c1centre)
circle1.scale((cscale,cscale))
circle2 = gradient_circle.GradientCircle(csectors,crings)
circle2.move(c2centre)
circle2.scale((cscale,cscale))

try:
    f = open('circles.pck','rb')
    (ccs_saturation, ccs_lightness) = pickle.load(f)
    assert len(ccs_saturation)==circle_count, 'wrong number of circles (saturation)'
    assert len(ccs_lightness)==circle_count, 'wrong number of circles (lightness)'
    assert len(ccs_saturation[0])==crings, 'wrong number of rings (saturation)'
    assert len(ccs_lightness[0])==crings, 'wrong number of rings (lightness)'
    assert len(ccs_saturation[0][1])==(csectors+1)*2, 'wrong number of vertices in a ring (saturation)'
    assert len(ccs_lightness[0][1])==(csectors+1)*2, 'wrong number of vertices in a ring (lightness)'
except (IOError,EOFError,AssertionError) as e:
    print e.args, e.message
    ccs_saturation = [circle1.get_colourisation(lambda x:colour_tools.colouriser(x,saturation=saturation*circle_step))
                      for saturation in range(0,circle_count)]
    ccs_lightness = [circle1.get_colourisation(lambda x:colour_tools.colouriser(x,lightness=lightness*circle_step))
                     for lightness in range(0,circle_count)]
    f = open('circles.pck','wb')
    pickle.dump((ccs_saturation,ccs_lightness),f)
finally:
    f.close()


# In[3]:

crosshair_fn = 'crosshair.png'
ch_texture = sfml.Texture.from_file(crosshair_fn)
ch_sprite = sfml.Sprite(ch_texture)
ch_size = ch_sprite.texture_rectangle.size

window_v_fn = 'window_v.png'
wv_texture = sfml.Texture.from_file(window_v_fn)
wv_sprite = sfml.Sprite(wv_texture)
#wv_size = wv_sprite.texture_rectangle.size
wv_offset = sfml.Vector2(-4,-3)

window_h_fn = 'window_h.png'
wh_texture = sfml.Texture.from_file(window_h_fn)
wh_sprite = sfml.Sprite(wh_texture)
#wh_size = wh_sprite.texture_rectangle.size
wh_offset = sfml.Vector2(-3,-4)


# In[4]:

bsize = sfml.Vector2(100.0,50.0)
bpos = sfml.Vector2(400.0,325.0)
bhsize = sfml.Vector2(100.0,50.0)
bhpos = sfml.Vector2(400.0,275.0)
box = sfml.RectangleShape()
box.size = bsize
box.position = bpos
box.position -= bsize/2
boxhue = sfml.RectangleShape()
boxhue.size = bhsize
boxhue.position = bhpos
boxhue.position -= bhsize/2


# In[5]:

gradient_box_steps = 5
gradient_box_rotation = 270.0
gradient_box_length = 200.0
gradient_box_width = 26.0
gradient_box_y = 400.0
gradient_s_x = 750.0-0.5*gradient_box_width
gradient_l_x = 50.0-0.5*gradient_box_width

gradient_s = gradient_box.GradientBox(gradient_box_steps)
gradient_l = gradient_box.GradientBox(gradient_box_steps)

gradient_s.rotate(gradient_box_rotation)
gradient_l.rotate(gradient_box_rotation)

gradient_s.scale((gradient_box_length,gradient_box_width))
gradient_l.scale((gradient_box_length,gradient_box_width))

gradient_s.move((gradient_s_x,gradient_box_y))
gradient_l.move((gradient_l_x,gradient_box_y))


# In[6]:

cn = colour_noise.ColourNoise()
cn.hue.circumference = 360.0
cn.hue.stationary.amplitude=480.0
cn.hue.stationary.frequency=0.02
cn.hue.wrap.frequency=0.005
cn.hue.wrap.set_seed(time.time())

cn.saturation.amplitude=50
cn.saturation.mean=50
cn.saturation.frequency=0.1

cn.lightness.amplitude=50
cn.lightness.mean=50
cn.lightness.frequency=0.02
#cn.colour_converter=lambda hsl:husl_to_sfml(*hsl)


# In[7]:

history_size = (600,26)
history_position = (100,450-13)
history_hue_position = (100,450+32-13)
history = colour_history.ColourHistory(lambda t: cn.value(t),0.1,200)
history_hue = colour_history.ColourHistory(lambda t: (cn.value(t)[0],100,50),0.1,200)
history.update_all(0.0)
history_hue.update_all(0.0)
history.scale(history_size)
history_hue.scale(history_size)
history.move(history_position)
history_hue.move(history_hue_position)


# In[8]:

def draw_colour(hue,saturation,lightness):
    isaturation = int(min(circle_count-2,saturation/circle_step))
    ilightness = int(min(circle_count-2,lightness/circle_step))
    rsaturation = saturation/circle_step-isaturation
    rlightness = lightness/circle_step-ilightness
    circle1.blend_colourisations(ccs_saturation[isaturation],
                                 ccs_saturation[isaturation+1],
                                 rsaturation)
    circle2.blend_colourisations(ccs_lightness[ilightness],
                                 ccs_lightness[ilightness+1],
                                 rlightness)
    box.fill_color = colour_tools.husl_to_sfml(hue,saturation,lightness)
    boxhue.fill_color = colour_tools.husl_to_sfml(hue,100.0,50.0)
    w.draw(circle1)
    w.draw(circle2)
    
    angle = hue*2*math.pi/360
    angle_vector = sfml.Vector2(math.cos(angle),math.sin(angle))
    rl = lightness*cscale/100
    rs = saturation*cscale/100
    
    chpos1 = c1centre + angle_vector*rl - ch_size/2
    chpos2 = c2centre + angle_vector*rs - ch_size/2
    ch_sprite.position = chpos1
    w.draw(ch_sprite)
    ch_sprite.position = chpos2
    w.draw(ch_sprite)
    
    w.draw(box)
    w.draw(boxhue)
    
    w.draw(history)
    wv_sprite.position = (history_position +
                          sfml.Vector2(history_size[0]/2.0,0.0)+
                          wv_offset)
    w.draw(wv_sprite)
    w.draw(history_hue)
    wv_sprite.position = (history_hue_position +
                          sfml.Vector2(history_size[0]/2.0,0.0)+
                          wv_offset)
    w.draw(wv_sprite)
    
    gradient_s.colourise(lambda r: colour_tools.husl_to_sfml(hue,100.0*r,lightness))
    gradient_l.colourise(lambda r: colour_tools.husl_to_sfml(hue,saturation,100.0*r))
    w.draw(gradient_s)
    w.draw(gradient_l)
    
    wh_sprite.position = (gradient_s.position - 
                          sfml.Vector2(0.0,saturation*gradient_box_length/100.0) +
                          wh_offset)
    w.draw(wh_sprite)
    wh_sprite.position = (gradient_l.position - 
                          sfml.Vector2(0.0,lightness*gradient_box_length/100.0) +
                          wh_offset)
    w.draw(wh_sprite)


# In[15]:

w = sfml.RenderWindow(sfml.VideoMode(800,600),"Hue Noise",sfml.Style.CLOSE)
w.vertical_synchronization = True
w.framerate_limit = 60
t = time.time()
start_time = time.time()
frame_count = 0
while(w.is_open):
    for e in w.events:
        if type(e) is sfml.CloseEvent:
            w.close()
    w.clear()
    tc = time.time()-start_time
    hsl = cn.value(tc)
    history.update_gradient(tc)
    history_hue.update_gradient(tc)
    draw_colour(*hsl)
    w.display()
    tt = time.time()
    delta_t = tt-t
    frame_count += 1
    if delta_t > 0.5:
        fps = frame_count/delta_t
        w.title = "Hue Noise ({0} fps)".format(int(fps))
        frame_count = 0
        t = tt
w.close()


# In[10]:

w.close()

