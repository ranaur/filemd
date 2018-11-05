import sys
#import inspect
from pprint import pprint

def metX():
    print("metX")

def metY():
    print("metY")
    pass

x = 1

def main():
    #moduleinfo = inspect.getmembers(sys.modules[__name__])
    moduleinfo = dir(sys.modules[__name__])
    for method in moduleinfo:
        if method.startswith("met"):
            print("Trying to call " + method)
            method_to_call = getattr(sys.modules[__name__], method)
            method_to_call()

if __name__ == '__main__':
    main()
