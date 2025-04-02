import re
from dosuby.src.interfaces.cms_enumeration_adapter import CMSEnumerationAdapter

class MoodleScanningAdapter(CMSEnumerationAdapter):
    """Moodle-specific scanning adapter
    
    This adapter handles detection of Moodle Learning Management System installations and their versions.
    """
    
    def __init__(self):
        super().__init__()
        self.detection_points = 0
        self.version_patterns = [
            # Pattern for generator meta tag
            (r'<meta name="generator" content="Moodle ([\d.]+)', 'Generator tag'),
            # Pattern for version in footer
            (r'<div class="[^"]*version[^"]*">Moodle[™ ]*([\d.]+)', 'Footer'),
            # Pattern for version in login page
            (r'<a href="https?://moodle.org/[^>]+>Moodle[™ ]*([\d.]+)', 'Login page'),
            # Pattern for version in JavaScript files
            (r'var M\.cfg = \{.*?"version":"([\d.]+)"', 'JavaScript config')
        ]
        
    def detect_cms(self):
        """Detect if the site is running Moodle
        
        Returns:
            dict: Detection result with type and confidence level
        """
        self.detection_points = 0
        evidence = []
        
        # Check for Moodle login page
        login = self.make_request(self.subdomain_uri, '/login/index.php')
        if login.status_code == 200 and ("Moodle" in login.text or "moodle-index-login" in login.text):
            self.detection_points += 30
            evidence.append("Moodle login page detected")
            
        # Check for Moodle /course directory
        course = self.make_request(self.subdomain_uri, '/course/')
        if course.status_code == 200 and "Moodle" in course.text:
            self.detection_points += 25
            evidence.append("Moodle course directory found")
            
        # Check for Moodle admin page
        admin = self.make_request(self.subdomain_uri, '/admin/')
        if admin.status_code == 200 and "Moodle" in admin.text:
            self.detection_points += 25
            evidence.append("Moodle admin directory found")
            
        # Check for Moodle config file (not accessible but common location)
        config = self.make_request(self.subdomain_uri, '/config.php')
        if config.status_code != 404:
            self.detection_points += 15
            evidence.append("Potential Moodle config.php found")
            
        # Check for Moodle installation script
        install = self.make_request(self.subdomain_uri, '/install.php')
        if install.status_code == 200 and "Moodle installation" in install.text:
            self.detection_points += 35
            evidence.append("Moodle installation script found")
            
        # Check for Moodle upgrade script
        upgrade = self.make_request(self.subdomain_uri, '/admin/upgrade.php')
        if upgrade.status_code == 200 and "Moodle upgrade" in upgrade.text:
            self.detection_points += 25
            evidence.append("Moodle upgrade script found")
            
        # Check for specific Moodle directories
        moodle_dirs = ['/lib/', '/mod/', '/theme/', '/blocks/']
        for directory in moodle_dirs:
            response = self.make_request(self.subdomain_uri, directory)
            if response.status_code == 200 or response.status_code == 403:
                self.detection_points += 10
                evidence.append(f"Moodle directory found: {directory}")
                
        # Check homepage for Moodle-specific signs
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            # Check for Moodle meta generator tag
            if re.search(r'<meta name="generator" content="Moodle', homepage.text):
                self.detection_points += 30
                evidence.append("Moodle generator meta tag found")
                
            # Check for common Moodle JavaScript
            if 'require.min.js' in homepage.text and 'M.cfg' in homepage.text:
                self.detection_points += 20
                evidence.append("Moodle JavaScript detected")
                
            # Check for common Moodle CSS classes
            for pattern in ['moodle-has-zindex', 'moodleheader', 'logininfo']:
                if pattern in homepage.text:
                    self.detection_points += 10
                    evidence.append(f"Moodle CSS pattern found: {pattern}")
                    
        # Check for Moodle documentation
        docs = self.make_request(self.subdomain_uri, '/admin/mnet/environment.php')
        if docs.status_code == 200 and "Moodle" in docs.text:
            self.detection_points += 15
            evidence.append("Moodle environment page found")
            
        # Check robots.txt for Moodle exclusions
        robots = self.make_request(self.subdomain_uri, '/robots.txt')
        if robots.status_code == 200 and ("/mod/" in robots.text or "/course/" in robots.text):
            self.detection_points += 10
            evidence.append("Moodle patterns in robots.txt")
            
        # Determine confidence level based on detection points
        confidence = "Low"
        if self.detection_points >= 50:
            confidence = "Medium"
        if self.detection_points >= 75:
            confidence = "High"
            
        is_detected = self.detection_points >= 30
            
        return {
            "cms": "Moodle", 
            "detected": is_detected,
            "confidence": confidence,
            "score": self.detection_points,
            "evidence": evidence
        }
        
    def detect_version(self):
        """Detect Moodle version if present
        
        Returns:
            str: Moodle version string if detected, None otherwise
        """
        version_evidence = {}
        
        # Check the homepage for version information
        homepage = self.make_request(self.subdomain_uri, '/', allow_redirects=True)
        if homepage.status_code == 200:
            for pattern, source in self.version_patterns:
                match = re.search(pattern, homepage.text)
                if match:
                    version_evidence[source] = match.group(1)
                    
        # Check login page which often contains version info
        login = self.make_request(self.subdomain_uri, '/login/index.php')
        if login.status_code == 200:
            for pattern, source in self.version_patterns:
                match = re.search(pattern, login.text)
                if match:
                    version_evidence[source] = match.group(1)
                    
        # Check Moodle version.php if accessible (rare but possible)
        version_php = self.make_request(self.subdomain_uri, '/version.php')
        if version_php.status_code == 200 and "$version" in version_php.text:
            match = re.search(r'\$version\s*=\s*(\d{10}(\.\d+)?)', version_php.text)
            if match:
                version_evidence['Version file'] = match.group(1)
                
        # Check pix/t/deleted.png which has version-specific URL
        pix_test = self.make_request(self.subdomain_uri, '/pix/t/deleted.png')
        if pix_test.status_code == 200:
            # If the file exists, try to check for version in various JavaScript files
            js_file = self.make_request(self.subdomain_uri, '/lib/javascript.php')
            if js_file.status_code == 200:
                match = re.search(r'var moodleVersion\s*=\s*[\'"]([^\'"]+)[\'"]', js_file.text)
                if match:
                    version_evidence['JavaScript version'] = match.group(1)
                    
        # Check for version in admin environment page
        admin_env = self.make_request(self.subdomain_uri, '/admin/environment.php')
        if admin_env.status_code == 200 and "Moodle" in admin_env.text:
            match = re.search(r'Moodle version</td>\s*<td[^>]*>([\d.]+)', admin_env.text)
            if match:
                version_evidence['Environment page'] = match.group(1)
                
        # Check for release notes that may reveal version
        release = self.make_request(self.subdomain_uri, '/admin/index.php')
        if release.status_code == 200:
            match = re.search(r'Release notes for ([\d.]+)', release.text)
            if match:
                version_evidence['Release notes'] = match.group(1)
                
        # Return the most reliable version found or None
        if version_evidence:
            # Prioritize versions found in more reliable sources
            for source in ['Environment page', 'Generator tag', 'Version file', 'Footer', 'Login page']:
                if source in version_evidence:
                    return version_evidence[source]
            
            # If none of the preferred sources are available, return any version found
            return next(iter(version_evidence.values()))
            
        return None
        
    def _process(self, uri: str):
        """Process Moodle detection and version identification
        
        Args:
            uri (str): The subdomain URI to scan
            
        Returns:
            dict: Detection result including CMS type, version, and evidence
        """
        self.subdomain_uri = uri
        return self.get_result()