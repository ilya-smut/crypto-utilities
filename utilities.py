def a_mod_p(a: int, p: int):
    '''
    Returns a modulo p
    '''
    if p <= 0:
        return None

    return a % p

def get_gcd(x: int, y: int):
    '''
    Basic Euclidean Algorithm
    '''
    a = x
    b = y
    r = a % b
    if r == 0:
        return b
    return get_gcd(b, r)


def get_extended_euclid(a: int, b: int):
    '''
    Extended Euclid
    '''
    if a == 0:
        return b, 0, 1
    
    gcd, x1, y1 = get_extended_euclid(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def get_mod_inverse_euclid(a: int, p: int, multiplication=True):
    '''
    returns modular multiplicative inverse of a in (Z/pZ)* if multiplication=True.
    Else returns additive inverse
    '''
    if not multiplication:
        return -1 * a_mod_p(a, p)
    a = a_mod_p(a,p)
    gcd, x, y = get_extended_euclid(a, p)
    if gcd != 1:
        return None # No inverse if not coprime to modulo
    return a_mod_p(x, p)


def get_binary_exp_factors(n: int) -> list[int]:
    bits = []
    while n > 0:
        bits.append(n & 1)
        n >>= 1
    return bits[::-1]


def fast_powering(g: int, x: int, p: int):
    return pow(g, x, p)


def get_mod_inverse_fermat(a: int, p: int, multiplication=True):
    if not multiplication:
        return -1 * a_mod_p(a, p)
    a = a_mod_p(a,p)
    if get_gcd(a,p) != 1:
        return None
    return a_mod_p(fast_powering(a, p-2, p), p)