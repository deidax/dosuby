import socket

def get_ip(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            value = socket.gethostbyname(value)
        except:
            pass
        
        return value
    return wrapper

def get_hostname(func):
    def wrapper(*args, **kwargs):
        value = func(*args, **kwargs)
        
        try:
            value = socket.gethostbyaddr(value)[0]
        except socket.error:
            value = "No reverse DNS record found"
        
        return value
    return wrapper