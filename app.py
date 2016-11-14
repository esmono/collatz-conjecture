import argparse
from collatz import CollatzConjecture

parser = argparse.ArgumentParser()
parser.add_argument("number", type=int, help="Number to be tested")
parser.add_argument("-g", "--graph",
                    help="Save the data to a graph database",
                    action="store_true")
parser.add_argument("-c", "--complex",
                    help="Number will be tested for all the paths to 1",
                    action="store_true")
args = parser.parse_args()


collatz = CollatzConjecture(args.number, args.complex)
collatz.calculate()

if args.graph:
    collatz.save_graph()
else:
    print(collatz.get_result())
