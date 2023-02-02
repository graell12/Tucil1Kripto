from . import viginere, otp, tools

p = "loremipsumdolorsit"
k = "nijika"
c = viginere.encrypt_v(p, k)
print(c)

tools.save_text_to_file(otp.generate_otp_key(), "otp_key")