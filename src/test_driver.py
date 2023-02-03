import viginere, otp, enigma, tools

p = "Standing on top of the great minaret of Istiqlal was a man with a violin"


"""
# 1. Viginere
k = "nijika"
cv = viginere.encrypt_v(p, k)
print(f"v_e: {cv}")
print(f"v_e2: {tools.group_to_fives(cv)}")
print(f"v_d: {viginere.decrypt_v(cv, k)}")


# 2. OTP
tools.save_text_to_file(otp.generate_otp_key(), "otp_key")
otp_key = tools.read_file("otp_key")
co = otp.encrypt_otp(p, otp_key)
print(f"o_e: {co}")
print(f"o_d: {otp.decrypt_otp(co, otp_key)}")

"""

# 3. Enigma
machine1 = enigma.M3Machine("II", "IV", "III", "B")
machine1.set_rotors("E", "N", "E")
ce = machine1.process_text(p)
print(f"e_e: {ce}")
machine1.set_rotors("E", "N", "E")
print(f"e_d: {machine1.process_text(ce)}")