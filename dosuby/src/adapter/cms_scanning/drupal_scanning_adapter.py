import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dosuby.src.interfaces.cms_enumeration_adapter import CMSEnumerationAdapter

class DrupalScanningAdapter(CMSEnumerationAdapter):
    """Drupal-specific scanning adapter
    
    This adapter handles detection of Drupal installations and their versions.
    """
    
    def __init__(self):
        super().__init__()
        self.detection_points = 0
        self.version_patterns = [
            # Pattern for generator meta tag
            (r'<meta name="Generator" content="Drupal ([\d.]+)', 'Generator tag'),
            # Pattern for version in changelog
            (r'Drupal ([\d.]+), \d{4}-\d{2}-\d{2}', 'Changelog'),
            # Pattern for version in .info files
            (r'version\s*=\s*"([\d.]+)"', 'Info file')
        ]
        
    def detect_cms(self):
        """Detect if the site is running Drupal
        
        Returns:
            dict: Detection result with type and confidence level
        """
        self.detection_points = 0
        evidence = []
        
        # Check for Drupal admin page
        admin = self.make_request(self.subdomain_uri, '/admin')
        if admin.status_code == 200 and "Drupal" in admin.text:
            self.detection_points += 25
            evidence.append("Drupal admin page detected")
            
        # Check for user login page
        user_login = self.make_request(self.subdomain_uri, '/user/login')
        if user_login.status_code == 200 and ("user-login-form" in user_login.text or "Drupal" in user_login.text):
            self.detection_points += 30
            evidence.append("Drupal user login page detected")
            
        # Check for CHANGELOG.txt which is often present in Drupal
        changelog = self.make_request(self.subdomain_uri, '/CHANGELOG.txt')
        if changelog.status_code == 200 and "Drupal" in changelog.text:
            self.detection_points += 35
            evidence.append("Drupal CHANGELOG.txt found")
            
        # Check for install.php
        install = self.make_request(self.subdomain_uri, '/install.php')
        if install.status_code == 200 and "Drupal" in install.text:
            self.detection_points += 35
            evidence.append("Drupal install.php found")
            
        # Check for common Drupal directories
        for path in ['/sites/all/modules/', '/sites/all/themes/', '/sites/default/']:
            response = self.make_request(self.subdomain_uri, path)
            if response.status_code == 200 or response.status_code == 403:
                self.detection_points += 15
                evidence.append(f"Drupal directory found: {path}")
                
        # Check homepage for Drupal-specific signs
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            # Check for Drupal CSS/JS paths
            for pattern in ['/sites/default/files/', '/sites/all/', 'drupal.js', 'Drupal.settings']:
                if pattern in homepage.text:
                    self.detection_points += 10
                    evidence.append(f"Drupal pattern found in homepage: {pattern}")
                    
            # Check for generator meta tag
            if re.search(r'<meta name="Generator" content="Drupal', homepage.text):
                self.detection_points += 25
                evidence.append("Drupal generator meta tag found")
                
        # Check for Drupal's README.txt
        readme = self.make_request(self.subdomain_uri, '/README.txt')
        if readme.status_code == 200 and "Drupal" in readme.text:
            self.detection_points += 25
            evidence.append("Drupal README.txt found")
            
        # Determine confidence level based on detection points
        confidence = "Low"
        if self.detection_points >= 50:
            confidence = "Medium"
        if self.detection_points >= 75:
            confidence = "High"
            
        is_detected = self.detection_points >= 30
            
        return {
            "cms": "Drupal", 
            "detected": is_detected,
            "confidence": confidence,
            "score": self.detection_points,
            "evidence": evidence
        }
        
    def detect_version(self):
        """Detect Drupal version if present
        
        Returns:
            str: Drupal version string if detected, None otherwise
        """
        version_evidence = {}
        
        # Check for CHANGELOG.txt which often contains version info
        changelog = self.make_request(self.subdomain_uri, '/CHANGELOG.txt')
        if changelog.status_code == 200 and "Drupal" in changelog.text:
            # Look for the first version mention which is typically the current version
            match = re.search(r'Drupal ([\d.]+),\s+\d{4}-\d{2}-\d{2}', changelog.text)
            if match:
                version_evidence['Changelog'] = match.group(1)
                
        # Check for version in .info files
        info_files = [
            '/themes/bartik/bartik.info',
            '/themes/seven/seven.info',
            '/themes/garland/garland.info',
            '/core/modules/system/system.info.yml'  # Drupal 8+
        ]
        
        for path in info_files:
            info_file = self.make_request(self.subdomain_uri, path)
            if info_file.status_code == 200:
                # Drupal 7 and below use .info files with version = "x.y.z"
                match = re.search(r'version\s*=\s*"([\d.]+)"', info_file.text)
                if match:
                    version_evidence['Info file'] = match.group(1)
                    break
                    
                # Drupal 8+ uses .info.yml files
                match = re.search(r'version:\s*[\'"]?([\d.]+)[\'"]?', info_file.text)
                if match:
                    version_evidence['Info file'] = match.group(1)
                    break
                    
        # Check the homepage for generator meta tag
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            match = re.search(r'<meta name="Generator" content="Drupal ([\d.]+)', homepage.text)
            if match:
                version_evidence['Generator tag'] = match.group(1)
                
        # Check /core/install.php for Drupal 8+
        core_install = self.make_request(self.subdomain_uri, '/core/install.php')
        if core_install.status_code == 200 and "Drupal" in core_install.text:
            match = re.search(r'Drupal (8|9|10)\.', core_install.text)
            if match:
                version_evidence['Install page'] = match.group(1) + '.x'
                
        # Return the most reliable version found or None
        if version_evidence:
            # Prioritize versions found in more reliable sources
            for source in ['Changelog', 'Info file', 'Generator tag', 'Install page']:
                if source in version_evidence:
                    return version_evidence[source]
            
            # If none of the preferred sources are available, return any version found
            return next(iter(version_evidence.values()))
            
        return None
        
    def _process(self, uri: str):
        """Process Drupal detection and version identification
        
        Args:
            uri (str): The subdomain URI to scan
            
        Returns:
            dict: Detection result including CMS type, version, and evidence
        """
        self.subdomain_uri = uri
        return self.get_result()