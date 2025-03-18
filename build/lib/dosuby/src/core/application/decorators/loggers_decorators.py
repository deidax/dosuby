import logging
from dosuby.src.core.domain.config import Config
from dosuby.src.core.domain.cache import Cache
from dosuby.src.serializers.extract_domain_serializer import ExtractUriSerializer
import socket
from dosuby.infrastructure.libs.loader import Loader

R = '\033[31m'  # red
G = '\033[32m'  # green
C = '\033[36m'  # cyan
W = '\033[0m'   # white
Y = '\033[33m'  # yellow

LOADER = Loader()

def enumerating(func):
    def wrapper(*args, **kwargs):
        while True:
            global LOADER
            LOADER.stop()
            info = f"{C}[*]  Enumerating{C}"
            LOADER = Loader(info, end=f"{info} ->{W} [Done] {W}")
            LOADER.start()
            result = func(*args, **kwargs)
            return result
    return wrapper

def info_logger(message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # logging.info(f"{C}[*]  {message}{C}")
            
            # global LOADER
            # LOADER.stop()
            info = f"{C}[*]  {message}{C}"
            # LOADER = Loader(info, end=f"{info} ->{W} [Done] {W}")
            # LOADER.start()
            logging.info(info)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def info_logger_attribute(attr_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            message = getattr(args[0], attr_name)
            logging.info(f"{C}[*]  {message}{C}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# def info_ip_found(attr_name):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             skip = getattr(args[0], attr_name)
#             value = func(*args, **kwargs)
            
#             if not skip:
#                 if value:
#                     logging.info(f"[*]  IP found: {value}")
#                 else:
#                     logging.warning("[!]    Could not found IP address")
            
#             return value
        
#         return wrapper
#     return decorator

def info_subdomain_found(attr_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            skip = getattr(args[0], attr_name)
            value = func(*args, **kwargs)
            if not skip:
                if value:
                    config = Config()
                    cache = Cache()
                    sub_ser = ExtractUriSerializer.serialize(uri=args[1])
                    if not config.scanning_modules:
                        
                        ip = None
                        
                        try:
                            ip = socket.gethostbyname(sub_ser)
                        except:
                            pass
                        
                        if ip:
                            info = f"{G}[+]  {sub_ser} --> {ip}{G}"
                            logging.info(info)
                        else:
                            info = f"{Y}[!]  {sub_ser} [Could not find IP address]{Y}"
                            logging.info(info)
                            
                    # else:
                        # global LOADER
                        # LOADER.stop()
                        
                        # info = f"[*]{C}  Subdomain found {sub_ser}. Scanning for [open ports, CMS, WebServer]...{C}"
                        # LOADER = Loader(info, end=f"{info} ->{W} [Done] {W}")
                        # LOADER.start()
                        # logging.info(f"[*]{C}  Subdomain found {sub_ser}{C}")
                    
                    cache.cached_enumeration_result_count = cache.cached_enumeration_result_count + 1
            return value
        
        return wrapper
    return decorator


# def info_port_scanning(ports):
#     global LOADER
#     LOADER.stop()
#     while ports == 'EMPTY':
#         info = f"{C}[*]  Start port scanning{C}"
#         LOADER = Loader(info)
#         LOADER.start()
        
#     LOADER.end = f"{C}[*]  Port scanning{C} -> {G} [Done] {G}"
#     LOADER.stop()
    
#     return ports

# def info_cms_scanning(attr_name):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             skip = getattr(args[0], attr_name)
#             value = func(*args, **kwargs)
#             if not skip:
#                 if value:
#                     global LOADER
#                     LOADER.stop()
#                     info = f"{C}[*]  Scanning for CMS{C}"
#                     LOADER = Loader(info, end=f"{info} ->{W} [Done] {W}")
#                     LOADER.start()
#             return value
        
#         return wrapper
#     return decorator

def log_subdomain_info(subdomain_uri):
    config = Config()
    logging.info(f"[*]{C}  ==> {subdomain_uri}{C}")
    # if config.scanning_modules:
    #     cache_singleton = Cache()
    #     if subdomain_uri not in cache_singleton.tmp_subdomains:
    #         cache_singleton.add_subdomain_uri(subdomain_uri)
    #         logging.info(f"[*]{C}  Subdomain found {subdomain_uri}{C}")