import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from src.interfaces.cms_enumeration_adapter import CMSEnumerationAdapter

class WordPressScanningAdapter(CMSEnumerationAdapter):
    
    
    
    
    def run(self):
        if self.subdomain_ip:
            return self._process(ip=self.subdomain_ip)
        return None
    

    def _process(self, ip) -> str | None:
        wpLoginCheck = self.scann_for_cms_by_url(ip, '/wp-login.php')
        if wpLoginCheck.status_code == 200 and "user_login" in wpLoginCheck.text and "404" not in wpLoginCheck.text:
            return "Potential WordPress WP-Login page"

        wpAdminCheck = self.scann_for_cms_by_url(ip, '/wp-admin')
        if wpAdminCheck.status_code == 200 and "user_login" in wpAdminCheck.text and "404" not in wpAdminCheck.text:
            return "Potential WordPress WP-Admin page"
    
        wpAdminUpgradeCheck = self.scann_for_cms_by_url(ip, '/wp-admin/upgrade.php')
        if wpAdminCheck.status_code == 200 and "user_login" in wpAdminUpgradeCheck.text and "404" not in wpAdminUpgradeCheck.text:
            return "Potential WordPress WP-Admin page"
    
        wpLinksCheck = self.scann_for_cms_by_url(ip, '/')
        if 'wp-' in wpLinksCheck.text:
            return "Potential WordPress wp- style links detected on index"
    
        wpAdminReadMeCheck = self.scann_for_cms_by_url(ip, '/readme.html')
        if wpAdminReadMeCheck.status_code == 200 and "404" not in wpAdminReadMeCheck.text:
            return "Potential WordPress Readme.html"
        
        return None

    def scann_for_cms_by_url(self, ip, index):
        print(f"http://{ip}{index}")
        return requests.get(f"http://{ip}{index}", allow_redirects=False, headers=self.user_agent, verify=False)