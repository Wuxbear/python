import sys

def main():
 
    while True:
        try:
            x = int(input("input which thread to run:"))
            print(x)
            if x == 999:
                break
        except:
            print("error: ", sys.exc_info())

if __name__ == '__main__':
    main()

