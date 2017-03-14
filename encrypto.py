# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 15:23:53 2016

@author: Vidyut
"""

import bcrypt
password = b"super secret password"
# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt(rounds=10))
# Check that a unhashed password matches one that has previously been
#   hashed
if bcrypt.hashpw(password, hashed) == hashed:
    print("It Matches!")
else:
    print("It Does not Match :(")
    
    
from passlib.hash import md5_crypt


%time h = md5_crypt.encrypt(str(0.54545435565))
chk = [m for m in range(len(h) if h[m]=='$')]
hashed = h[chk[len(chk)-1]+1:]
