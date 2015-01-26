__author__ = 'Humberto, Gabriela'

from itertools import chain, combinations
from DBNormalizer.model.FDependencyList import *


def find_fds_rhs(lhs, rhs, db_partition):
    """
    Finds all the minimal functional dependencies X->rhs with X subset of lhs. Usually lhs = U\rhs where U is the
    set of attributes in the relation. The idea of this function is to eliminate unnecessary computation using the
    fact that, if the fd X->E does not hold, then for all Y subset of X, Y->E doesn't hold either.

    db_partition doesn't play an important role in this function, it is passed to the function test_fd_db that
    determines if a given fd is satisfied by the data in db_partition.

    :param lhs: a list containing attributes in the lhs of a fd
    :param rhs: a list containing attributes in the rhs of a fd
    :param db_partition: a partition of a relation in SQL over which the dependencies are to be tested
    :return: a list with the minimal lhs that satisfy lhs->rhs
    """
    x = {tuple(lhs)}
    e0 = set()  # set with the non-satisfied fds
    e1 = set()  # set with the satisfied fds
    set_len = lhs.__len__()
    while x.__len__() != 0:
        level = set()   # each level tries the proper subsets of X with length len(X)-1
        for subx in x:
            #TODO Change this function that is for testing purposes only for the real one
            if not test_fds(list(subx), rhs, db_partition):
                e0 = e0.union([subx])
            else:
                e1 = set(remove_super_sets(list(subx), e1))  # removes redundancy in e1
                e1 = e1.union([subx])
                level = level.union([subx])

        level = set(subsets(list(level), set_len-1))   # obtain the next level
        e0 = set(subsets(list(e0), set_len-1))
        x = prune(level, e0)  # removes the cases that are not satisfiable by means of e0
        set_len -= 1
    return [list(x) for x in list(e1)]


def subsets(x, k):
    """
    Finds the subsets of cardinality k for each element (set) of the list x
    :param x: a list of sets
    :param k: integer
    :return: list of subsets
    """
    sub_set = set()
    for i in x:
        sub_set = sub_set.union(set(combinations(i, k)))
    return list(sub_set)


def prune(x, y):
    """
    Set difference
    :param x:
    :param y:
    :return:
    """
    return x - y


def test_fds(lhs, rhs, fds):
    """
    Tests if the fds lhs->rhs is satisfied in fds. This function is only for testing purposes
    :param lhs:
    :param rhs:
    :param fds:
    :return: boolean
    """
    closure = fds.attribute_closure(lhs)
    return rhs[0] in closure


def remove_super_sets(sub_set, set_of_sets):
    """
    Removes the elements in set_of_sets that are super sets of sub_set
    :param sub_set: a set
    :param set_of_sets: list of sets
    :return: list of sets
    """
    return [x for x in set_of_sets if not set(x).issuperset(set(sub_set))]
