import pickle, os
from pprint import pprint
from matplotlib import pyplot as plt


def import_data(file):
    return pickle.load(open(f"results/{file}", "rb"))


def main():
    
    bruteforce_results = import_data("results_complete_bruteforce_fixed.pickle")
    greedy_results = import_data("results_complete_greedy_fixed.pickle")



    

if __name__ == "__main__":
    main()