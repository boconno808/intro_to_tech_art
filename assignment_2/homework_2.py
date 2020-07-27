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
  
def connect_attributes_all_joints(ns1_all_joints, ns2_all_joints, ns1, ns2):
    
    hashset_ns1 = dict.fromkeys(ns1_all_joints, True)
    
    hashset_ns2 = dict.fromkeys(ns2_all_joints, True)
    
    hashset_fingers_left = {
        'LeftHandMiddle1': True,
        'LeftHandRing1': True,
        'LeftHandPinky1': True,
        'LeftHandIndex1': True
    }
    
    hashset_fingertips_left = {
        'LeftHandMiddle3': True,
        'LeftHandRing3': True,
        'LeftHandPinky3': True,
        'LeftHandIndex3': True,
        'LeftHandMiddle2': True,
        'LeftHandRing2': True,
        'LeftHandPinky2': True,
        'LeftHandIndex2': True
    }
    
    hashset_fingers_right = {
        'RightHandMiddle1': True,
        'RightHandRing1': True,
        'RightHandPinky1': True,
        'RightHandIndex1': True
    }
    
    hashset_fingertips_right = {
        'RightHandMiddle2': True,
        'RightHandRing2': True,
        'RightHandPinky2': True,
        'RightHandIndex2': True,
        'RightHandMiddle3': True,
        'RightHandRing3': True,
        'RightHandPinky3': True,
        'RightHandIndex3': True
    }
    
    hashset_no_mo = {
        'LeftArm':True,
        'RightArm':True,
        'LeftForeArm':True,
        'RightForeArm':True,
        'LeftFingerBase':True,
        'RightFingerBase':True
    }
    
    # If the character has the joint give it animation
    for ns2_joint in ns2_all_joints:
        no_ns_joint = ns2_joint.split(":")[1]
        ns1_joint = "{0}:{1}".format(ns1, no_ns_joint)
        
        # Thumbs has different naming
        if no_ns_joint == 'LeftHandThumb1':
            maya.cmds.parentConstraint('{0}:{1}'.format(ns1,'LThumb'), '{0}:{1}'.format(ns2, no_ns_joint), st = ["x", "y", "z"], mo = True)
        if no_ns_joint == 'LeftHandThumb3':
            maya.cmds.parentConstraint('{0}:{1}'.format(ns1,'LThumb_End'), '{0}:{1}'.format(ns2, no_ns_joint), st = ["x", "y", "z"], mo = True)
        if no_ns_joint == 'RightHandThumb1':
            maya.cmds.parentConstraint('{0}:{1}'.format(ns1,'RThumb'), '{0}:{1}'.format(ns2, no_ns_joint), st = ["x", "y", "z"], mo = True)
        if no_ns_joint == 'RightHandThumb3':
            maya.cmds.parentConstraint('{0}:{1}'.format(ns1,'RThumb_End'), '{0}:{1}'.format(ns2, no_ns_joint), st = ["x", "y", "z"], mo = True)
        
        # If animation has corresponding joint connect them
        if hashset_ns1.has_key(ns1_joint):
            
            if no_ns_joint == 'Spine1':
                maya.cmds.parentConstraint(ns1_joint, 'character:Spine3', st = ["x", "y", "z"], mo = True)
                
            elif no_ns_joint == 'Spine':
                maya.cmds.parentConstraint('{0}:{1}'.format(ns1, 'LowerBack'), 'character:Spine', mo = True)
                maya.cmds.parentConstraint(ns1_joint, 'character:Spine1',  st = ["x", "y", "z"], mo = True)
                maya.cmds.parentConstraint(ns1_joint, 'character:Spine2',  st = ["x", "y", "z"], mo = True)
                
            elif no_ns_joint == 'Hips':
                maya.cmds.parentConstraint(ns1_joint, ns2_joint)
                
            # Fixing the hands since rig has less fingers, this should only run for LeftHandIndex 1
            elif hashset_fingers_left.has_key(no_ns_joint):
                for left_finger in hashset_fingers_left: 
                    maya.cmds.parentConstraint(ns1_joint, '{0}:{1}'.format(ns2, left_finger), st = ["x", "y", "z"], mo = True)
                for left_fingertip in hashset_fingertips_left: 
                    maya.cmds.parentConstraint('{0}:{1}'.format(ns1, 'LeftHandIndex1_End'), '{0}:{1}'.format(ns2, left_fingertip), st = ["x", "y", "z"], mo = True)
                    
            elif hashset_fingers_right.has_key(no_ns_joint):
                for right_finger in hashset_fingers_right: 
                    maya.cmds.parentConstraint(ns1_joint, '{0}:{1}'.format(ns2, right_finger), st = ["x", "y", "z"], mo = True)
                for right_fingertip in hashset_fingertips_right: 
                    maya.cmds.parentConstraint('{0}:{1}'.format(ns1, 'RightHandIndex1_End'), '{0}:{1}'.format(ns2, right_fingertip), st = ["x", "y", "z"], mo = True)
            
            elif hashset_no_mo.has_key(no_ns_joint):
                maya.cmds.parentConstraint(ns1_joint, ns2_joint, st = ["x", "y", "z"])

            else: 
                maya.cmds.parentConstraint(ns1_joint, ns2_joint, st = ["x", "y", "z"], mo = True)

def create_file_namespace(file_path, needs_text):
    
    if not os.path.exists(file_path):
        maya.cmds.error("File does not exist: {0}".format(file_path))
        return
    
    file_path_dir, file_path_fullname =  os.path.split(file_path)
    
    file_path_name, file_path_ext =  os.path.splitext(file_path_fullname)
    
    if needs_text:
        
        file_path_name = 'anim{0}'.format(file_path_name)
    
    return file_path_name

def files_from_dir(directory):
    
    file_list = os.listdir(directory)
    
    return file_list

def get_joints_from_namespace(ns):
    
    return maya.cmds.ls("{0}:*".format(ns), type = "joint")

def import_file(file_path, file_namespace):
    
    if not os.path.exists(file_path):
        
        maya.cmds.error("File does not exist: {0}".format(file_path))
        return
    
    maya.cmds.file( file_path, i = True, ns = file_namespace )
  
def map_animation_to_char(anim_path, char_path, anim_file):
    
    char_ns = create_file_namespace(char_path, False)
    anim_ns = create_file_namespace(anim_path, True)
    
    # Bring in character
    import_file(char_path, char_ns)
    
    # Bring in the animation
    create_reference(anim_path, anim_ns)
    
    # Set the last keyframe to be as long as the reference animation 
    animCurves = maya.cmds.ls(type='animCurve')
    last = cmds.findKeyframe(animCurves, which='last')
    
    maya.cmds.playbackOptions(maxTime = last)
    
    # Get a list of joints for both anim and char
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
    # Remove reference  
    maya.cmds.file("C:/Users/Imoto/Documents/maya/projects/homework2/animations/maya/{0}".format(anim_file), rr = True)
    
def run():
    
    # Get all animation files in the animation folder
    anim_files = files_from_dir(r'C:/Users/Imoto/Documents/maya/projects/homework2/animations/maya/')

    for anim_file in anim_files:
    
        # Creates a new scene
        maya.cmds.file(new = True, force = True)
        maya.cmds.currentUnit( time = '120fps' )
        
        # Create char and anim namespace
        char_path = "C:/Users/Imoto/Documents/maya/projects/homework2/character.mb"
        anim_path = "C:/Users/Imoto/Documents/maya/projects/homework2/animations/maya/{0}".format(anim_file)
        
        map_animation_to_char(anim_path, char_path, anim_file)

        # Save a file
        renamed_file = "anim{0}".format(anim_file)
        
        maya.cmds.file(rename = renamed_file)
        maya.cmds.file(save = True, type='mayaAscii', f = True)       
        
run()