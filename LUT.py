class LUT:
    def __init__(self,name,inputs,output):

        if len(inputs) <=4:
            self.name= name
            self.inputs=inputs
            self.output=output
        else:
            print("Error: trying to assign more than 4 inputs to 4-input LUT")




