import maya.cmds
import random

# Shapes appear in the order below, randomly generated translation/rotation/size
# within a certain range so they can look uniform while still being random
# Alternating "inwards" and "outwards" direction/scaling/roation 

shapes = {
    1: maya.cmds.polyCube(),
    2: maya.cmds.polySphere(),
    3: maya.cmds.polyHelix(),
    4: maya.cmds.polyCone(),
    5: maya.cmds.polyPipe(),
    6: maya.cmds.polyTorus(),
    7: maya.cmds.polyPyramid(),
    8: maya.cmds.polyPlane(),
    9: maya.cmds.polyPrism(),
    10: maya.cmds.polyCylinder()
}
now = 1
for shape in shapes:
    current_shape = shapes[shape][0]
    maya.cmds.hide(current_shape)
    maya.cmds.currentTime(now)
    maya.cmds.setKeyframe(current_shape)

maya.cmds.select(cl = True)
now = 2
for shape in shapes:
    start_range = [-5,5]
    end_range = [-20,20]
    start_angle = [0,90]
    end_angle = [90,180]
    start_size = [1,2]
    end_size = [2,5]
    maya.cmds.currentTime(now)
    current_shape = shapes[shape][0]
    maya.cmds.showHidden(current_shape)
    if shape%2 == 0:
        temp = start_range
        start_range = end_range
        end_range = temp
    maya.cmds.setAttr(current_shape + ".translateX", random.randint(start_range[0], start_range[1]))
    maya.cmds.setAttr(current_shape + ".translateY", random.randint(start_range[0], start_range[1]))
    maya.cmds.setAttr(current_shape + ".translateZ", random.randint(start_range[0], start_range[1]))
    maya.cmds.setAttr(current_shape + ".rotateX", random.randint(start_angle[0], start_angle[1]))
    maya.cmds.setAttr(current_shape + ".rotateY", random.randint(start_angle[0], start_angle[1]))
    maya.cmds.setAttr(current_shape + ".rotateZ", random.randint(start_angle[0], start_angle[1]))
    maya.cmds.setAttr(current_shape + ".scaleX", random.randint(start_size[0], start_size[1]))
    maya.cmds.setAttr(current_shape + ".scaleY", random.randint(start_size[0], start_size[1]))
    maya.cmds.setAttr(current_shape + ".scaleZ", random.randint(start_size[0], start_size[1]))
    
    maya.cmds.setKeyframe(current_shape)
    now += 24
    maya.cmds.currentTime(now)
    maya.cmds.setAttr(current_shape + ".translateX", random.randint(end_range[0], end_range[1]))
    maya.cmds.setAttr(current_shape + ".translateY", random.randint(end_range[0], end_range[1]))
    maya.cmds.setAttr(current_shape + ".translateZ", random.randint(end_range[0], end_range[1]))
    maya.cmds.setAttr(current_shape + ".rotateX", random.randint(end_angle[0], end_angle[1]))
    maya.cmds.setAttr(current_shape + ".rotateY", random.randint(end_angle[0], end_angle[1]))
    maya.cmds.setAttr(current_shape + ".rotateZ", random.randint(end_angle[0], end_angle[1]))
    maya.cmds.setAttr(current_shape + ".scaleX", random.randint(end_size[0], end_size[1]))
    maya.cmds.setAttr(current_shape + ".scaleY", random.randint(end_size[0], end_size[1]))
    maya.cmds.setAttr(current_shape + ".scaleZ", random.randint(end_size[0], end_size[1]))
    maya.cmds.setKeyframe(current_shape)
    now += 1
    maya.cmds.currentTime(now)
    maya.cmds.hide(current_shape)
    maya.cmds.setKeyframe(current_shape)
    now += 24