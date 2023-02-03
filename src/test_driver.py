import viginere, otp, tools

tools.save_text_to_file(otp.generate_otp_key(), "otp_key")