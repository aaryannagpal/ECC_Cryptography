#!/usr/bin/env python
# coding: utf-8

# # Elliptical Cryptography - Diffe-Hellman

# ### Importing the necessary modules

# In[117]:


from EllipticalCurve import *
import random
import numpy as np
from math import ceil, floor, log
import matplotlib.pyplot as plt


# ## Creating Generator

# ### Ferman Test to check primality

# In[118]:


def checkPrime(a):
    if a==2:
        return True
    i=0
    while i<5:
        p=np.random.randint(2,20)
        if pow(p,a-1,a)!=1:
            return False
        else:
            return True
        i+=1


# ### Generating a Prime Number

# In[119]:


def LargePrime(k):  
    
    b=100*(log(k,2)+1) #number of attempts max
    while b>0:
        n = random.randrange(2**(k-1),2**(k))
        b-=1
        if checkPrime(n) == True:
            return n
    return "Failure in computing"


# ### Creating a prime number $p$

# In[120]:


p = LargePrime(10) #to have a prime number >= 128, which are the same number of characters in the ASCII table, so that infinity does not come
p


# ### Creating an ECC

# In[121]:


def ECC_Variables(k = 10):
    a = random.randint(0,pow(2,k-1))
    b = random.randint(0,pow(2,k-1))
    c = 4*pow(a,3) + 27*pow(b,2)
    if c == 0:
        ECC_Variables()
    else:
        return a,b

X,Y = ECC_Variables()


# ### Declaring $E$

# In[122]:


E = ECC(X,Y,p)


# ### Declaring $G$

# In[123]:


def GenCheck(G):
    n = []
    for i in range(p+1):
        if E.super_mult(G,i) == inf:
            n.append(i)
    if len(n) == 1:
        if n[0] > 0:
            return True
    else:
        return False

def Gen():
    E_g = E.points
    G = random.choice(E_g)
    while GenCheck(G) != True:
        E_g.remove(G)
        G = random.choice(E_g)
    if G == None:
        a = "No Generator Found"
        return a
    return G

G = Gen()
#get checked

##Researched and found that to make a G is actually a very very tough


# In[124]:


#testing G
for i in range(p):
    if E.super_mult(G,i) == inf:
        print(i)

#Cyclic Group Order


# ## Message Exchange
# 
# We assume the generator $G$ and Elliptic Curve $E$ have already been shared between the sender and recipient.

# In[125]:


def encrypt(plain, receiver_public_key, sender_private_key):
    X=[]
    M=0
    p,B = receiver_public_key
    S = E.super_mult(B,sender_private_key)
    cipher = S[0] + S[1]
    for i in plain:
        M = ord(i)
        c = cipher*M     #for now, we only multiply
        X.append(c)
    return (X)


# In[126]:


def decrypt(cipher,receiver_private_key):
    X=''
    M=0
    ciphertext,sender_public_key = cipher
    S = E.super_mult(sender_public_key,receiver_private_key)
    m = S[0] + S[1]
    for i in ciphertext:
        x = int(i/m)         #reversing the multiplication
        M = chr(x)
        X+=M
    return (X)


# ### For creating Public Keys

# In[127]:


def randomInteger(k = 6):
    a = random.randint(0,pow(2,k-1))
    return a


# ### B's Public Key

# In[128]:


b = randomInteger() #private key

B = E.super_mult(G,b)

public_key = (p,B)


# ### A's Public Key (using B's Public Key)

# In[129]:


a = randomInteger() #private key
A = E.super_mult(G,a)


# ## A Encrypting

# In[130]:


plaintext = "Hello, this is ECDH"
ciphertext = encrypt(plaintext, public_key, a)

#print(ciphertext)

cipher = (ciphertext, A)


# ## B Decrypting

# In[131]:


message = decrypt(cipher, b)
print(message)


# ## Verification

# In[132]:


message == plaintext

