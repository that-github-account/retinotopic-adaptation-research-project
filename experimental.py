class Endless_Test(object):
    
    def __init__(self, string, onEnd):
        
        self.string = ("The angle is " + str(string))
        self.onEnd = onEnd
        
    def printit(self):
        
        print(self.string)
        delay(1000)
        
        


    
#    if len(used_angles) < 360:
#        print(1)
#        new_angle = randint(0, 360)
#        print(new_angle)
#        if new_angle in used_angles:
#            print("used")
#        else:
#            used_angles.append(new_angle)
#            print("appended")
#    else:
#        for angles in used_angles:
#            if test == True and repositioned == False and next == False:
#                Collision.reposition(fixation_left.xpos, fixation_left.ypos, angles, 2)
#                repositioned = True
#            else:
#                if test == True and repositioned == True and next == False:
#                    fixation_left.display()
#                    Collision.display()
#                    Collision.single_iteration(speed)
#                    if Collision.iterations == 0:
#                        next = True
#                        repositioned = False
#                
#            if test == True and next == True and repositioned == False:
#                Collision.reposition(fixation_right.xpos, fixation_right.ypos, angles, 2)
#                repositioned = True
#            else:
#                if test == True and next == True and repositioned == True:
#                    fixation_right.display()
#                    Collision.display()
#                    Collision.single_iteration(speed)
#                    if Collision.iterations == 0:
#                        next = False
#                        repositioned = False
