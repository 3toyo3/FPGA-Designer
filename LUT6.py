class LUT6:
    def __init__(self,name,inputs,output):

        if len(inputs) <=6:
            self.name= name
            self.inputs=inputs
            self.output=output
        else:
            print("Error: trying to assign more than 6 inputs to 6-input LUT")

