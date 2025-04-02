import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dosuby.src.interfaces.cms_enumeration_adapter import CMSEnumerationAdapter

class WordPressScanningAdapter(CMSEnumerationAdapter):
    """WordPress-specific scanning adapter
    
    This adapter handles detection of WordPress installations and their versions.
    """
    
    def __init__(self):
        super().__init__()
        self.detection_points = 0
        self.version_patterns = [
            # Pattern for wp-includes version in HTML source
            (r'wp-includes\/js\/wp-emoji-release\.min\.js\?ver=([\d.]+)', 'JavaScript version'),
            # Pattern for generator meta tag
            (r'<meta name="generator" content="WordPress ([\d.]+)"', 'Generator tag'),
            # Pattern for readme.html
            (r'<br />\s*Version ([\d.]+)', 'Readme file'),
            # Pattern for RSS feed version
            (r'<generator>https:\/\/wordpress\.org\/\?v=([\d.]+)<\/generator>', 'RSS feed')
        ]
        
    def detect_cms(self):
        """Detect if the site is running WordPress
        
        Returns:
            dict: Detection result with type and confidence level
        """
        self.detection_points = 0
        evidence = []
        
        # Check for WordPress login page
        wp_login = self.make_request(self.subdomain_uri, '/wp-login.php')
        if wp_login.status_code == 200 and "user_login" in wp_login.text and "404" not in wp_login.text:
            self.detection_points += 30
            evidence.append("WP-Login page detected")
        
        # Check for wp-admin directory
        wp_admin = self.make_request(self.subdomain_uri, '/wp-admin')
        if wp_admin.status_code == 200 and "user_login" in wp_admin.text and "404" not in wp_admin.text:
            self.detection_points += 30
            evidence.append("WP-Admin page detected")
        
        # Check for upgrade.php
        wp_upgrade = self.make_request(self.subdomain_uri, '/wp-admin/upgrade.php')
        if wp_upgrade.status_code == 200 and "WordPress database upgrade" in wp_upgrade.text:
            self.detection_points += 20
            evidence.append("WordPress upgrade page detected")
        
        # Check for readme.html
        wp_readme = self.make_request(self.subdomain_uri, '/readme.html')
        if wp_readme.status_code == 200 and "WordPress" in wp_readme.text and "404" not in wp_readme.text:
            self.detection_points += 25
            evidence.append("WordPress readme.html detected")
        
        # Check for wp-content directory
        wp_content = self.make_request(self.subdomain_uri, '/wp-content/')
        if wp_content.status_code == 200 or wp_content.status_code == 403:
            self.detection_points += 20
            evidence.append("wp-content directory found")
        
        # Check for wp-includes directory
        wp_includes = self.make_request(self.subdomain_uri, '/wp-includes/')
        if wp_includes.status_code == 200 or wp_includes.status_code == 403:
            self.detection_points += 20
            evidence.append("wp-includes directory found")
            
        # Check homepage for WordPress references
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            if 'wp-content' in homepage.text or 'wp-includes' in homepage.text:
                self.detection_points += 15
                evidence.append("WordPress references in homepage")
                
            # Check for common WP fingerprints in source
            if 'wp-emoji' in homepage.text or 'wp-block-library' in homepage.text:
                self.detection_points += 15
                evidence.append("WordPress JavaScript libraries detected")
        
        # Determine confidence level based on detection points
        confidence = "Low"
        if self.detection_points >= 50:
            confidence = "Medium"
        if self.detection_points >= 75:
            confidence = "High"
            
        is_detected = self.detection_points >= 30
            
        return {
            "cms": "WordPress", 
            "detected": is_detected,
            "confidence": confidence,
            "score": self.detection_points,
            "evidence": evidence
        }
        
    def detect_version(self):
        """Detect WordPress version if present
        
        Returns:
            str: WordPress version string if detected, None otherwise
        """
        version_evidence = {}
        
        # Check the homepage
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            for pattern, source in self.version_patterns:
                match = re.search(pattern, homepage.text)
                if match:
                    version_evidence[source] = match.group(1)
        
        # Check readme.html which often contains version info
        readme = self.make_request(self.subdomain_uri, '/readme.html')
        if readme.status_code == 200:
            match = re.search(r'<br />\s*Version ([\d.]+)', readme.text)
            if match:
                version_evidence['Readme file'] = match.group(1)
        
        # Check license.txt which may contain version
        license_txt = self.make_request(self.subdomain_uri, '/license.txt')
        if license_txt.status_code == 200 and "WordPress" in license_txt.text:
            match = re.search(r'WordPress - Web publishing software\s*\n*\s*Copyright \d{4}(?:-\d{4})? by the contributors\s*\n*\s*Version ([\d.]+)', license_txt.text)
            if match:
                version_evidence['License file'] = match.group(1)
                
        # Check XML-RPC API
        xmlrpc = self.make_request(self.subdomain_uri, '/xmlrpc.php')
        if xmlrpc.status_code == 405 or "XML-RPC server accepts POST requests only" in xmlrpc.text:
            # XML-RPC is enabled, we could potentially query it for system.getCapabilities
            version_evidence['XML-RPC'] = "Detected but version not extracted"
            
        # Check feed page
        feed = self.make_request(self.subdomain_uri, '/feed/')
        if feed.status_code == 200:
            match = re.search(r'<generator>https:\/\/wordpress\.org\/\?v=([\d.]+)<\/generator>', feed.text)
            if match:
                version_evidence['RSS feed'] = match.group(1)
                
        # Return the most reliable version found or None
        if version_evidence:
            # Prioritize versions found in more reliable sources
            for source in ['Readme file', 'License file', 'Generator tag', 'RSS feed']:
                if source in version_evidence:
                    return version_evidence[source]
            
            # If none of the preferred sources are available, return any version found
            return next(iter(version_evidence.values()))
            
        return None
        
    def _process(self, uri: str):
        """Process WordPress detection and version identification
        
        Args:
            uri (str): The subdomain URI to scan
            
        Returns:
            dict: Detection result including CMS type, version, and evidence
        """
        self.subdomain_uri = uri
        return self.get_result()