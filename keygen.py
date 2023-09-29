import random, galois

if __name__ == '__main__':
    print("Enter the parameters")
    n = int(input("Codeword length, n: "))
    t = int(input("Error correction capacity, t: "))
    m = int(input("Field degree, m: "))
    
    order = 2**m
    GF = galois.GF(order)
    print("\nPrimitive polynomial:", GF.irreducible_poly)

    # Generate random monic irreducible polynomial g(z) over F_2^m of degree 't':
    irr_poly = galois.irreducible_poly(order, t)
    print("\ng(x):", irr_poly)

    # Create a random set with distinct elements of the field
    L = random.sample(range(order), n)
    print("\nSupport, L:", L)

    # Compute H, here t x n
    H = [[0] * n for _ in range(t)]
    for i in range(t):
        for j in range(n):
            h = GF(L[j])
            for k in range(i):
                h *= GF(L[j])
            H[i][j] = int(h / irr_poly(L[j]))
    
    print('\nH:')
    for item in H:
        print(item)

    # Replace each element of H with vectors of (F_2)^m
    for i in range(t):
        for j in range(n):
            H[i][j] = [int(x) for x in list(format(H[i][j], f'0{m}b'))]

    # Reshape H to proper form, dimensions n x mt
    I = []
    for item in zip(*H):
        I.append(item[0] + item[1])
 
    H = [[0] * n for _ in range (m * t)]
    for i in range(n):
        for j in range(m * t):
            H[j][i] = I[i][j]

    print('\nElements converted to binary representation, H:')
    H = GF(H)
    print(H)

    # Perform Gaussian elimination
    H = H.row_reduce(eye = 'left')
    print('\nAfter RREF, H:')
    print(H)

    # Extract the public key T from H = (I_mt | T_(mt x n - mt))
    T = [[0] * (n - m * t) for _ in range(m * t)]
    for i in range(m * t):
        for j in range(n - m * t):
            T[i][j] = H[i][j + m * t]
    
    print('\nPublic Key, T:')
    T = GF(T)
    print(T)

    # Generate uniform random n length string
    s = ''.join([str(random.randrange(2)) for _ in range(n)])
    print('\ns:', s)
    