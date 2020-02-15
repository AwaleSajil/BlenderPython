import bpy

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
    
def clickPicture(resx = 640, resy = 480, frameNo = 1, sampleNo = 64, location = "/"):
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
    bpy.context.scene.render.filepath = location + "/PhotoL"
    bpy.ops.render.render(write_still=True, use_viewport=True)
    
    #select active camera and click photo
    bpy.context.scene.camera = bpy.data.objects["Camera.R"]
    bpy.context.scene.render.filepath = location + "/PhotoR"
    bpy.ops.render.render(write_still=True, use_viewport=True)


def getCameraPose():
    camL_loc = bpy.data.objects["Camera.L"].location
    camL_rot = bpy.data.objects["Camera.L"].rotation_euler
    
    camR_loc = bpy.data.objects["Camera.R"].location
    camR_rot = bpy.data.objects["Camera.R"].rotation_euler
    
    pose = {"Camera.L" : [camL_loc, camL_rot], "Camera.R" : [camR_loc, camR_rot]}
    
    return pose






print(getCameraPose())

    