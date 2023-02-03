import time

class Responses(object):
    
    def __init__(self, WindowX, WindowY):
        
        self.WindowX = WindowX
        self.WindowY = WindowY
        
        self.awaiting_response = False
        self.skip_response = False
        
        self.response = "This is just a test. The response was "
        
        self.response_dictionary = []
        
        self.response_dictionary_practice = {"LAUNCH": 0, "PASS": 0}
        
        self.trial_number = 1
        
    def display(self, locationX, locationY):
        
        stroke("#32cd32")
        fill("#32cd32")
        rectMode(CENTER)
        rect(locationX, locationY, 2*(10) + 5, (10)/2)
        rect(locationX, locationY, (10)/2, 2*(10) + 5)
        
        ##Text Version Below
        
        #fill(255)
        
        #textAlign(LEFT)
        
        #textSize(50)
        #big_text = "Please respond."
        #text(big_text, locationX - textWidth(big_text)/2, locationY + 100)
        
        #textSize(20)
        #small_textD = "Press D for a launch."
        #text(small_textD, locationX*0.75 - textWidth(small_textD)/2, locationY + 150)
            
        #textSize(20)
        #small_textK = "Press K for a pass."
        #text(small_textK, locationX*1.25 - textWidth(small_textK)/2, locationY + 150)
        
        #make another display that? Probalby not as that conflicts with training.
            
        
    def get_response(self, locationX, locationY):
        self.display(locationX, locationY)
        if keyPressed:
            if key == "d":
                self.response = self.response + "D "
                print(self.response)
                
                self.awaiting_response = False
                
            if key == "k":
                self.response = self.response + "K "
                print(self.response)
                
                self.awaiting_response = False
                
                
    def get_response_test(self, degree_of_overlap, trial_type, locationX, locationY):
        self.display(locationX, locationY)
        self.awaiting_response = not self.skip_response
        if keyPressed:
            
            if key == "d":
                response = str(trial_type) + " trial" + "," + str(degree_of_overlap*100) + "%" + " overlap" + ","
                self.response_dictionary.append([response + "rated as a launch"])
                self.trial_number = self.trial_number + 1
                #print(self.response_dictionary)
                
                self.awaiting_response = False
                
            if key == "k":
                response = str(trial_type) + " trial" + "," + str(degree_of_overlap*100) + "%" + " overlap" + ","
                self.response_dictionary.append([response + "rated as a pass"])
                self.trial_number = self.trial_number + 1
                #print(self.response_dictionary)
                
                self.awaiting_response = False
                
                
    def get_response_practice(self, locationX, locationY):
        self.display(locationX, locationY)
        self.awaiting_response = not self.skip_response
        if keyPressed:
            
            if key == "d":
                self.response_dictionary_practice["LAUNCH"] = self.response_dictionary_practice["LAUNCH"] + 1
                self.awaiting_response = False
                
                
            if key == "k":
                self.response_dictionary_practice["PASS"] = self.response_dictionary_practice["PASS"] + 1
                
                self.awaiting_response = False
        
        
