import argparse
import html_generator as hm

parser = argparse.ArgumentParser(description='PHP Documentation Generator')
parser.add_argument("-p", required=False, type=str, help="Path to directory being documented")
parser.add_argument("-t", required=False, type=str, help="Path to directory where to store documentation files")

args = parser.parse_args()

if __name__ == '__main__':

    hm.__gen__(r'D:\recFolder')