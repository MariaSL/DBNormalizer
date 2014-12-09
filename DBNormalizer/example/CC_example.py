__author__ = 'mariaslanova'

from mincover import *

# fd1 = FDependency(['A','B','C','D'],['E'])
# fd2 = FDependency(['A','B'],['E'])
# fd3 = FDependency(['B','C'],['E'])
fd1 = FDependency(['A', 'B'], ['C', 'D'])
fd2 = FDependency(['C'], ['A','D','E'])
fd3 = FDependency(['B'], ['D','E'])
fd4 = FDependency(['D'], ['E'])
fdlist = FDependencyList([fd1, fd2, fd3, fd4])

print(makeRightsingleton(fdlist))
print(removeExtraneous(makeRightsingleton(fdlist)))
print(removeDuplicacy(removeExtraneous(makeRightsingleton(fdlist))))