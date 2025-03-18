from dosuby.src.interfaces.report_repo import ReportRepo
from dosuby.src.core.domain.enumeration_reporte import EnumerationReporte
from rich.console import Console
from rich.table import Table


class CliReportRepo(ReportRepo):

    def read_report(self):
        report = EnumerationReporte()
        report_subdomains = CliReportRepo.remove_duplicates(
            report.report_subdomains)
        table = Table(title="\nSubdomains Found")
        if not self.config.scanning_modules:
            columns = ["Subdomain", "IP"]
            for col in columns:
                table.add_column(col)

            subdomain: dict
            # print(report_subdomains)
            for subdomain in report_subdomains:
                if not subdomain.get('subdomain_ip'):
                    ip_str = 'N/A'
                else:
                    ip_str = subdomain.get('subdomain_ip')

                row = [
                    subdomain.get('subdomain_uri'),
                    ip_str,
                ]
                table.add_row(*row, style='bright_green')

            console = Console()
            console.print(table)
            return

        columns = ["Subdomain", "IP", "Open Ports", "CMS", "Web Server"]

        for col in columns:
            table.add_column(col)

        for subdomain in report_subdomains:
            if not subdomain.get('subdomain_ip'):
                ip_str = 'N/A'
            else:
                ip_str = subdomain.get('subdomain_ip')

            if not subdomain.get('subdomain_open_ports'):
                open_ports_str = 'N/A'
            else:
                open_ports_str = ", ".join(
                    [str(num) for num in subdomain.get('subdomain_open_ports')])

            if not subdomain.get('subdomian_cms'):
                cms_str = 'N/A'
            else:
                cms_str = subdomain.get('subdomian_cms')

            if not subdomain.get('subdomain_webserver'):
                webserver_str = 'N/A'
            else:
                webserver_str = subdomain.get('subdomain_webserver')

            row = [
                subdomain.get('subdomain_uri'),
                ip_str,
                open_ports_str,
                cms_str,
                webserver_str
            ]

            table.add_row(*row, style='bright_green')

        # for row in rows:
        #     table.add_row(*row,style='bright_green')

        console = Console()
        console.print(table)

    @staticmethod
    def remove_duplicates(data_list):
        unique_list = []
        for item in data_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list
