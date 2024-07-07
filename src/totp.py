
import time 
import pyotp 
import qrcode 

key =  "GUZTEMBQGQZDKXZVKBDUWRKZ"
  
uri = pyotp.totp.TOTP(key).provisioning_uri( 
    name='5Paisa.com', 
    issuer_name='53200425') 
  
print(uri) 
  
  
# Qr code generation step 
qrcode.make(uri).save("qr.png") 
  
"""Verifying stage starts"""
  
totp = pyotp.TOTP(key) 

print(totp.now())
#print(totp.generate_otp())
# verifying the code 
# while True: 
#   print(totp.verify(input(("Enter the Code : "))))