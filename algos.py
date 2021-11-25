import numpy as np

def maximum_likelihood(gateways):
    ''' 
    gateways: [(x1, y1, r1), (x2, y2, r2), ...]
    returns: (x, y)
    '''

    x_n = gateways[len(gateways) - 1][0]
    y_n = gateways[len(gateways) - 1][1]
    r_n = gateways[len(gateways) - 1][2]

    A = np.zeros((len(gateways) - 1, 2))
    b = np.zeros((len(gateways) - 1, 1))
    for i, gateway in enumerate(gateways[:-1]):
        x_i = gateway[0]
        y_i = gateway[1]
        r_i = gateway[2]
        
        A[i] = [x_n - x_i, y_n - y_i]
        b[i] = [-(x_i**2) - (y_i**2) + (r_i)**2 + (x_n)**2 + (y_n)**2 - (r_n)**2]

    print(A)
    print(b)
    return np.linalg.lstsq(A, b)[0]

def min_max(gateways):
    '''
    gateways: [(x1, y1, r1), (x2, y2, r2), ...]
    returns: (x, y)
    '''
    l = -np.inf
    r = np.inf
    t = np.inf
    b = -np.inf
    for gateway in gateways:
        lg = gateway[0] + gateway[2] / 2
        rg = gateway[0] - gateway[2] / 2
        tg = gateway[1] - gateway[2] / 2
        bg = gateway[1] + gateway[2] / 2

        l = max(l, lg)
        r = min(l, rg)
        t = min(l, tg)
        b = max(l, bg)

    return ( (l+r)/2, (t+b)/2 )

print(maximum_likelihood([[2, 0, 2], [4, 4, 2], [10, 0, 5]]))
print(min_max([[2, 0, 2], [4, 4, 2], [10, 0, 5]]))