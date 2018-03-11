import base64
import binascii
import struct


def b64encode(s, altchars=None):
   encoded = binascii.b2a_base64(s)[:-1]
   if altchars is not None:
      return (encoded, {'+': altchars[0], '/': altchars[1]})
   return encoded

def b64decode(s, altchars=None):
   if altchars is not None:
      s = (s, {altchars[0]: '+', altchars[1]: '/'})
   try:
      return binascii.a2b_base64(s)
   except binascii.Error, msg:
      # Transform this exception for consistency
      raise TypeError(msg)

print b64encode("man12345")
print b64decode(b64encode("man12345"))

