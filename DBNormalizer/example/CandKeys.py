__author__ = 'mariaslanova'

from DBNormalizer.model.Normalization import *


N=Normalization()

RO=set(['A','B','C','D','E'])

fd1 = FDependency(['A', 'B'], ['C','D'])
fd2 = FDependency(['A'], ['B'])
fd3 = FDependency(['B'], ['C'])
fd4 = FDependency(['C'], ['E'])
fd5 = FDependency(['B', 'D'], ['A'])


FDs = FDependencyList([fd1, fd2, fd3, fd4,fd5])
minFds=FDs.MinimalCover()

L=N.findCandKeys(RO,minFds,FDs)
print('Candidate keys =',L)