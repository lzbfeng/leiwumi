import md5

def MD5(info):
        key = md5.new(info)
        return key.digest()