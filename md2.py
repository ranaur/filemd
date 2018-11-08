#!/usr/bin/env python
import argparse
import builtins

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line metadata editor')
    builtins.subparsers = parser.add_subparsers()
    import commands
    parser.add_argument("--driver", nargs="?", default='DriverRemoraYAML', help='name of the driver')

    args = parser.parse_args()

    import inspect
    if (hasattr(args, 'func') and inspect.isfunction(args.func)):
        try:
            exit(args.func(args))
        except Exception as e:
            print(("error: " + e.__class__.__name__ + " " + str(e)).rstrip())
            exit(1)
    else:
        parser.print_help()


