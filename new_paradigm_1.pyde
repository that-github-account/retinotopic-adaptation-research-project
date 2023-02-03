#NOTES:

#The current speed error may be occuring due to reoccuring values, i.e., 3.3333... or 6.6666...
#Match the speed and the distance.

#CSV file, one line per participant
#Dictionary as list of lists or strings. 
#Keep demographics in order!


#Some trials and count whether pp are able to understand. 

#Think about reaction time
#Dictionary rather than list
#Print it to the csv file

#Write check for speed so there is no reciprocal 

#Fixation_cross speed might need to be adjusted

#----------------
#Pre-Requisits 
import random
import time



#Settings-------------------------------------------
WindowX = 1920
WindowY = 1080

speed = 20
example_speed = 2.5
fixation_cross_speed_adjust = 0.1 #must be multiple of 10 as based on visual degree calculations

visual_degree_disc_size = 1.5
fixation_cross_size = 10

visual_degree_fixation_location = 5
distance_from_screen = 500 #in mm

n_angles_pre_test = 2 #total 180
n_angles_post_test = 2 #total 180
n_angles_adaptation = 2 #usually 640
n_angles_practice = 2 #total 18
n_angles_top_up = 16 #set to 16

adaptation_sequence_intertrial_delay = 100

autostart = False
sequence = ""
repositioned = False
next = False
experimental = False
require_response_switch = True
#----------------------------------------------------

#Setting up functions
from classes import Collision
from fixation_locations import Fixation_Dot
from experimental_ import Endless_Test
from responses import Responses
from text import Text

#Visual Degree Conversion
screen_horizontal_ratio = 1920/509.76 #pixels per mm
screen_vertical_ratio = 1080/286.74 #pixels per mm

visual_degree_fixation_location_in_radian = radians(visual_degree_fixation_location)
visual_degree_disc_size_in_radian = radians(visual_degree_disc_size)

screen_size_of_fixation_location = tan(visual_degree_fixation_location_in_radian)*distance_from_screen
screen_size_of_disc_size = tan(visual_degree_disc_size_in_radian)*distance_from_screen

fixation_location_in_pixels = round(screen_size_of_fixation_location*screen_horizontal_ratio, 2)
disc_size_in_pixels = round(screen_size_of_disc_size*screen_horizontal_ratio, 2) #note that the disc needs to be defined along the X and Y axis but as we are displaying a circle both ratios would return the same size



#Speeds
fixation_cross_speed = fixation_location_in_pixels*fixation_cross_speed_adjust

#Compiling Data Structure and Trial Lists 
    
possible_overlap = [0, 0.125, 0.25, 0.375, 0.5, 0.675, 0.75, 0.875, 1]

trial_overlap_left = []
trial_overlap_right = []

for x in range(0, 10):
    x = list(possible_overlap)
    trial_overlap_left.append(x)
    trial_overlap_right.append(x)
    
trial_overlap_left = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, trial_overlap_left) for i in b]
trial_overlap_right = [i for b in map(lambda x:[x] if not isinstance(x, list) else x, trial_overlap_right) for i in b]

dictionary_trials = {}
    
for x in range(0, 180):
    if len(trial_overlap_left) > 0:
        overlap = random.choice(trial_overlap_left)
        dictionary_trials[x] = {"overlap": overlap, "location": "left"}
        trial_overlap_left.remove(overlap)
    else:
        overlap = random.choice(trial_overlap_right)
        dictionary_trials[x] = {"overlap": overlap, "location": "right"}
        trial_overlap_right.remove(overlap)
            
dictionary_trials2 = dict(dictionary_trials)

dictionary_practice_trials = {}

overlap_practice_trials_l = list(possible_overlap)
overlap_practice_trials_r = list(possible_overlap)

for x in range(0, 18):
    if len(dictionary_practice_trials) < 9:
        overlap = random.choice(overlap_practice_trials_l)
        dictionary_practice_trials[x] = {"overlap": overlap, "location": "left"}
        overlap_practice_trials_l.remove(overlap)
    else:
        overlap = random.choice(overlap_practice_trials_r)
        dictionary_practice_trials[x] = {"overlap": overlap, "location": "right"}
        overlap_practice_trials_r.remove(overlap)        
    

angles_pre_adaptation = []
while len(angles_pre_adaptation) < n_angles_pre_test:
    new_angle = random.randint(0, 360)
    if new_angle not in angles_pre_adaptation:
        angles_pre_adaptation.append(new_angle)
        
angles_adaptation = []
while len(angles_adaptation) < n_angles_adaptation:
    new_angle = random.randint(-360, 360)
    if new_angle not in angles_adaptation:
        angles_adaptation.append(new_angle)
        
angles_post_adaptation = []
while len(angles_post_adaptation) < n_angles_post_test:
    new_angle = random.randint(0, 360)
    if new_angle not in angles_post_adaptation:
        angles_post_adaptation.append(new_angle)
        
top_up_angles = []
while len(top_up_angles) < 180*n_angles_top_up:
    new_angle = random.randint(0,360)
    top_up_angles.append(new_angle)        

initial_fixation = random.randint(0, 1)

if initial_fixation == 0:
    trial_fixation = "left"
    adaptation_fixation = "right"
else:
    trial_fixation = "right"
    adaptation_fixation = "left"



#Defining Functions
Collision = Collision(0, 100, disc_size_in_pixels, WindowX, WindowY, fixation_location_in_pixels)
fixation_dot = Fixation_Dot(WindowX, WindowY, fixation_location_in_pixels, fixation_cross_size, fixation_cross_speed)
response_request = Responses(WindowX, WindowY)
txt = Text(WindowX, WindowY)



#Defining additional variables
delaysequence = 0
value = 0
timeinms = 0

practice_counter = []
practice_time = 0

count_for_top_up = n_angles_top_up

example_intro = "none"

example_counter = {"LAUNCH": 0, "PASS": 0}



#Checks

print("Pre-Adaptation Trials" + str(len(dictionary_trials)))
print("Post-Adaptation Trials" + str(len(dictionary_trials2)))
print("Practice Trials" + str(len(dictionary_practice_trials)))
print("Angles pre-a" + str(len(angles_pre_adaptation)))
print("Angles a" + str(len(angles_adaptation)))
print("Angles post-a" + str(len(angles_post_adaptation)))
print("Angles top_up" + str(len(top_up_angles)/16))


def setup():
    fullScreen()
    frameRate(60)
    
def draw():
    background(0)

    #Settings
    show_FPS = False
    display_grid = False
    check_display_circularity = False
    display_visualdegree = False
    check_animation_time = False
    
    test = False    
    

    
    #Global variables 
    global repositioned
    global next
    global experimental
    global autostart
    global sequence
    global require_response_switch
    global visualdegree
    global delaysequence
    global value
    global timeinms
    global begin_practice_trials
    global count_for_top_up
    global example_intro
    global adaptation_sequence_intertrial_delay
    global example_speed
    global n_angles_practice
    global n_angles_top_up
    global example_counter

        
    if experimental == True:  
        print("none")
    
    if autostart == False:
        
        if keyPressed: 
            if key == ENTER:
                print("Loading Experiment ... Please Wait")
                autostart = True
                sequence = "Introduction"
                delay(500)
                
            if key == TAB:
                print("Admin Access")
                experimental = True
                delay(2000)
        else:
            txt.start_message_display()
            
    else:
        
        
##------Introduction 

        if sequence == "Introduction":
            
            if keyPressed:
                if key == "d":
                    example_intro = "launch"
                    delaysequence = "wait"
                    timeinms = millis()
                    
                if key == "k":
                    example_intro = "pass"
                    delaysequence = "wait"
                    timeinms = millis()
                
                if key == ENTER:
                    sequence = "starting practice"
                    timeinms = millis()

                    
            if example_intro == "launch":
                
                txt.example_instructions_header()
                txt.example_launch()
                
                if delaysequence == "wait":
                    
                    if millis() - timeinms < 500:
                        background(0)
                        txt.example_instructions_header()
                        txt.example_launch()
                    else:
                        delaysequence = 0
                else:
                    
                    if repositioned == False:
                        
                        fixation_dot.refixate(adaptation_fixation)
                        
                        Collision.reposition(fixation_dot.xpos, "override; adaptation", fixation_dot.ypos, 45, 0, 1)
                        
                        example_counter["PASS"] = example_counter["PASS"] + 1
                        
                        repositioned = True
                            
                    else:
                            
                        if repositioned == True:
    
                            Collision.single_iteration(example_speed)
                            
                            if Collision.iterations == 0:
                                
                                repositioned = False
                                example_intro = "wait"
                                timeinms = millis()
                            
            if example_intro == "pass":
                
                txt.example_instructions_header()
                txt.example_pass()
                
                if delaysequence == "wait":
                    
                    if millis() - timeinms < 500:
                        background(0)
                        txt.example_instructions_header()
                        txt.example_pass()
                    else:
                        delaysequence = 0
                else:
                    
                    if repositioned == False:
                        
                        fixation_dot.refixate(adaptation_fixation)
                        
                        Collision.reposition(fixation_dot.xpos, "override; adaptation", fixation_dot.ypos, 45, 1, 1)
                        
                        example_counter["LAUNCH"] = example_counter["LAUNCH"] + 1
                        
                        repositioned = True
                            
                    else:
                            
                        if repositioned == True:
    
                            Collision.single_iteration(example_speed)
                            
                            if Collision.iterations == 0:
                                
                                repositioned = False
                                example_intro = "wait"
                                timeinms = millis()
                            
            if example_intro == "wait":
                    
                if millis() - timeinms < 500:
                    background(0)
                    txt.example_instructions_header()
                else:
                    example_intro = "none"
                            
            if example_intro == "none":
                txt.main_instructions_display()        
        
        
        
        
        
##------Practice
        
        if sequence == "starting practice":
            if keyPressed and millis() - timeinms > 500:
                if key == ENTER:
                    sequence = "Practice"
                    delaysequence = "wait"
                    timeinms = millis()
            else:
                txt.practice_instructions_display()
        
        if sequence == "Practice":
            
            fixation_dot.refixate(trial_fixation)
            fixation_dot.display()
            
            if delaysequence == "wait":
            
                if millis() - timeinms < 1500:
                    fixation_dot.refixate(trial_fixation)
                    fixation_dot.display()
                else:
                    delaysequence = 0
                    
                    repositioned = False
            
            else:
                
                
                if repositioned == False:
                    
                    #print("The number of trials left is " + str(len(dictionary_practice_trials)) + ".")
                    
                    number_of_trial = random.choice(list(dictionary_practice_trials.keys()))
                    dict_of_trial = dictionary_practice_trials.get(number_of_trial)
                    dictionary_practice_trials.pop(number_of_trial)
        
                    overlap = dict_of_trial["overlap"]
                    location = dict_of_trial["location"]
                        
                    Collision.reposition(fixation_dot.xpos, location, fixation_dot.ypos, 45, overlap, 1)
                    
                    repositioned = True
                        
                else:
                        
                    if repositioned == True and response_request.awaiting_response == False:

                        Collision.single_iteration(speed)
                        
                        if Collision.iterations == 0:
                            
                            response_request.awaiting_response = True
                            
                    else:
                        if response_request.awaiting_response == True:
                            
                            response_request.get_response_practice(fixation_dot.xpos, fixation_dot.ypos)
                            
                            
                            if response_request.awaiting_response == False:
                                
                                delaysequence = "wait"
                                timeinms = millis()
                                
                                if len(dictionary_practice_trials) == 18 - n_angles_practice:
                                    sequence = "starting main exp"
                                    print("The time of the practice trials was " + str(millis()))
                                    
                
                
                
                
                
                
##------PRE-ADAPTATION                   
                
        if sequence == "starting main exp":
            
            if keyPressed:
                if key == ENTER:
                    sequence = "Pre-Adaptation"
                    delaysequence = "wait"
                    timeinms = millis()
            else:
                txt.pre_adaptation_trials_instructions_display()
            
        if sequence == "Pre-Adaptation":
            
            fixation_dot.refixate(trial_fixation)
            fixation_dot.display()
        
            if delaysequence == "wait":
            
                if millis() - timeinms < 1500:
                    fixation_dot.refixate(trial_fixation)
                    fixation_dot.display()
                else:
                    delaysequence = 0
                    repositioned = False
            
            else:
        
                if repositioned == False:
                    
                    #print("The number of trials left is " + str(len(dictionary_trials)) + ".")
                    
                    number_of_trial = random.choice(list(dictionary_trials.keys()))
                    dict_of_trial = dictionary_trials.get(number_of_trial)
                    dictionary_trials.pop(number_of_trial)
        
                    overlap = dict_of_trial["overlap"]
                    location = dict_of_trial["location"]
                    
                    #print("The overlap will be " + str(overlap) + ".")
                    #print("Stimuli will be displayed on the " + location + ".")
                        
                    Collision.reposition(fixation_dot.xpos, location, fixation_dot.ypos, random.choice(angles_pre_adaptation), overlap, 1)
                    angles_pre_adaptation.remove(Collision.angle)
                    
                    repositioned = True
                    
                else:
                        
                    if repositioned == True and response_request.awaiting_response == False:

                        Collision.single_iteration(speed)
                        
                        if Collision.iterations == 0:
                            
                            response_request.awaiting_response = True 
                    
                    else:
                                                    
                        if response_request.awaiting_response == True:
                            
                            if Collision.sfrl == trial_fixation:
                                response_request.get_response_test(Collision.overlap, "retinotopic", fixation_dot.xpos, fixation_dot.ypos)
                            else:
                                response_request.get_response_test(Collision.overlap, "spatiotopic", fixation_dot.xpos, fixation_dot.ypos)
                                
                            if response_request.awaiting_response == False:
                                                        
                                #print("Trials remaining in the sequence: " + str(len(angles_pre_adaptation)))
                            
                                delaysequence = "wait"
                                timeinms = millis()
                                
                                if len(angles_pre_adaptation) == 0 and response_request.awaiting_response == False:
                                    sequence = "starting adaptation"
                                    fixation_dot.require_refixation = True
                                    repositioned = False
                                    
                                    print("The time of the pre-adaptation trials was " + str(millis()))
                            
                            
                            
                            
                            
                                
##------ADAPTATION                                
                                
        if sequence == "starting adaptation":
            
            if keyPressed:
                if key == ENTER:
                    sequence = "Adaptation"
                    
                    delaysequence = "intermediate-fixation"
                    timeinms = millis()
                    
            else:
                txt.adaptation_instructions_display()
                        
        if sequence == "Adaptation":
            
            if delaysequence == "intermediate-fixation":
                
                if fixation_dot.require_refixation == True:
                    fixation_dot.move_fixation(adaptation_fixation)
                    fixation_dot.display()
                else:
                    fixation_dot.display()
                    
                    delaysequence = "wait"
                    timeinms = millis()
                    
            else:
                 
                fixation_dot.refixate(adaptation_fixation)
                fixation_dot.display() 
                 
                if delaysequence == "wait":
                
                    if millis() - timeinms < 1500:
                        fixation_dot.refixate(adaptation_fixation)
                        fixation_dot.display()
                    else:
                        delaysequence = 0
                else:
                    
                    if repositioned == False and delaysequence != "adaptation":
                        Collision.reposition(fixation_dot.xpos, "override; adaptation", fixation_dot.ypos, random.choice(angles_adaptation), 0, 1)
                        angles_adaptation.remove(Collision.angle)
                        
                        delaysequence = "adaptation"
                        timeinms = millis()
                        
                    if repositioned == False and delaysequence == "adaptation":
                        if millis() - timeinms < adaptation_sequence_intertrial_delay:
                            background(0)
                            fixation_dot.display()
                        else:
                            repositioned = True
                            delaysequence = 0
                        
                    if repositioned == True:
                        
                        Collision.single_iteration(speed)
                        
                        if Collision.iterations == 0:
                            
                            if len(angles_adaptation) == 0:

                                sequence = "starting post-adaptation"
                                fixation_dot.require_refixation = True
                                repositioned = False
                                
                                print("The time of the adaptation trials was " + str(millis()))
                            else:
                                repositioned = False
                                #print("Stimuli remaining in the sequence: " + str(len(angles_adaptation)))
                                
                                #KURZER DELAY HERE
                                                            
                                                            


##------POST-ADAPTATION                               
                            
        if sequence == "starting post-adaptation":
            
            if keyPressed:
                if key == ENTER:
                    sequence = "Post-Adaptation"

                    delaysequence = "intermediate-fixation"
                    timeinms = millis()
            else:
                txt.post_adaptation_instructions_display()
        
        if sequence == "Post-Adaptation":

            if delaysequence == "intermediate-fixation":
                if fixation_dot.require_refixation == True:                
                    fixation_dot.move_fixation(trial_fixation)
                    fixation_dot.display()
                else:
                    fixation_dot.display()
                    
                    delaysequence = "wait"
                    timeinms = millis()
            
            else:
                fixation_dot.refixate(trial_fixation)
                fixation_dot.display()

                if delaysequence == "wait":
                    
                    if millis() - timeinms < 1500:
                        fixation_dot.refixate(trial_fixation)
                        fixation_dot.display()
                    else:
                        delaysequence = 0
                        repositioned = False
                
                else:

                    if repositioned == False:
                        
                        #print("The number of trials left is " + str(len(dictionary_trials2)) + ".")
                        
                        number_of_trial = random.choice(list(dictionary_trials2.keys()))
                        dict_of_trial = dictionary_trials2.get(number_of_trial)
                        dictionary_trials2.pop(number_of_trial)
            
                        overlap = dict_of_trial["overlap"]
                        location = dict_of_trial["location"]
                        
                        #print("The overlap will be " + str(overlap) + ".")
                        #print("Stimuli will be displayed on the " + location + ".")
                        
                        Collision.reposition(fixation_dot.xpos, location, fixation_dot.ypos, random.choice(angles_post_adaptation), overlap, 1)
                        angles_post_adaptation.remove(Collision.angle)
                        
                        repositioned = True
                    
                    else:
                        
                        if repositioned == True and response_request.awaiting_response == False:

                            Collision.single_iteration(speed)
                            
                            if Collision.iterations == 0:
                                
                                response_request.awaiting_response = True
                                    
                        else:
                            
                            if response_request.awaiting_response == True:
                                
                                if Collision.sfrl == trial_fixation:
                                    response_request.get_response_test(Collision.overlap, "retinotopic", fixation_dot.xpos, fixation_dot.ypos)
                                else:
                                    response_request.get_response_test(Collision.overlap, "spatiotopic", fixation_dot.xpos, fixation_dot.ypos)
                                    
                                if response_request.awaiting_response == False:
                                    
                                    #print("Trials remaining in the sequence " + str(len(angles_post_adaptation)))
                                    
                                    if len(angles_post_adaptation) == 0:
                                        sequence = "save responses"
                                        print("The time of the post-adaptation trials was " + str(millis()))
                                    else:
                                        repositioned = False
                                        
                                        fixation_dot.require_refixation = True
                                    
                                        delaysequence = "intermediate-fixation top-up"
                                        timeinms = millis()
                                        
                                        sequence = "top-up"
                                        

            
        if sequence == "top-up":
            
            if delaysequence == "intermediate-fixation top-up":
                
                if fixation_dot.require_refixation == True:
                    fixation_dot.move_fixation(adaptation_fixation)
                    fixation_dot.display()
                else:
                    fixation_dot.display()
                
                    delaysequence = "wait top-up"
                    timeinms = millis()
            else:
                
                fixation_dot.display()
                
                if delaysequence == "wait top-up":
                    
                    if millis() - timeinms < 1500:
                        fixation_dot.refixate(adaptation_fixation)
                        fixation_dot.display()
                    else:
                        delaysequence = 0
                        
                else:
                    if repositioned == False and delaysequence != "adaptation":
            
                        Collision.reposition(fixation_dot.xpos, "override; adaptation", fixation_dot.ypos, random.choice(top_up_angles), 0, 1)
                        top_up_angles.remove(Collision.angle)
                        
                        delaysequence = "adaptation"
                        timeinms = millis()
                        
                    if repositioned == False and delaysequence == "adaptation":
                        if millis() - timeinms < adaptation_sequence_intertrial_delay:
                            background(0)
                            fixation_dot.display()
                        else:
                            repositioned = True
                            delaysequence = 0
                        
                    if repositioned == True:
                        if repositioned == True:
                            
                            Collision.single_iteration(speed)
                            
                            if Collision.iterations == 0:
                                
                                if count_for_top_up == 1:
                                    
                                    delaysequence = "intermediate-fixation"
                                    timeinms = millis()
                
                                    fixation_dot.require_refixation = True
                                    repositioned = False
                                    
                                    count_for_top_up = n_angles_top_up
                                    
                                    sequence = "Post-Adaptation"
                                    
                                else:
                                    count_for_top_up = count_for_top_up - 1
                                    
                                    repositioned = False
                    
                        
                        
        
        
        
        
##------DEBRIEF   
        
        if sequence == "save responses":
            
            file = open("results_main.csv", "a")
            
            for trial in range(len(response_request.response_dictionary)):
                file.write("".join(response_request.response_dictionary[trial]) + ",")
            
            file.write("\n")            
            
            file.close()
            
            
            file = open("results_practice.csv", "a")
            
            file.write("launch " + str(response_request.response_dictionary_practice["LAUNCH"]) + "," + "pass " + str(response_request.response_dictionary_practice["PASS"]))
            
            file.write("\n")
            
            file.close()
            
            
            file = open("results_instructions.csv", "a")
            
            file.write("launch " + str(example_counter["LAUNCH"]) + "," + "pass " + str(example_counter["PASS"]))
            
            file.write("\n")
            
            file.close()
            
            
            for trial in range(len(response_request.response_dictionary)):
                print("".join(response_request.response_dictionary[trial]) + ",")

            print("launch " + str(response_request.response_dictionary_practice["LAUNCH"]) + "," + "pass " + str(response_request.response_dictionary_practice["PASS"]))

            print("launch " + str(example_counter["LAUNCH"]) + "," + "pass " + str(example_counter["PASS"]))
            
            
            sequence = "Debrief"
            
            delaysequence = "pause"
            timeinms = millis()
            print("The total time was " + str(millis()))
        
        if sequence == "Debrief":
            
            if delaysequence == "pause":
                
                if millis() - timeinms < 1000:
                    background(0)
                else:
                    txt.debrief_message_display()

            

        
##------DEVELOPMENT FEATURES       

    if show_FPS == True:
        fill(255)
        textSize(25)
        text(frameRate, 0, 20)

    if check_display_circularity == True:
        for numbers in xrange(360):
            Collision.reposition(WindowX, WindowY, numbers, 5)
            Collision.display()
    
    if display_grid == True:
        rectMode(CENTER)
        rect(Collision.StartX, Collision.StartY, 4, 4)
        rect(Collision.EndX, Collision.EndY, 4, 4)
        rect(Collision.CenterX, Collision.CenterY, 4, 4)
        line(Collision.StartX, Collision.StartY, Collision.EndX, Collision.EndY)
        
    if display_visualdegree == True:
        rectMode(CENTER)
        rect(WindowX/2, WindowY/2, 4, 4)
        rect(WindowX/2 + visualdegree, WindowY/2, 4, 4)
        rect(WindowX/2 - visualdegree, WindowY/2, 4, 4)
        
    if check_animation_time == True:
        
        if keyPressed:
            if key == "c":
                delaysequence = "run"
      
        if delaysequence == "run":
              
            if repositioned == False:
                    
                    fixation_dot.refixate(adaptation_fixation)
                    
                    Collision.reposition(fixation_dot.xpos, "override; adaptation", fixation_dot.ypos, 45, 0, 1)
                    
                    timeinms = millis()
                    
                    repositioned = True
                    
            else:
                if repositioned == True:

                    Collision.single_iteration(speed)
                    
                    if Collision.condition == 3:
                        print(millis() - timeinms)
                    
                        repositioned = False
                        
                        delaysequence = 0
        
