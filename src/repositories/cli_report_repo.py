from src.interfaces.report_repo import ReportRepo
from src.core.domain.enumeration_reporte import EnumerationReporte

class CliReportRepo(ReportRepo):
    
    
    def read_report(self):
        report = EnumerationReporte()
        return report.report_subdomains