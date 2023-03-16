import sys
import os

"""This will create a new enumeration module object
"""

def main():
    # read class name
    class_name = sys.argv[1]

    if not class_name.isalpha():
        print(f"[x] Invalid class name '{class_name}'")
        return False

    class_name = class_name.lower()


    USE_CASE_TEMPLATE = "src/utils/module_template/use_case/template.txt"
    USE_CASE_PATH = "src/core/application/use_cases/"
    
    STRATEGY_TEMPLATE = "src/utils/module_template/strategy/cli/template.txt"
    STRATEGY_PATH = f"src/core/application/strategies/{class_name}/cli/"

    # Start by creating a new UseCase
    with open(USE_CASE_TEMPLATE, 'r') as f:
        use_case_template = f.read()
        
    with open(STRATEGY_TEMPLATE, 'r') as f:
        strategy_template = f.read()


    # Replace the class name with the provided argument
    use_case = use_case_template.replace("{{class}}", class_name)\
                                .replace("{{Class}}", class_name.capitalize())
                                
    strategy = strategy_template.replace("{{class}}", class_name)\
                            .replace("{{Class}}", class_name.capitalize())

    # Write the resulting use_case to a new file
    path = f'{USE_CASE_PATH}{class_name}_enumeration_use_case.py'
    with open(path, 'w') as f:
        f.write(use_case)
        print(f"[+] Creating '{path}' -> UseCase")
        
    # creating the strategy
    # Create the directory path if it does not exist
    os.makedirs(os.path.dirname(STRATEGY_PATH), exist_ok=True)
    # Write the resulting strategy to a new file
    path = f'{STRATEGY_PATH}{class_name}_cli_enumeration_strategy.py'
    with open(path, 'w') as f:
        f.write(strategy)
        print(f"[+] Creating '{path}' -> Strategy")
        create_init(STRATEGY_PATH.replace('/cli/','/'))


def create_init(path: str):
    with open(f"{path}__init__.py", 'w') as f:
        f.write('')
    

if __name__ == "__main__":
    main()