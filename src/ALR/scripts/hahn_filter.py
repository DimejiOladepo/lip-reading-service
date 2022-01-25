from math import factorial, sqrt, isinf, isnan
from PIL import Image


class HahnFilter:
    def __init__(self, img_dir, alpha=5, beta=5):
        self.a = int((alpha + beta)/2)
        im = Image.open(img_dir)
        im = im.convert('L')
        self.im = im 
        # self.N, self.N_MAX = im.size
        self.N, self.N_MAX = 50, 5
        self.b = int(self.a + self.N)
        self.c = int((beta - alpha)/2)


    def hahn_polynomial_values(self):
        """Algorithm for computing the weighted dual Hahn polynomial values"""
        a = self.a
        b = self.b
        c = self.c
        N = self.N
        N_MAX = self.N_MAX

        i = 0
        w_n_i = list()
        while i <= (N-1):
            n = 2
            w_n = list()
            s = a + i
            w_0 = sqrt(rho(s) * (2*s + 1)/sqrd_norm(0))
            w_1 = [(rho_general(1,s-1) - rho_general(1,s))/(rho(s) * (2*s+1))] * sqrt(p_s * (2 * s + 1)/sqrd_norm(1))
            i += 1
            while n <= (N_MAX-1):
                A = (1/n) * [s * (s+1) - a * b + a * c - b * c - (b-a-c-1) * (2*n-1)+2 * (n-1)**2]
                B = (-1/n) * (a+c+n-1) * (b-a-n+1) * (b-c-n+1)
                D = sqrt(n/((a+c+n)*(b-a-n)*(b-c-n)))
                F = (n*(n-1)/sqrt((a+c+n) * (a+c+n-1) * (b-a-n+1) * (b-a-n) * (b-c-n+1) * (b-c-n)))
                if n == 2:
                    w = (A * w_1) * D + (B * w_0 * F)
                elif n == 3:
                    w = (A * w_n[-1]) * D + (B * w_1 * F)
                elif n > 3:
                    w = (A * w_n[-1]) * D + (B * w_n[-2] * F)
                n += 1
                w_n.append(w)
            w_n_i.append(w_n)


    def hahn_moments(self):
        """Computation of the dual Hahn Moments up to order NMAX"""
        a = self.a
        b = self.b
        c = self.c
        N = self.N
        N_MAX = self.N_MAX

        im = self.im
        # im = im.convert("L")
        px = self.im.load()
        
        w_m, w_n = list(), list()

        # s = t = a

        def hahn_polynomial_m(j,i):
            if j == 0:
                w = (sqrt(rho(i) * (2*i + 1)/sqrd_norm(0)))
                # try:
                #     w = (sqrt(rho(i) * (2*i + 1)/sqrd_norm(0)))
                # except ValueError: w = 1
            elif j == 1:
                try:
                    w = ((rho_general(1,i-1) - rho_general(1,i))/(rho(i) * (2*i+1))) * sqrt(rho(i) * (2 * i + 1)/sqrd_norm(1))
                except ValueError: w = 1
            elif j > 1:
                A = (1/j) * (i * (i+1) - a * b + a * c - b * c - (b-a-c-1) * (2*j-1)+2 * (j-1)**2)
                B = (-1/j) * (a+c+j-1) * (b-a-j+1) * (b-c-j+1)
                D = sqrt(j/((a+c+j)*(b-a-j)*(b-c-j)))
                F = sqrt((j*(j-1)/((a+c+j) * (a+c+j-1) * (b-a-j+1) * (b-a-j) * (b-c-j+1) * (b-c-j))))
                w = (A * w_m[-1] * D) + (B * w_m[-2] * F)
                print(i)
                print(j)
                print(A)
                print(B)
                print(D)
                print(F)
            # if isnan(w):
            #     exit()
            if isinf(w):
                w = 0
            w_m.append(w)
            print('hahn_polynomial_m: ', w)
            return w

        def hahn_polynomial_n(j,i):
            if j == 0:
                try:
                    w = (sqrt(rho(i) * (2*i + 1)/sqrd_norm(0)))
                except ValueError: w = 1
            elif j == 1:
                try:
                    w = ((rho_general(1,i-1) - rho_general(1,i))/(rho(i) * (2*i+1))) * sqrt(rho(i) * (2 * i + 1)/sqrd_norm(1))
                except ValueError: w = 1
            elif j > 1:
                A = (1/j) * (i * (i+1) - a * b + a * c - b * c - (b-a-c-1) * (2*j-1)+2 * (j-1)**2)
                B = (-1/j) * (a+c+j-1) * (b-a-j+1) * (b-c-j+1)
                D = sqrt(j/((a+c+j)*(b-a-j)*(b-c-j)))
                F = sqrt((j*(j-1)/((a+c+j) * (a+c+j-1) * (b-a-j+1) * (b-a-j) * (b-c-j+1) * (b-c-j))))
                w = (A * w_n[-1] * D) + (B * w_n[-2] * F)
                print(i)
                print(j)
                print(A)
                print(B)
                print(D)
                print(F)
            if isinf(w):
                w = 0
            w_n.append(w)
            print('hahn_polynomial_n: ', w)
            return w


        def rho(s):
            """Weighting function p(s)"""
            assert -0.5 < a < b
            assert abs(c) < (1 + a)
            # print(a)
            # print(b)
            # print(c)
            # print(s)
            rho = (factorial(a+s) * factorial(c+s))/(factorial(s-a) * factorial(b-s-1) * factorial(b+s) * factorial(s-c))
            return rho
            # try:
            #     rho = (factorial(a+s) * factorial(c+s))/(factorial(s-a) * factorial(b-s-1) * factorial(b+s) * factorial(s-c))
            #     return rho
            # except ValueError: return 1


        def sigma(s):
            """One classical hahn polynomial solution"""
            sigma = (s-a)*(s+b)*(s-c)
            return sigma
            

        def rho_general(s,n):
            """Generalized weighting function - p_n(s)"""
            k = 1
            right_eqn_sum = list()
            left_eqn = rho(s+n)
            while k <= s:
                right_eqn = sigma(s+k)
                right_eqn_sum.append(right_eqn)
                k += 1
            rho_general = left_eqn * right_eqn
            return rho_general


        def sqrd_norm(n):
            """Squared norm - d_n_^2"""
            sqrd_norm = factorial(a+c+n)/(factorial(n) * factorial(b-a-n-1) * factorial(b-c-n-1))
            # print(sqrd_norm)
            # if int(sqrd_norm) == 0: return 1
            # else: return int(sqrd_norm)
            return sqrd_norm


        moments = list()
        for m in range(N_MAX):
            # w_m.clear() 
            for n in range(N_MAX):
                # w_n.clear()
                sum_1 = 0
                s = a
                while s <= b-1:
                    t = a
                    while t <= b-1:
                        # print("First one ", hahn_polynomial_m(m,s))
                        # print("Second one ", hahn_polynomial_n(n,(a-b+t)))
                        sum_1 = sum_1 + (hahn_polynomial_m(m,s) * hahn_polynomial_n(n,(a-b+t)) * px[s,t]) 
                        t += 1
                    s += 1
                moments.append(sum_1)
        print('moments ', moments)
        return moments 


if(__name__ == '__main__'):
    HahnFilter('data/AVLetters2_imgs/sp1_A1/2.jpg').hahn_moments()
    # HahnFilter('/Users/dimejioladepo/Downloads/20210318-DSC_6265.jpg').hahn_moments()