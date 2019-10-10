import argparse

parser = argparse.ArgumentParser(description='PHP Documentation Generator')
parser.add_argument("-p", required=True, type=str, help="Path to directory being documented")
parser.add_argument("-t", required=True, type=str, help="Path to directory where to store documentation files")

args = parser.parse_args()

if __name__ == '__main__':

    print(args.p)
    print(args.t)