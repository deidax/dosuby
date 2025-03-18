from dosuby.src.interfaces.security_enumeration import SecurityEnumeration

class WebserverEnumerationAdapter(SecurityEnumeration):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using the Sockets

        """
        super().__init__()
    
    
    def run(self):
        return self._process()
    

    def _process(self, **kwargs):
        return super()._process(**kwargs)
        