import bpy
from camera_matrix_calc import *


frameNumber = 1

def initObj(obj = "Robot", pos = [0,0,0], rot = [0,0,0]):
    #initilize the object
    robot = bpy.data.objects[obj]
    #set the frame number at which we are about to change
    frameNumber = 1
    bpy.context.scene.frame_set(frameNumber)
    #set the position(absolute) of robot
    robot.location = pos
    #set the rotation in radians
    robot.rotation_euler = rot
    

#move robot, takes relative parameters    
def move(obj = "Robot", dPosb = [0,0,0], drot = [0,0,0], dFrame = 0):
    #initilize the object
    robot = bpy.data.objects[obj]
    #set the frame number at which we are about to change
    frameNumber += dFrame
    bpy.context.scene.frame_set(frameNumber)
    #set the position(absolute) of robot
    robot.location += dPosb
    #set the rotation in radians
    robot.rotation_euler += drot
    
def clickPicture(resx = 640, resy = 480, frameNo = 1, sampleNo = 64, location = "/", name = ["PhotoL","PhotoR"]):
    #set render engine
    bpy.context.scene.render.engine = 'CYCLES'
    #set the output resolution
    bpy.context.scene.render.resolution_x = resx
    bpy.context.scene.render.resolution_y = resy
    
    bpy.context.scene.render.resolution_percentage = 100
    
    bpy.context.scene.frame_current = frameNo
    bpy.context.scene.cycles.samples = sampleNo
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    
    #select active camera and clcik photo
    bpy.context.scene.camera = bpy.data.objects["Camera.L"]
    bpy.context.scene.render.filepath = location + "/" + str(name[0])
    bpy.ops.render.render(write_still=True, use_viewport=True)
    
    #select active camera and click photo
    bpy.context.scene.camera = bpy.data.objects["Camera.R"]
    bpy.context.scene.render.filepath = location + "/" + str(name[1])
    bpy.ops.render.render(write_still=True, use_viewport=True)


def getCameraPose():
    camL_loc = bpy.data.objects["Camera.L"].location
    camL_rot = bpy.data.objects["Camera.L"].rotation_euler
    
    camR_loc = bpy.data.objects["Camera.R"].location
    camR_rot = bpy.data.objects["Camera.R"].rotation_euler
    
    pose = {"Camera.L" : [camL_loc, camL_rot], "Camera.R" : [camR_loc, camR_rot]}
    
    return pose



def getMatrix():
  import scipy.io as io
  import numpy as np
  points = io.loadmat('/Users/homeimac/Documents/BlenderPython-master/triangulated_points.mat')
  length = len(points["X"][0])

  cordinates = []
  for i in range(length):
    #extract the point
    x = points['X'][0][i]
    y = points['Y'][0][i]
    z = points['Z'][0][i]
    p = np.array([x, y, z])
    cordinates.append(p)

  return np.array(cordinates)


def initDots(positions, size = 0.02):
    
    for position in positions:
        bpy.ops.mesh.primitive_uv_sphere_add(size=size, view_align=False, enter_editmode=False, location=position, layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


def deleteObj(obj):
    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select the object
    bpy.data.objects[obj].select = True    # Blender 2.7x

    # https://wiki.blender.org/wiki/Reference/Release_Notes/2.80/Python_API/Scene_and_Object_API
    #bpy.data.objects['Camera'].select_set(True) # Blender 2.8x

    bpy.ops.object.delete()
    
def deleteDots():
    s = 'Sphere'
    
    deleteObj(s)
    for i in range(1,133):
        st = s + '.' + '%03d'%(int('000')+i)
        print(st)
        deleteObj(st)
        
        


def clickRoundPictures(focus = [0,5,0], n = 8, r = 5):
    import numpy as np
    
    distance = (focus) - np.array(bpy.data.objects["Robot"].location)
    radius = r
    step_theta = 2*np.pi/n
    
    for i in range(n):
        x = radius*np.cos(step_theta*(i)) + focus[0]
        y = radius*np.sin(step_theta*(i)) + focus[1]
        rotation = np.pi/2 + step_theta*(i)
        
        #moverobot
        robot = bpy.data.objects["Robot"]
        
        #set the position(absolute) of robot
        robot.location = [x,y,robot.location[2]]
        #set the rotation in radians
        robot.rotation_euler = [0,0,rotation]
        clickPicture(name = ["Photo_Left_" + str(i), "Photo_Right_" + str(i)])
        
        #also save matrix values
        cam = bpy.data.objects['Camera.L']
        P, K, RT = get_3x4_P_matrix_from_blender(cam)

        p = "/Users/homeimac/Documents/BlenderPython-master/"
        np.savetxt(p + "P_Matrix_Left" + str(i) + ".txt", np.array(P))
        np.savetxt(p + "K_Matrix_Left" + str(i) + ".txt", np.array(K))
        np.savetxt(p + "RT_Matrix_Left" + str(i) + ".txt", np.array(RT))
        
        cam = bpy.data.objects['Camera.R']
        P, K, RT = get_3x4_P_matrix_from_blender(cam)
        
        np.savetxt(p + "P_Matrix_Right" + str(i) + ".txt", np.array(P))
        np.savetxt(p + "K_Matrix_Right" + str(i) + ".txt", np.array(K))
        np.savetxt(p + "RT_Matrix_Right" + str(i) + ".txt", np.array(RT))
        
        
clickRoundPictures()