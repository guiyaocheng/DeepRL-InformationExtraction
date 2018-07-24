# -*-coding:utf-8-*-


####
# arguments
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument('--run', type=int, default=10, help='number of runs')
# parser.add_argument('--epoch', type=int, default=500, help='number of epochs in this run')
# parser.add_argument('--lrate', type=float, default=0.001, help='learning rate')
# parser.add_argument('--epsilon', type=float, default=0.01, help='rate for epsilon-greedy')
# parser.add_argument('--train_files', type=str, default=[], help='list of training files', nargs='+')
# parser.add_argument('--test_files', type=str, default=[], help='list of testing files', nargs='+')
# parser.add_argument('--loss', choices=['log', 'cross_entropy', 'square_error', 'minus_log'], default='log', help='the option of loss types')
# parser.add_argument('--policy', choices=['onpolicy', 'offpolicy', 'onsample'], default='onsample', help='the option of policies')
# parser.add_argument('--work_dir', type=str, default='F:/work', help='the dir for log files and models')
# parser.add_argument('--feat_limit', type=int, default=10000, help='the limit size of features')
# parser.add_argument('--batch_size', type=int, default=50, help='the batch size')
# parser.add_argument('--rewards', type=float, default=[1.0,-1.0,0.1], help='the specified rewards', nargs='+')
# parser.add_argument('--alpha', type=float, default=0.1, help='the weight of updates')
# parser.add_argument('--mem_size', type=int, default=10, help='the size of memory')
# parser.add_argument('--action_space_in', type=str, default=None, help='the input file of action space')
# parser.add_argument('--error_rate', type=float, default=0.8, help='the error rate for analytic dataset')
# parser.add_argument('--fold', type=int, default=1, help='the fold for analytic dataset')
args = parser.parse_args()

