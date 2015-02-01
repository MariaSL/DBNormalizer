__author__ = 'Paris: Maria, Bishnu, Harsha'

from itertools import combinations
from DBNormalizer.model.mincover import *
from DBNormalizer.model.FDependencyList import *

class Normalization:
    """
    This class contains the methods to achieve Normalization
    """

    def __init__(self):
        """
        Constructor Inializes FDList1NF,FDList3NF,FDListBCNF,FDListNoNF that
		represents the functional dependencies that violate the corresponding Normal Form
        :return:
        """
        self.FDList2NF=FDependencyList()
        self.FDList3NF=FDependencyList()
        self.FDListBCNF=FDependencyList()
        self.FDListNoNF=FDependencyList()

    def isKey(self,lhs, candKeys):
        """
        Check is param lhs is a candidate key
        :param lhs: list
        :param candKeys: list of set of candidate Keys
        :return boolean: if lhs is key else return false:
        """
        key = False
        if (candKeys.__contains__(lhs)):
            key = True
        return key

    
    def isSingleton(self,rhs):
        """
        Check if param rhs is singleton
        :param rhs: list/set
        :return: True if singleton false otherwise
        """

        singleTon = False
        l =rhs.__len__()
        if (l == 1):
            singleTon = True
        return singleTon


    
    def isNonPrime(self,attr, candKeys):
        """
        check if attr is a non prime attribute
        :param attr: Attribute of a realtion
        :param candKeys:list of Candidate Keys
        :return: True of non Prime else false.
        """
        prime = False
        for key in candKeys:
            if (key.__contains__(attr)):
                Prime = True
                break
        return not prime


    
    def isProperSubset(self,lhs, key):
        """
        check if lhs is proper subset of key
        :param lhs: set of left attribute of a FD
        :param key: Set representing a  candidate key
        :return: True if lhs is proper subset of key else False.
        """
        propersubset = False
        if (lhs.issubset(key) and not key.issubset(lhs)):
            propersubset = True
        return propersubset


    
    def findNonEmptySubsets(self,S):
        """
        Find the non empty subset of S
        """

        subs = [set(j) for i in range(len(S)) for j in list(combinations(S, i + 1))]
        return subs


    
    def getLnRSet(self,minFDs):
        """
        Compute all the attributes that apears in left and right and store them into two seperate List
        :param minFDs: Minimal Cover of A relation
        :return: list of set of left and right attributes e.g. [{lhs attributes}{right attributes}]
        """
        LRset = list()
        L = []
        R = []
        for fd in minFDs:
            L.extend(fd.lh)
            R.extend(fd.rh)
        LRset.append(set(L))
        LRset.append(set(R))
        return LRset


    #R={all the attributes}
    #S=[{LHSs},{RHSs}]
    #necessary is the necessary attributes
    def getNecessaryAttribute(self,R, minFDs):
        """
        ompute the Necessary attribute
        :param R: Attribute Set of the relation
        :param minFDs: Minimal Cover of the relation R
        :return: Set of attributes that apears only at left hand side of the FDs, but never in right
        """
        S = Normalization.getLnRSet(self,minFDs)
        necessary = R.difference(S[0].union(S[1]))
        necessary = necessary.union(S[0].difference(S[1]))
        return necessary


    #R={all the attributes}
    #S=[{LHSs},{RHSs}]
    #useless is the useless attributes
    def getUseLessAttribute(self,R, minFDs):
        """
        Compute the Useless attribute
        :param R: Attribute Set of the relation
        :param minFDs: Minimal Cover of the relation R
        :return: Set of attributes that apears only at right hand side of the FDs, but never in left
        """

        S = Normalization.getLnRSet(self,minFDs)
        useless = S[1].difference(S[0])
        return useless


    
    def getUsefulAttribute(self,R, X, Y):
        """
        Compute the Necessary attribute
        :param R: Attribute Set of the relation
        :param X: et of Necessary attributes
        :param Y: set of useless attributes
        :return: Set of attributes that apears  at left hand side of the FDs,and also  at right
        """
        M = R.difference(X.union(Y))
        return M


    
    def addedL(self,L, X):
        """
        Add X to the all the element of L
        :param L: list of Set of attributes
        :param X: set of attributes
        :return: list of set of attributes after adding X to all the elements of L
        """
        L1 = list()
        for Z in L:
            L1.append(Z.union(X))
        return L1


    
    def findCandKeys(self,R, minFDs,FDs):
        """

        Compute all the candidate Keys of A relation with Attribute Set R and Minimal Cover minFDs
		param R: set of attributes of a relation.
		param minFDs: Minimal Cover of the relation
		param FDs: Also Minimal Cover of the relation
		return list: list of set of candidate keys
        """

        candKeys = list()
        X = self.getNecessaryAttribute(R, minFDs)
        #print(X)
        Y = self.getUseLessAttribute(R, minFDs)
        #print(Y)
        M = self.getUsefulAttribute(R,X, Y)
        #print(M)
        L = self.findNonEmptySubsets(M)
        if(X!=set()):
            xclosure =set(FDs.attribute_closure(X))
            #print(xclosure)
            if (xclosure == R):
                #print("True")
                candKeys.append(X)
                #print(candKeys)
            else:
                L = self.addedL(L, X)


        
        while L != []:
            #i = i + 1
            Z = L[0]
            del L[0]
            zclosure = set(FDs.attribute_closure(Z))
            if (zclosure == R):
                candKeys.append(Z)
                L=self.removeSuperSet(Z, L)
        return candKeys


    def removeSuperSet(self,Z, L):
        """

        Remove the super set of Z from L
		param Z: set for which super set to be removed
		param L: list of set from which superset of Z to be removed
		return list: list of after doing removing
        """

        L1 = L.copy()
        for l in L1:
            if (Z.issubset(l)):
                L.remove(l)
        return L


    def findClosure(Fds,attr):

        closure=Fds.attribute_closure(attr)
        return set(closure)


    #keys=[set(l) for l in allKeys]
    #print(keys)
    #violation2nf variable keeps the state of violation [true or false]
    #isSigleton(fd) checks if given fd is singleton (rightside with single attribute)
    #candKeys is list of candidate Keys computed beforehand
    #isProperSubset(lhs, key) checks if lhs is a proper subset of key.
    #nonPrime(rhs) checks if rhs is a non Prime attribute
    def check2NF(self,fd, lhs, rhs, candKeys):
        """

        check for 2NF violation and keep the violated FD in FDList2NF
		param fd: Depenency of the relation that is to be tested for violation
		param lhs: list ,left attributes of fd
		param rhs: list ,right attributes of fd
		param candKeys: list of set of candidate Keys
		reutrn boolean: true violates 2NF conditions false otherwise
        """

        violation2NF = False
        if (self.isSingleton(rhs)):
            for key in candKeys:
                if (self.isProperSubset(lhs, key)):
                    if (self.isNonPrime(rhs,candKeys)):
                        violation2NF = True
                        self.FDList2NF.append(fd)
                        break
        return violation2NF


    #iskey(lhs,candKeys) test if lhs is key
    #toAttributeList(rhs) get the all the attributes in right Hand side as a List
    def check3NF(self,fd, lhs, rhs, candKeys):
        """

        check for 3NF violation and keep the violated FD in FDList3NF
		param fd: Depenency of the relation that is to be tested for violation
		param lhs: list ,left attributes of fd
		param rhs: list ,right attributes of fd
		param candKeys: list of set of candidate Keys
		reutrn boolean: true violates 3NF conditions false otherwise
        """

        violation3NF = False
        if (self.isKey(lhs, candKeys)):
            violation3NF = False
        else:
            for attr in rhs:
                if (self.isNonPrime(attr, candKeys)):
                    violation3NF = True
                    self.FDList3NF.append(fd)
                    break
        return violation3NF


    
    def checkBCNF(self,fd, lhs, rhs, candKeys):
        """
     	check for BCNF violation and keep the violated FD in FDListBCNF
		param fd: Depenency of the relation that is to be tested for violation
		param lhs: list ,left attributes of fd
		param rhs: list ,right attributes of fd
		param candKeys: list of set of candidate Keys
		reutrn boolean: true violates BCNF conditions false otherwise
        """
        violationBCNF = False
        if (not self.isKey(lhs, candKeys)):
            violationBCNF = True
            self.FDListBCNF.append(fd)
        return violationBCNF

