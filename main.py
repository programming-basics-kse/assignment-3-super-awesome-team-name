import argparse

def get_args() -> dict:
    parser = argparse.ArgumentParser("Sample Program")
    parser.add_argument("filepath", type=str, help="Path to the file")
    parser.add_argument("-medals", action="store_true", required=True, help="Required argument")
    parser.add_argument("team",type=str, nargs="+", help="Name of the team")
    parser.add_argument("year", type=int, help="Year of the olympics")
    parser.add_argument("-output", "--output", type=str, help="Name of the output file")
    args = vars(parser.parse_args())
    return args

print(get_args())