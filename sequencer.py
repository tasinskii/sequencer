import threading
import sounddevice as sd
import soundfile as sf
import numpy as np

SAMPLERATE = 44100

class Sequence:
    def __init__(self, name):
        self.name = name
        self.bpm = 100
        self.length = 16
        self.samples = []
        self.patterns = []
        self.wave = []
        
    def load_sample(self):
        print("--------------")
        while True:         
            chosen_sample = input("Drag sample to add to sequence: ")
            self.samples.append(chosen_sample.strip())
            default_pattern = []
            for i in range(0, self.length):
                default_pattern.append(0)
            self.patterns.append(default_pattern)
            print("--- Sample " + chosen_sample + " Added ---")
            ask = input("Would you like to add another sample (Y/n)? ")
            if ask != 'Y':
                print("--------------")
                print('\n')
                break;
    
    def edit_pattern(self):
        print("--------------")
        done = False
        while done == False:         
            print(self.samples)
            sample_id = input("Input number corresponding to sample pattern to be edited: ")
            sample_id = int(sample_id)
            sample_pattern = self.patterns[sample_id]
            while done == False:
                print("--- Pattern for sample: " + self.samples[sample_id] + " ---" + "\n")
                key=[]
                for i in range(0, len(sample_pattern)): #pattern beat ids
                    key.append(i)  
                print("Editing pattern: ")
                print("--------------")
                print(key)
                print(sample_pattern)
                while True:
                    edited_beat = input("Select number of which beat to edit: ")
                    choice = input("Choose value to add to beat(1,0): ")
                    sample_pattern[int(edited_beat)] = choice
                    print(sample_pattern)
                    ask = input("Edit another beat (Y/n)? ")
                    if ask != 'Y':
                        print("--------------")
                        print('\n')
                        done = True
                        break;

    def make_sequence(self, pattern, sample):
        ratio = (60.0/float(self.bpm)) #bpm/60 => length of one beat
        length = int(SAMPLERATE*ratio)
        onebar = np.zeros(length*4)
        ind = 0
        for i in range(0, self.length):#16 beats
            if pattern[i] == '1':
                onebar = np.concatenate((onebar[:ind], sample, onebar[(ind+np.size(sample)):]))
                ind += int(length/4) #advance by 16th of a beat
            else:
                ind += int(length/4)
        return onebar
   
        
        
    def build_sequence(self):
        bars = []
        for i in range(0, len(self.samples)):
            sample, sr = sf.read(self.samples[i])
            sample_bar = self.make_sequence(self.patterns[i], sample)
            bars.append(sample_bar)
        result = sum(bars)
        self.wave = result
        return result
    
s = Sequence(name='1')
def play_sequence():
    print("Control + Z to exit sequencer, repeating sequence 16 times")
    result = np.tile(s.wave, 16)
    sd.play(result, SAMPLERATE)
    #sd.play(s.wave, SAMPLERATE)


###### main loop

while True:
    print("-------------------------")
    print("Epic 16 beat Sequencer")
    
    choice = input('''
    [1] -> load samples, [2] -> edit pattern, [3] -> play sequence
                   ''')  
    if choice == '1':
        s.load_sample()
    elif choice == '2':
        s.edit_pattern()
    elif choice == '3':
        res = s.build_sequence()
        t = threading.Thread(target=play_sequence)
        t.start()
        
        
        
