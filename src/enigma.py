# M3 Enigma (Wehrmacht version)
# Plugboards are not modeled due to time constraint
import tools

# Rotors

class Rotor:
    def __init__(self, rot_id):
        # Create a Rotor object, consisting of an
        # entry ring and an encrypt ring.
        # Head is defined as the first char in ring
        self.rot_id = rot_id
        self.entry_ring = get_rot_conf("entry")
        self.encrypt_ring = get_rot_conf(rot_id)
    

    def get_entry_ring(self):
        return self.entry_ring

    
    def get_encrypt_ring(self):
        return self.encrypt_ring


    def is_time_for_turnover(self):
    # If the encrypt rotor moves to this chars, it 
    # means it's true for next rotor to move
        dict_notches = {
            "I"   : "R",
            "II"  : "F",
            "III" : "W",
            "IV"  : "K",
            "V"   : "A"
        }
        return (self.get_entry_ring()[0] == dict_notches[self.rot_id])


    def rotate(self):
        # Rotate ABC..XYZ to ZAB..WXY
        # Entry side
        entry_ring_L = self.entry_ring[0:25]
        entry_ring_R = self.entry_ring[25:]
        self.entry_ring = (entry_ring_R + entry_ring_L)
        # Encrypt side
        encrypt_ring_L = self.encrypt_ring[0:25]
        encrypt_ring_R = self.encrypt_ring[25:]
        self.encrypt_ring = (encrypt_ring_R + encrypt_ring_L)
# End of Rotor class

# Tools 
def get_rot_conf(rot_id):
    dict_rot_id = {
        "entry" : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
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
            while self.rotors[i].get_entry_ring()[0] != self.positions[i]:
                self.rotors[i].rotate()
        self.is_rotor_set = True
    

    def process_char(self, reflector, char):
        # Used for both encrypt and decrypt
        for i in range(0, 3):
            char = get_pair(self.rotors[i].get_entry_ring(), self.rotors[i].get_encrypt_ring(), char)
        char = get_pair(self.rotors[2].get_entry_ring(), reflector, char)
        for i in range(2, -1, -1):
            char = get_pair(self.rotors[i].get_encrypt_ring(), self.rotors[i].get_entry_ring(), char)

        self.rotors[0].rotate()
        if self.rotors[0].is_time_for_turnover():
            self.rotors[1].rotate()
            if self.rotors[1].is_time_for_turnover():
                self.rotors[2].rotate

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


