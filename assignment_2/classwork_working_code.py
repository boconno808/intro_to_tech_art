'''
Apply a given animation onto a given character
and save the file via python
'''
import os
import maya.cmds

def create_reference(file_path, file_namespace):
    
    if not os.path.exists(file_path):
        
        maya.cmds.error("File does not exist: {0}".format(file_path))
        return
    
    maya.cmds.file(file_path, r = True, ns = file_namespace)
    
def connect_attributes(src, dst, attr):
    
    #given an attr, source and destination
    srcString = "{0}.{1}".format(src, attr)
    dstString = "{0}.{1}".format(dst, attr)
    
    maya.cmds.connectAttr(srcString, dstString, f = True)

def connect_attributes_joint(obj1_joint, obj2_joint):
    
    attr_list = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]
    
    for attr in attr_list: 
        connect_attributes(obj1_joint, obj2_joint, attr)
    
def connect_attributes_all_joints(ns1_all_joints, ns2_all_joints, ns1, ns2):
    hashset_ns1 = dict.fromkeys(ns1_all_joints, True)
    hashset_ns2 = dict.fromkeys(ns2_all_joints, True)

    # If the character has the joint give it animation
    for ns2_joint in ns2_all_joints:
        no_ns_joint = ns2_joint.split(":")[1]
        print "NO NS JOINT IS: {0}".format(no_ns_joint)
        ns1_joint = "{0}:{1}".format(ns1, no_ns_joint)
        print "NS1 JOINT IS: {0}".format(ns1_joint)
        if hashset_ns1.has_key(ns1_joint):
            connect_attributes_joint(ns1_joint, ns2_joint)


def create_file_namespace(file_path):
    
    if not os.path.exists(file_path):
        maya.cmds.error("File does not exist: {0}".format(file_path))
        return
    
    file_path_dir, file_path_fullname =  os.path.split(file_path)
    
    file_path_name, file_path_ext =  os.path.splitext(file_path_fullname)
    
    return file_path_name

def get_joints_from_namespace(ns):
    
    return maya.cmds.ls("{0}:*".format(ns), type = "joint")

def run():
    
    # Creates a new scene
    maya.cmds.file(new = True, force = True)
    
    # Create char and anim namespace
    char_path = "C:/Users/Imoto/Documents/maya/projects/homework2/character.mb"
    anim_path = "C:/Users/Imoto/Documents/maya/projects/homework2/animations/maya/01_01.ma"
    
    char_ns = create_file_namespace(char_path)
    anim_ns = create_file_namespace(anim_path)
    
    # Bring in character
    create_reference(char_path, char_ns)
    # Bring in the animation
    create_reference(anim_path, anim_ns)
    
    # get a list of joints for both anim and char

    char_joints = get_joints_from_namespace(char_ns)
    anim_joints = get_joints_from_namespace(anim_ns)
    
    # Attach animation to character 
    connect_attributes_all_joints(anim_joints, char_joints, anim_ns, char_ns)
    
     # Bake animation bones 
    
    maya.cmds.select(cl = True)
    maya.cmds.select(char_joints)
    
    start_time = maya.cmds.playbackOptions(q = True, min = True)
    end_time = maya.cmds.playbackOptions(q = True, max = True)
    
    maya.cmds.bakeResults(
                            simulation = True,
                            time = (start_time, end_time),
                            sampleBy = 1,
                            oversamplingRate = 1,
                            disableImplicitControl = True,
                            preserveOutsideKeys = True,
                            sparseAnimCurveBake = False,
                            removeBakedAnimFromLayer = False,
                            bakeOnOverrideLayer = False, 
                            minimizeRotation = True,
                            controlPoints = False,
                            shape = True
                            )
    # remove reference  
    maya.cmds.file("C:/Users/Imoto/Documents/maya/projects/homework2/animations/maya/01_01.ma", rr = True)
    
    # Save a file
    renamed_file = "C:/Users/Imoto/Documents/maya/projects/homework2/test.ma"
    
    maya.cmds.file(rename = renamed_file)
    maya.cmds.file(save = True, f = True)
    
run()