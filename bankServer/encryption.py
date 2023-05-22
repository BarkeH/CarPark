from ecies import decrypt
import binascii

def getPrivateKey():
    with open('keys/private.txt') as f:
        for line in f:
            return binascii.unhexlify(''.join(line.split()))

def decryptMessage(message):
    privateKey = getPrivateKey()
    print(privateKey)
    print(message)
    unhexed = binascii.unhexlify(message)
    print(unhexed)
    decryptedMessage = decrypt(privateKey, unhexed)
    return decryptedMessage.decode('utf-8')
