import argparse
from infrastructure.libs.helpers.dosuby_module import DosubyModule

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('action', choices=['create', 'delete'], help='the action to perform\ncreate: to create a new enumeration module.\ndelete: to delete an enumeration module')
parser.add_argument('name', help='the name of the enumeration module to create or delete')

args = parser.parse_args()

if args.action == 'create':
    print(f'Creating {args.name} module...')
    enumeration_module = DosubyModule(class_name=args.name)
    enumeration_module.create()
elif args.action == 'delete':
    print(f'Deleting {args.name}...')
    # code to delete item