import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dosuby.src.interfaces.cms_enumeration_adapter import CMSEnumerationAdapter

class JoomlaScanningAdapter(CMSEnumerationAdapter):
    """Joomla-specific scanning adapter
    
    This adapter handles detection of Joomla installations and their versions.
    """
    
    def __init__(self):
        super().__init__()
        self.detection_points = 0
        self.version_patterns = [
            # Pattern for generator meta tag
            (r'<meta name="generator" content="Joomla! ([\d.]+)', 'Generator tag'),
            # Pattern for version in administrator login page
            (r'<div class="joomla-version[^>]*>Joomla! ([\d.]+)', 'Admin login'),
            # Pattern for XML manifest files
            (r'<version>([\d.]+)</version>', 'Manifest file')
        ]
        
    def detect_cms(self):
        """Detect if the site is running Joomla
        
        Returns:
            dict: Detection result with type and confidence level
        """
        self.detection_points = 0
        evidence = []
        
        # Check for Joomla administrator login
        admin_login = self.make_request(self.subdomain_uri, '/administrator/')
        if admin_login.status_code == 200 and ("Joomla" in admin_login.text or "mod-login-username" in admin_login.text):
            self.detection_points += 30
            evidence.append("Joomla administrator login page detected")
        
        # Check for Joomla installation directory
        installation = self.make_request(self.subdomain_uri, '/installation/')
        if installation.status_code == 200 and "Joomla" in installation.text:
            self.detection_points += 35
            evidence.append("Joomla installation directory found")
        
        # Check for component directory
        components = self.make_request(self.subdomain_uri, '/components/')
        if components.status_code == 200 or components.status_code == 403:
            self.detection_points += 15
            evidence.append("Joomla components directory found")
            
        # Check for modules directory
        modules = self.make_request(self.subdomain_uri, '/modules/')
        if modules.status_code == 200 or modules.status_code == 403:
            self.detection_points += 15
            evidence.append("Joomla modules directory found")
            
        # Check for templates directory
        templates = self.make_request(self.subdomain_uri, '/templates/')
        if templates.status_code == 200 or templates.status_code == 403:
            self.detection_points += 15
            evidence.append("Joomla templates directory found")
            
        # Check homepage for Joomla references
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            # Check for Joomla script paths
            if '/media/jui/' in homepage.text or '/media/system/js/' in homepage.text:
                self.detection_points += 20
                evidence.append("Joomla script references in homepage")
                
            # Check for Joomla meta generator tag
            if re.search(r'<meta name="generator" content="Joomla', homepage.text):
                self.detection_points += 25
                evidence.append("Joomla generator meta tag found")
                
        # Check for robots.txt with Joomla references
        robots = self.make_request(self.subdomain_uri, '/robots.txt')
        if robots.status_code == 200 and "joomla" in robots.text.lower():
            self.detection_points += 15
            evidence.append("Joomla references in robots.txt")
            
        # Determine confidence level based on detection points
        confidence = "Low"
        if self.detection_points >= 50:
            confidence = "Medium"
        if self.detection_points >= 75:
            confidence = "High"
            
        is_detected = self.detection_points >= 30
            
        return {
            "cms": "Joomla", 
            "detected": is_detected,
            "confidence": confidence,
            "score": self.detection_points,
            "evidence": evidence
        }
        
    def detect_version(self):
        """Detect Joomla version if present
        
        Returns:
            str: Joomla version string if detected, None otherwise
        """
        version_evidence = {}
        
        # Check the homepage for generator tag
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            match = re.search(r'<meta name="generator" content="Joomla! ([\d.]+)', homepage.text)
            if match:
                version_evidence['Generator tag'] = match.group(1)
                
        # Check administrator login page
        admin_login = self.make_request(self.subdomain_uri, '/administrator/')
        if admin_login.status_code == 200:
            match = re.search(r'<div class="joomla-version[^>]*>Joomla! ([\d.]+)', admin_login.text)
            if match:
                version_evidence['Admin login'] = match.group(1)
                
        # Check XML manifest files that may contain version info
        manifest_paths = [
            '/administrator/manifests/files/joomla.xml',
            '/language/en-GB/en-GB.xml',
            '/modules/mod_menu/mod_menu.xml'
        ]
        
        for path in manifest_paths:
            manifest = self.make_request(self.subdomain_uri, path)
            if manifest.status_code == 200:
                match = re.search(r'<version>([\d.]+)</version>', manifest.text)
                if match:
                    version_evidence['Manifest file'] = match.group(1)
                    break
                    
        # Check for language strings which may contain version info
        lang_file = self.make_request(self.subdomain_uri, '/language/en-GB/en-GB.ini')
        if lang_file.status_code == 200:
            match = re.search(r'JVERSION="([\d.]+)"', lang_file.text)
            if match:
                version_evidence['Language file'] = match.group(1)
                
        # Return the most reliable version found or None
        if version_evidence:
            # Prioritize versions found in more reliable sources
            for source in ['Manifest file', 'Generator tag', 'Admin login', 'Language file']:
                if source in version_evidence:
                    return version_evidence[source]
            
            # If none of the preferred sources are available, return any version found
            return next(iter(version_evidence.values()))
            
        return None
        
    def _process(self, uri: str):
        """Process Joomla detection and version identification
        
        Args:
            uri (str): The subdomain URI to scan
            
        Returns:
            dict: Detection result including CMS type, version, and evidence
        """
        self.subdomain_uri = uri
        return self.get_result()