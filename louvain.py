from community_detection import *
import argparse


if __name__ == '__main__':
    
    
    parser = argparse.ArgumentParser(
        description='Script for performing Louvain Community Detection on a complete graph'
    )
    
    parser.add_argument('--cities-list', required= True, type= str, nargs='+')
    parser.add_argument('--distance-cutoff ',required= False, type= int)
    args = parser.parse_args()

    print(args._get_kwargs())