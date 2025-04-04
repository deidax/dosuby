from random import expovariate
from dosuby.src.interfaces.report_repo import ReportRepo
from dosuby.src.core.domain.enumeration_reporte import EnumerationReporte
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.box import Box, DOUBLE, ROUNDED
from rich.layout import Layout
from typing import List, Dict, Any, Optional, Union


class CliReportRepo(ReportRepo):
    """
    Command Line Interface Repository for displaying enumeration reports.
    Provides a rich and structured display of subdomain information and vulnerabilities.
    """

    def read_report(self):
        """
        Display the enumeration report in the command line interface with improved formatting.
        """
        # Get report data
        report = EnumerationReporte()
        report_subdomains = self._remove_duplicates(report.report_subdomains)
        
        # Create console
        console = Console()
        
        # Display header
        self._display_header(console)
        
        # Display statistics
        self._display_statistics(console, report_subdomains)
        
        # Display subdomains table
        self._display_subdomains_table(console, report_subdomains)
        
        # Display vulnerabilities section if scanning modules are enabled
        if self.config.scanning_modules:
            self._display_vulnerabilities_section(console, report_subdomains)

    def _display_header(self, console: Console):
        """
        Display a styled header for the report.
        
        Args:
            console: Rich console instance
        """
        console.print("\n")
        console.print("╔══════════════════════════════════════════════════════════════╗", style="bright_blue")
        console.print("║                      DOSUBY SCAN REPORT                      ║", style="bright_blue")
        console.print("╚══════════════════════════════════════════════════════════════╝", style="bright_blue")
        console.print("\n")

    def _display_statistics(self, console: Console, report_subdomains: List[Dict[str, Any]]):
        """
        Display summary statistics about the scan.
        
        Args:
            console: Rich console instance
            report_subdomains: List of subdomain dictionaries
        """
        # Count subdomains
        subdomain_count = len(report_subdomains)
        
        # Count vulnerabilities if applicable
        vuln_count = 0
        critical_count = 0
        high_count = 0
        
        if self.config.scanning_modules:
            for subdomain in report_subdomains:
                vulns = subdomain.get('subdomain_vulnerabilities', [])
                if isinstance(vulns, list):
                    vuln_count += len(vulns)
                    for vuln in vulns:
                        if isinstance(vuln, dict):
                            severity = vuln.get('severity', '').upper()
                            if severity == 'CRITICAL':
                                critical_count += 1
                            elif severity == 'HIGH':
                                high_count += 1
        
        # Create statistics panel
        stats_text = [
            f"Subdomains: [bright_green]{subdomain_count}[/bright_green]"
        ]
        
        if self.config.scanning_modules:
            stats_text.append(f"Vulnerabilities: [bright_yellow]{vuln_count}[/bright_yellow]")
            
            if critical_count > 0:
                stats_text.append(f"Critical: [bright_red]{critical_count}[/bright_red]")
            
            if high_count > 0:
                stats_text.append(f"High: [bright_yellow]{high_count}[/bright_yellow]")
        
        console.print(Panel(
            " | ".join(stats_text),
            title="Scan Statistics",
            border_style="bright_blue",
            box=ROUNDED
        ))
        console.print("\n")

    def _display_subdomains_table(self, console: Console, report_subdomains: List[Dict[str, Any]]):
        """
        Display an enhanced table with subdomain information.
        
        Args:
            console: Rich console instance
            report_subdomains: List of subdomain dictionaries
        """
        # Create table with improved styling
        table = Table(
            title="Discovered Subdomains",
            box=ROUNDED,
            header_style="bright_blue",
            border_style="blue",
            expand=True
        )
        
        # Define columns based on scanning modules setting
        if not self.config.scanning_modules:
            columns = ["Subdomain", "IP Address"]
        else:
            columns = ["Subdomain", "IP Address", "Open Ports", "CMS", "Web Server", "Vulnerabilities"]
        
        # Add columns with improved styling
        for col in columns:
            table.add_column(col, justify="left", style="bright_white")
        
        # Add rows to table
        for subdomain in report_subdomains:
            row = self._create_subdomain_row(subdomain)
            
            # Convert all row items to strings to avoid rendering errors
            row = [str(item) if item is not None else "N/A" for item in row]
            
            # Determine row style based on vulnerabilities
            row_style = "bright_green"
            if self.config.scanning_modules:
                vulns = subdomain.get('subdomain_vulnerabilities', [])
                if isinstance(vulns, list) and vulns:
                    # Check for critical vulnerabilities
                    has_critical = any(
                        isinstance(v, dict) and v.get('severity', '').upper() == 'CRITICAL'
                        for v in vulns
                    )
                    # Check for high vulnerabilities
                    has_high = any(
                        isinstance(v, dict) and v.get('severity', '').upper() == 'HIGH'
                        for v in vulns
                    )
                    
                    if has_critical:
                        row_style = "bright_red"
                    elif has_high:
                        row_style = "yellow"
            
            table.add_row(*row, style=row_style)
        
        console.print(table)
        console.print("\n")

    def _create_subdomain_row(self, subdomain: Dict[str, Any]) -> List[str]:
        """
        Create a table row for a subdomain with proper handling of all fields.
        
        Args:
            subdomain: Dictionary containing subdomain information
            
        Returns:
            List of strings representing a table row
        """
        # Basic info (always included)
        row = [
            subdomain.get('subdomain_uri', 'N/A'),
            subdomain.get('subdomain_ip', 'N/A')
        ]
        
        # If scanning modules are enabled, add additional columns
        if self.config.scanning_modules:
            # Open ports - convert to comma-separated string
            open_ports = subdomain.get('subdomain_open_ports', [])
            if isinstance(open_ports, list) and open_ports:
                open_ports_str = ", ".join(str(port) for port in open_ports)
            else:
                open_ports_str = "N/A"
            
            # CMS info
            cms_str = subdomain.get('subdomian_cms', 'N/A')
            
            # Web server info
            webserver_str = subdomain.get('subdomain_webserver', 'N/A')
            
            if not webserver_str:
                webserver_str = 'N/A'
                
            
            # Vulnerabilities summary
            vulns = subdomain.get('subdomain_vulnerabilities', [])
            if isinstance(vulns, list) and vulns:
                # Count by severity
                critical_count = sum(1 for v in vulns if isinstance(v, dict) and v.get('severity', '').upper() == 'CRITICAL')
                high_count = sum(1 for v in vulns if isinstance(v, dict) and v.get('severity', '').upper() == 'HIGH')
                medium_count = sum(1 for v in vulns if isinstance(v, dict) and v.get('severity', '').upper() == 'MEDIUM')
                
                # Create summary string
                vuln_parts = []
                if critical_count > 0:
                    vuln_parts.append(f"{critical_count} Critical")
                if high_count > 0:
                    vuln_parts.append(f"{high_count} High")
                if medium_count > 0:
                    vuln_parts.append(f"{medium_count} Medium")
                
                if not vuln_parts:
                    vuln_parts.append(f"{len(vulns)} Low/Unknown")
                
                vuln_str = ", ".join(vuln_parts)
            else:
                vuln_str = "N/A"
            
            # Add additional columns to row
            row.extend([open_ports_str, cms_str, webserver_str, vuln_str])
        
        return row

    def _display_vulnerabilities_section(self, console: Console, report_subdomains: List[Dict[str, Any]]):
        """
        Display detailed vulnerability information for each affected subdomain.
        
        Args:
            console: Rich console instance
            report_subdomains: List of subdomain dictionaries
        """
        # Check if any vulnerabilities exist
        has_vulnerabilities = False
        for subdomain in report_subdomains:
            vulns = subdomain.get('subdomain_vulnerabilities', [])
            if isinstance(vulns, list) and vulns:
                has_vulnerabilities = True
                break
        
        if not has_vulnerabilities:
            return
        
        # Display section header
        console.print("═" * 80, style="bright_blue")
        console.print("VULNERABILITY DETAILS", style="bright_blue bold")
        console.print("═" * 80, style="bright_blue")
        console.print("\n")
        
        # Display vulnerabilities for each affected subdomain
        for subdomain in report_subdomains:
            vulns = subdomain.get('subdomain_vulnerabilities', [])
            if not isinstance(vulns, list) or not vulns:
                continue
            
            # Display subdomain header
            console.print(f"[bold blue]● {subdomain.get('subdomain_uri', 'N/A')} ({subdomain.get('subdomain_ip', 'N/A')})[/bold blue]")
            
            # Create vulnerability table
            vuln_table = Table(
                box=ROUNDED,
                header_style="bright_white on blue",
                border_style="blue",
                expand=True
            )
            
            # Add columns
            vuln_table.add_column("CVE ID", style="bright_white")
            vuln_table.add_column("Severity", style="bright_white")
            vuln_table.add_column("CVSS", style="bright_white", justify="right")
            vuln_table.add_column("Exploitable", style="bright_white", justify="right")
            vuln_table.add_column("Description", style="bright_white")
            
            # Sort vulnerabilities by severity
            sorted_vulns = sorted(
                vulns,
                key=lambda v: {
                    "CRITICAL": 0, 
                    "HIGH": 1, 
                    "MEDIUM": 2, 
                    "LOW": 3
                }.get(v.get('severity', '').upper(), 4)
            )
            
            # Add vulnerabilities to table
            for vuln in sorted_vulns:
                if not isinstance(vuln, dict):
                    continue
                
                cve_id = vuln.get('cve_id', 'N/A')
                severity = vuln.get('severity', 'Unknown').upper()
                cvss_score = vuln.get('cvss_score', 'N/A')
                exploitable = "Exploitable" if vuln.get('exploitable', False) else "No known exploit"
                description = vuln.get('description', 'No description available') 
                if description:
                    # Split into words, take first 50, rejoin with spaces, and add ellipsis
                    words = description.split()
                    if len(words) > 50:
                        description = " ".join(words[:50]) + "..."
                # Get row style based on severity
                row_style = {
                    "CRITICAL": "bright_red",
                    "HIGH": "bright_yellow",
                    "MEDIUM": "bright_green",
                    "LOW": "bright_blue"
                }.get(severity, "bright_white")
                
                vuln_table.add_row(cve_id, severity, str(cvss_score), exploitable, description, style=row_style)
            
            console.print(vuln_table)
            console.print("\n")

    @staticmethod
    def _remove_duplicates(data_list: List) -> List:
        """
        Remove duplicate items from a list using a more efficient approach.
        
        Args:
            data_list: List of items to deduplicate
            
        Returns:
            List with duplicates removed
        """
        # Handle empty lists
        if not data_list:
            return []
        
        # Use a set to track seen items (more efficient for larger lists)
        seen = set()
        unique_list = []
        
        for item in data_list:
            # For dictionaries, we need to use a hashable representation
            if isinstance(item, dict):
                # Create a hashable representation using a tuple of sorted items
                item_hash = tuple(sorted((k, str(v)) for k, v in item.items()))
                if item_hash not in seen:
                    seen.add(item_hash)
                    unique_list.append(item)
            # For other types that might be hashable
            else:
                try:
                    if item not in seen:
                        seen.add(item)
                        unique_list.append(item)
                except:
                    # Fallback for unhashable types
                    if item not in unique_list:
                        unique_list.append(item)
        
        return unique_list