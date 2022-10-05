import numpy as np
import matplotlib.pyplot as plt
inf = "Infinity"


# ### Making some helper functions


def Mod(x,p):
    return x%p


def extended_euclid(m,n):
        if n == 0:
            return (m,1,0)
        else:
            q = m // n
            r = m % n
            (g,u,v) = extended_euclid(n,r)
        return (g,v,u-q*v)

def inv(s,p):
        (g,x,y) = extended_euclid(s,p)
        if (g != 1):
            return (0) 
        else:
            return(x % p)

# checking the inverse
Mod(Mod(7,13)*inv(7,13),13)


# ### Creating a class for Elliptic Curves

class ECC:
    

    def __init__(self,a,b,p):
        self.a = a
        self.b = b
        self.p = p
        self.points = []
        self.Points()


    def Points(self):
        self.points.append(inf)
        for x in range(self.p):
            for y in range(self.p):

                if Mod(pow(y,2) - (pow(x,3)+(self.a*x)+self.b), self.p) == 0:
                    if (x,y) not in self.points:
                        self.points.append((x,y))
        return self.points


    def slope(self, A, B):
        x1,y1 = A
        x2,y2 = B
        gamma = inf
        
        if A == B:
            gamma = (3*pow(x1,2) + self.a) * inv(2*y1, self.p)

        else:
            gamma = (y2-y1)*inv(x2-x1, self.p)

        if x1 == x2 and y1 != y2:
            gamma = inf
        
        return gamma


    def add(self, A, B):
        if A == inf:
            return B
        elif B == inf:
            return A
        else:
            x1,y1 = A
            x2,y2 = B
            S = self.slope(A,B)
            if S == inf:
                return inf
            else:
                x3 = pow(S,2) - x1 - x2
                y3 = S*(x1-x3) - y1

                x3 = Mod(x3,self.p)
                y3 = Mod(y3,self.p)

                return (x3,y3)


    def pointDoubler(self, A):
        if A == inf:
            return inf
        else:
            x1,y1 = A
            x2,y2 = A
            S = (3*pow(x1,2) + self.a) * inv(2*y1, self.p)
            if S == inf:
                return inf
            else:
                x3 = pow(S,2) - x1 - x2
                y3 = S*(x1-x3) - y1

                x3 = Mod(x3,self.p)
                y3 = Mod(y3,self.p)

                return (x3,y3)

    def binary_mode(self, k):
        K = bin(k)[2:]
        res =[int(x) for x in K]
        return res[::-1]
    
    def power_check(self, k):
        V = []
        K = self.binary_mode(k)
        for i in range(0,len(K)):
            if K[i] == 1:
                V.append(i)
        return V

    def power_mult(self,P,k):
        # P 
        while k >0:
            P = self.pointDoubler(P)
            k -= 1
        return P

    def super_mult(self,P,k):
        product = inf
        if k == 0:
            return (0,0)
        else:
            K = self.power_check(k)
            for i in K:
                X = self.power_mult(P,i)
                product = self.add(X,product)
        return product
