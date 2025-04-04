from abc import ABC, abstractmethod
import signal
import sys
import os
from dosuby.src.interfaces.enumeration_handler import EnumerationHandler
from dosuby.src.interfaces.handler import Handler
from dosuby.src.interfaces.success_response import SuccessResponse
from dosuby.src.core.application.response.cli.failed_response_builder import FailureResponseBuilder
from dosuby.src.core.domain.cache import Cache
from dosuby.src.core.domain.enumeration_reporte import EnumerationReporte
from dosuby.src.repositories.cli_report_repo import CliReportRepo


class InterruptibleHandler(Handler):
    """
    Enhanced Handler that supports graceful interruption during the enumeration process.
    Allows safe termination while preserving and displaying collected results.
    """
    
    # Class variable to track if interrupt was received
    _interrupt_received = False
    
    @classmethod
    def setup_interrupt_handling(cls):
        """
        Set up the interrupt handler at the class level.
        Should be called once at the beginning of the enumeration process.
        """
        def interrupt_handler(sig, frame):
            """
            Signal handler for keyboard interrupts.
            Sets the interrupt flag instead of immediately exiting.
            """
            cls._interrupt_received = True
            print("\n\n" + "-" * 60)
            print("🛑 Interrupt received. Preparing to exit gracefully...")
            print("Please wait while current operations complete...")
            print("-" * 60)
            
        # Register the interrupt handler
        signal.signal(signal.SIGINT, interrupt_handler)
    
    @classmethod
    def check_for_interrupt(cls):
        """
        Check if an interrupt has been received and display results before exiting.
        
        Returns:
            bool: True if interrupt was received, False otherwise
        """
        if cls._interrupt_received:
            print("\n\n" + "-" * 60)
            print("🛑 Exiting due to user interrupt.")
            print("-" * 60)
            
            # Display results collected so far
            try:
                report_singleton = EnumerationReporte()
                
                if report_singleton.report_subdomains:
                    print("\n📊 Showing results collected so far:")
                    report = CliReportRepo()
                    report.read_report()
                else:
                    print("\nNo results collected yet.")
            except Exception as e:
                print(f"Could not display report: {str(e)}")
            
            print("\nExiting immediately...")
            # Force immediate exit
            os._exit(0)
            
        return False
    
    def __init__(self, next_handler: EnumerationHandler=None) -> None:
        super().__init__(next_handler)
        self.cache = Cache()

    def handle(self, uri: str, success_response: SuccessResponse=SuccessResponse()):
        """
        Enhanced handle method that checks for interrupts during execution.
        
        Args:
            uri (str): domain target to handle
            success_response (SuccessResponse): success response (will be passed to the next handler)

        Returns:
            Handler: Next handler or response
        """
        try:
            # Check for interrupt before processing
            InterruptibleHandler.check_for_interrupt()
            
            # Process to put before the handler
            self.pre_handler_process()
            
            # Run the handler process
            result = self._handler_process(uri=uri, success_response=success_response)
            
            # Check for interrupt after processing
            InterruptibleHandler.check_for_interrupt()
            
            return result
            
        except Exception as ex:
            failed_response = FailureResponseBuilder().build_system_error(ex)
            return failed_response.get_response()
    
    def _handler_process(self, uri: str, success_response: SuccessResponse):
        """
        Enhanced handler process that periodically checks for interrupts.
        
        Args:
            uri (str): domain target to handle
            success_response (SuccessResponse): success response
            
        Returns:
            The result of handler processing
        """
        self.cache.cached_enumeration_result_count = 0
        
        # Run the service with interrupt checking
        service_response = self.run_service(uri=uri, success_response=success_response)
        
        # Check for interrupt after service run
        InterruptibleHandler.check_for_interrupt()
        
        if type(service_response) is SuccessResponse and self._next_handler:
            return self._next_handler.handle(uri, service_response)
        
        return service_response