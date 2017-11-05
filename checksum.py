"""
CertUtil is a pre-installed Windows utility, that can be used to generate hash checksums:

certUtil -hashfile pathToFileToCheck [HashAlgorithm]
HashAlgorithm choices: MD2 MD4 MD5 SHA1 SHA256 SHA384 SHA512

e.g.:
PS C:\Users\vesna> certUtil -hashfile C:\Users\vesna\Documents\Progs\pycharm-community-2017.2.2.exe SHA256
"""

curr = "48 8e 6e 50 d4 4f 2a 56 e4 bb cd f2 ef c2 b2 95 e8 05 87 ad 63 58 29 76 0a c1 f9 ca 2c 0e b9 98"
curr = ''.join([char for char in curr if char != ' '])
print(curr == '488e6e50d44f2a56e4bbcdf2efc2b295e80587ad635829760ac1f9ca2c0eb998')
