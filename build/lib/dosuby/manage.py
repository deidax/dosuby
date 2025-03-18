#!./venv/bin/python3

import argparse
import sys
from dosuby.infrastructure.libs.helpers.dosuby_module import DosubyModule


parser = argparse.ArgumentParser(description='Dosuby manager')
action_group = parser.add_mutually_exclusive_group(required=True)
action_group.add_argument('--create', action='store_true', help='to create a new enumeration module')
action_group.add_argument('--list', action='store_true', help='to list enumeration modules')
action_group.add_argument('--delete', action='store_true', help='to delete an enumeration module')
parser.add_argument('--name', help='the name of the enumeration module to create or delete')

args = parser.parse_args()

if args.create and not args.name:
    parser.error('--name is required when --create is specified')
elif not args.list and not args.create and not args.delete:
    parser.error('one of --create, --list, or --delete is required')

if args.create:
    print(f'Creating {args.name} module...')
    enumeration_module = DosubyModule(class_name=args.name)
    enumeration_module.create()
elif args.list:
    print(f'List of enumeration modules')
    DosubyModule.list_modules()
elif args.delete:
    confirmation = input(f'Are you sure you want to delete {args.name} module? (y/N): ')
    if confirmation.lower() == 'y':
        print(f'Deleting {args.name} module...')
        enumeration_module = DosubyModule(class_name=args.name)
        enumeration_module.delete()
    else:
        print("[*] Deletion cancelled")
        sys.exit(0)
