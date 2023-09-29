import numpy as np
import hashlib

GFBITS = 12  # M
SYS_T = 64   # T
SYS_N = 3488 # N
IRR_BYTES = 128
COND_BYTES = 64
SYS_NBYTES = SYS_N // 8
GFMASK = 0xFFF
PK_NROWS = 112
PK_ROW_BYTES = 32
GF_BYTES = 2
K = SYS_N - (SYS_T * GFBITS)

# generate uniform random vector e ∈ F_n^2 with Hamming weight t
def gen_e():
    num_ones = SYS_T
    num_zeroes = SYS_N - SYS_T
    e = np.array([0] * num_zeroes + [1] * num_ones)
    np.random.shuffle(e)
    return e

# taking a mock value of the public key T
def gen_mock_T():
    row, col = K, GFBITS * SYS_T
    T = np.random.randint(2, size=(row, col))
    return T

# generate the H matrix from the T public key
def gen_H():
    mt = GFBITS * SYS_T
    I = np.identity(mt)
    T = gen_mock_T()
    H = np.concatenate((I, T))
    return H

# get the C0 part of the ciphertext
def compute_c0(H, e):
    return np.dot(e, H)

def compute_c1(e):
    shake = hashlib.shake_256()
    e_str = ''.join(str(bit) for bit in e) 
    shake.update(e_str.encode())
    return shake.hexdigest(256)

def gen_session_key(c0, c1, e):
    c0_str = [str(int(x)) for x in c0]
    concat_c0 = ''.join(c0_str)

    e_str = ''.join(str(bit) for bit in e)
    shake = hashlib.shake_256()

    c = concat_c0 + c1
    shake.update(concat_c0.encode())
    shake.update(e_str.encode())
    
    return shake.hexdigest(256)


def encrypt():
    H = gen_H()
    e = gen_e()
    
    c0 = compute_c0(H, e)
    c1 = compute_c1(e)
    c0_str = [str(int(x)) for x in c0]
    concat_c0 = ''.join(c0_str)

    C = concat_c0 + c1 # ciphertext
    K = gen_session_key(c0, c1, e) # session key
    return (C, K)

if __name__ == '__main__':
    c, k = encrypt()
    print(f"Cipher Text: {c}")
    print("\n#######################################################\n")
    print(f"Session Key: {k}")








