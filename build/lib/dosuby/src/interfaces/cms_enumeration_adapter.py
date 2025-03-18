from dosuby.src.interfaces.security_enumeration import SecurityEnumeration

class CMSEnumerationAdapter(SecurityEnumeration):
    
    def __init__(self) -> None:
        """This class will manage the port enumeration logic using the Sockets

        """
        super().__init__()
        self.subdomain_uri = ''
        self.user_agent = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
            }
        
    
    
    def run(self):
        yield self._process()
    

    def _process(self, **kwargs):
        return super()._process(**kwargs)
    
    def scann_for_cms_by_url(self, ip, index):
        """Run the CMS scan logic for the given IP using url

        Args:
            ip (str): Subdomain IP
            index (str): page name related to a cms
        """
        NotImplementedError("scann_for_cms is not implemented")