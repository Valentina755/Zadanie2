import numpy as np
import matplotlib.pyplot as plt
import os
import requests
import re
import scipy.special as sc
import matplotlib.ticker as mt

def a(n, x):
    return sc.spherical_jn(n, x) / h(n, x) 

def b(n, x):
    return ((x * sc.spherical_jn(n - 1, x) - n * sc.spherical_jn(n, x))
            / (x * h(n - 1, x) - n * h(n, x)))
    
def h(n, x):
    return sc.spherical_jn(n, x) + 1j * sc.spherical_yn(n, x)

def RCS(D, fmin, fmax):
    c = 3e8
    r = D/2
    f = np.arange(fmin, fmax+1e6, 1e6)
    sigma = []
    for i in f:
        lambda_ = c / i
        k = 2 * np.pi / lambda_
        summa = []
        for n in range(1,110):
            summa.append((-1) ** n * (n + 0.5) * (b(n, k * r) - a(n, k * r)))
        sigma.append((lambda_ ** 2 / np.pi) * abs(sum(summa)) ** 2)
    w = open('results/task_02_4О-506C_CHURSINA_08.txt', 'w')
    print ('f, [МГц]\tsigma, [м^2]\n', file = w)
    for i in range(len(f)):
        print('{0}\t\t{1}\n'.format(f[i] * 1e-6, sigma[i]), file = w)
    w.close()
    plt.plot(f, sigma)
    plt.grid()
    plt.ylabel(r'$\sigma$, [$м^2$]', fontsize = 18)
    plt.xlabel('$f$, [Гц]')
    plt.show()
           
if __name__ == '__main__':
    try: os.mkdir('results')
    except OSError: pass
    r = requests.get('https://jenyay.net/uploads/Student/Modelling/task_02.txt')
    for i in r.text.splitlines():
        if re.match(r'8\.', i): z = i 
    match = list(map(lambda z:float(z), re.findall(r'=(\d+\.?\d*[e-]*\d+)',z)))
    D, fmin, fmax = match[0], match[1], match[2]
    RCS(D, fmin, fmax)
    
    
    

    
