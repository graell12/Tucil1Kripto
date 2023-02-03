# M3 Enigma (Wehrmacht version)
# Plugboards are not modeled due to time constraint
import tools

# Rotors

class Rotor:
    def __init__(self, rot_id):
        # Create a Rotor object, consisting of a
        # front ring and an back ring.
        # Head is defined as the first char in front ring
        self.rot_id = rot_id
        self.front_ring = get_rot_conf("front")
        self.back_ring = get_rot_conf(rot_id)
    

    def get_front_ring(self):
        return self.front_ring

    
    def get_back_ring(self):
        return self.back_ring


    def is_time_for_turnover(self):
    # If the back rotor moves to this chars, it 
    # means it's true for next rotor to move
        dict_notches = {
            "I"   : "R",
            "II"  : "F",
            "III" : "W",
            "IV"  : "K",
            "V"   : "A"
        }
        return (self.get_front_ring()[0] == dict_notches[self.rot_id])


    def rotate(self):
        # Rotate ABC..XYZ to B..YZA
        # Front side
        front_ring_L = self.front_ring[0:1]
        front_ring_R = self.front_ring[1:]
        self.front_ring = (front_ring_R + front_ring_L)
        # Back side
        back_ring_L = self.back_ring[0:1]
        back_ring_R = self.back_ring[1:]
        self.back_ring = (back_ring_R + back_ring_L)
# End of Rotor class

# Tools 
def get_rot_conf(rot_id):
    dict_rot_id = {
        "front" : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "I"     : "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "II"    : "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "III"   : "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "IV"    : "ESOVPZJAYQUIRHXLNFTGKDCMWB",
        "V"     : "VZBRGITYUPSDNHLXAWMJQOFECK"
    }
    return dict_rot_id[rot_id]


def get_ref_conf(ref_id):
    dict_ref_id = {
        "contacts" : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",            
        "B"        : "YRUHQSLDPXNGOKMIEBFZCWVJAT",
        "C"        : "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    }
    return dict_ref_id[ref_id]

def get_pair(init_ring, dest_ring, init_head):
    i = 0
    while init_ring[i] != init_head:
        i += 1
    return dest_ring[i]


# M3 Machine
class M3Machine:
    def __init__(self, rot_id1, rot_id2, rot_id3, ref_id):
        self.rotors = [Rotor(rot_id1), Rotor(rot_id2), Rotor(rot_id3)]
        self.reflector = get_ref_conf(ref_id) 
        self.positions = ["A", "A", "A"]
        self.is_rotor_set = False
    

    def set_rotors(self, pos1, pos2, pos3):
        self.positions = [pos1, pos2, pos3]
        for i in range(0,3):
            while self.rotors[i].get_front_ring()[0] != self.positions[i]:
                self.rotors[i].rotate()
        self.is_rotor_set = True
    

    def process_char(self, reflector, char):
        # Used for both encrypt and decrypt

        # 1. Key is pressed. Check for turnover
        self.rotors[2].rotate()
        if self.rotors[2].is_time_for_turnover():
            self.rotors[1].rotate()
            if self.rotors[1].is_time_for_turnover():
                self.rotors[0].rotate

        # 2. Digital signal enters I/O, apparently from rotor 3 to rotor 1
        for i in range(2, -1, -1):
            char = get_pair(self.rotors[i].get_front_ring(), self.rotors[i].get_back_ring(), char)

        # 3. Digital signal is reflected by reflector
        char = get_pair(get_rot_conf("front"), reflector, char)

        # 4. Digital signal is returned to I/O
        for i in range(0, 3):
            char = get_pair(self.rotors[i].get_back_ring(), self.rotors[i].get_front_ring(), char)

        return char
    

    def process_text(self, text):
        # Used for both encrypt and decrypt
        text = tools.cleanse(text)
        if self.is_rotor_set:
            self.set_rotors(self.positions[0], self.positions[1], self.positions[2])
            newtext = ""
            i = 0
            for i in range(0, len(text)):
                newtext += self.process_char(self.reflector, text[i])
            self.is_rotor_set = False
            return newtext
        else:
            return "ACHTUNG: ROTOR RINGS CONFIG NOT SET!"


