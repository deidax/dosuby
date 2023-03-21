import shutil
import os

"""This will create a new enumeration module object
"""
class DosubyModule:


    def __init__(self,class_name: str):
        self.class_name = class_name.lower()
        self.USE_CASE_TEMPLATE = "src/utils/module_template/use_case/template.txt"
        self.USE_CASE_PATH = "src/core/application/use_cases/"
        
        self.STRATEGY_TEMPLATE = "src/utils/module_template/strategy/cli/template.txt"
        self.STRATEGY_PATH = f"src/core/application/strategies/{class_name}/cli/"
        
        self.ADAPTER_TEMPLATE = "src/utils/module_template/adapter/template.txt"
        self.ADAPTER_PATH = f"src/adapter/{class_name}/"
        
        self.HANDLER_TEMPLATE = "src/utils/module_template/handlers/cli/template.txt"
        self.HANDLER_PATH = f"src/handlers/cli/"
        
        self.SERVICE_TEMPLATE = "src/utils/module_template/services/cli/template.txt"
        self.SERVICE_PATH = f"src/services/{class_name}/cli/"
    
    def create(self):
        # read class name
        class_name = self.class_name

        if not class_name.isalpha():
            print(f"[x] Invalid class name '{class_name}'")
            return False

        # Start by creating a new UseCase
        with open(self.USE_CASE_TEMPLATE, 'r') as f:
            use_case_template = f.read()
            
        with open(self.STRATEGY_TEMPLATE, 'r') as f:
            strategy_template = f.read()
        
        with open(self.ADAPTER_TEMPLATE, 'r') as f:
            adapter_template = f.read()
            
        with open(self.HANDLER_TEMPLATE, 'r') as f:
            handler_template = f.read()
        
        with open(self.SERVICE_TEMPLATE, 'r') as f:
            service_template = f.read()


        # Replace the class name with the provided argument
        use_case = use_case_template.replace("{{class}}", class_name)\
                                    .replace("{{Class}}", class_name.capitalize())
                                    
        strategy = strategy_template.replace("{{class}}", class_name)\
                                .replace("{{Class}}", class_name.capitalize())
        
        adapter = adapter_template.replace("{{class}}", class_name)\
                                .replace("{{Class}}", class_name.capitalize())

        handler = handler_template.replace("{{class}}", class_name)\
                            .replace("{{Class}}", class_name.capitalize())
        
        service = service_template.replace("{{class}}", class_name)\
                            .replace("{{Class}}", class_name.capitalize())

        # Write the resulting use_case to a new file
        path = f'{self.USE_CASE_PATH}{class_name}_enumeration_use_case.py'
        with open(path, 'w') as f:
            f.write(use_case)
            print(f"[+] Creating '{path}' -> UseCase")
            
        # creating the strategy
        # Create the directory path if it does not exist
        os.makedirs(os.path.dirname(self.STRATEGY_PATH), exist_ok=True)
        # Write the resulting strategy to a new file
        path = f'{self.STRATEGY_PATH}{class_name}_cli_enumeration_strategy.py'
        with open(path, 'w') as f:
            f.write(strategy)
            print(f"[+] Creating '{path}' -> Strategy")
            self.create_init(self.STRATEGY_PATH.replace('/cli/','/'))

        os.makedirs(os.path.dirname(self.ADAPTER_PATH), exist_ok=True)
        path = f'{self.ADAPTER_PATH}{class_name}_adapter.py'
        with open(path, 'w') as f:
            f.write(adapter)
            print(f"[+] Creating '{path}' -> Adapter")
            self.create_init(self.ADAPTER_PATH)
        
        os.makedirs(os.path.dirname(self.SERVICE_PATH), exist_ok=True)
        # Write the resulting service to a new file
        path = f'{self.SERVICE_PATH}{class_name}_cli_service.py'
        with open(path, 'w') as f:
            f.write(service)
            print(f"[+] Creating '{path}' -> Service")
            self.create_init(self.SERVICE_PATH.replace('/cli/','/'))
        
        os.makedirs(os.path.dirname(self.HANDLER_PATH), exist_ok=True)
        path = f'{self.HANDLER_PATH}{class_name}_handler.py'
        with open(path, 'w') as f:
            f.write(handler)
            print(f"[+] Creating '{path}' -> Handler")

    def create_init(self, path: str):
        with open(f"{path}__init__.py", 'w') as f:
            f.write('')
    
    
    def delete(self):
        
        try:
            use_case_path = f'{self.USE_CASE_PATH}{self.class_name}_enumeration_use_case.py'
            strategy_path = f'src/core/application/strategies/{self.class_name}/'
            adapter_path = self.ADAPTER_PATH
            handler_path = f'{self.HANDLER_PATH}{self.class_name}_handler.py'
            service_path = f'src/services/{self.class_name}/'

            os.remove(use_case_path)
            print(f"[-] {use_case_path} -> Use case removed")
            
            shutil.rmtree(strategy_path)
            print(f"[-] {strategy_path} -> Strategy removed")
            
            shutil.rmtree(adapter_path)
            print(f"[-] {adapter_path} -> Adapter removed")
            
            os.remove(handler_path)
            print(f"[-] {handler_path} -> Handler removed")
            
            shutil.rmtree(service_path)
            print(f"[-] {service_path} -> Service removed")
            
        except Exception as e:
            print("[x] Error: {e}".format(e=e))
            print(f"[!] Probably the module '{self.class_name}' doesn't exist")
    
    
    @staticmethod
    def list_modules():
        path = 'src/handlers/cli/'
        files = os.listdir(path)
        i = 0
        for file in files:
            file = file.replace('_handler.py','')
            if file not in ['__init__.py', '__pycache__', 'handler_cli.py']:
                i = i + 1
                print(f"-> {file}")
                
        print(f"[Total: {i}]")