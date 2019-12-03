import probability

class Problem:

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        
        self.R,self.C,self.S,self.P,self.M=[],[],[],[],[]
        
        f1=fh.readlines()
        
        for i in f1:
            if i[0] == 'R':
                self.R.append(i.rstrip()[2:])
            elif i[0] == 'C':
                self.C.append(i.rstrip()[2:])
            elif i[0] == 'S':
                self.S.append(i.rstrip()[2:])
            elif i[0] == 'P':
                self.P.append(i.rstrip()[2:])
            elif i[0] == 'M':
                self.M.append(i.rstrip()[2:])
        
        print(self.R,self.C,self.S,self.P,self.M)
        
    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        return (room, likelihood)

def solver(input_file):
    return Problem(input_file).solve()

fh = open("P2.txt","r")
p = Problem(fh)
