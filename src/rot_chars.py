# Rotate a character

def encrypt_rot_c(p, k):
    # Encrypt a character by rotation
    n_p = ord(p.upper()) - 65
    n_k = ord(k.upper()) - 65
    n_c = ((n_p + n_k) % 26) + 65
    c = chr(n_c)
    return c


def decrypt_rot_c(c, k):
    # Decrypt a character by rotation
    n_c = ord(c.upper()) - 65
    n_k = ord(k.upper()) - 65
    n_p = ((n_c - n_k) % 26) + 65
    p = chr(n_p)
    return p