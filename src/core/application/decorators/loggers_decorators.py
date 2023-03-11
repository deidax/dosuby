import logging

def simple_logging_display(message: str):
    logging.info(f"[*]  {message}")

def info_logger(message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logging.info(f"[*]  {message}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def info_logger_attribute(attr_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            message = getattr(args[0], attr_name)
            logging.info(f"[*]  {message}")
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
                    logging.info(f"[*]  Subdomain found {args[1]}")
            return value
        
        return wrapper
    return decorator

def info_port_scanning(attr_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            skip = getattr(args[0], attr_name)
            value = func(*args, **kwargs)
            if not skip:
                if value:
                    logging.info(f"[*]  Scanning ports")
            return value
        
        return wrapper
    return decorator

def info_cms_scanning(attr_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            skip = getattr(args[0], attr_name)
            value = func(*args, **kwargs)
            if not skip:
                if value:
                    logging.info(f"[*]  Scanning for CMS")
            return value
        
        return wrapper
    return decorator