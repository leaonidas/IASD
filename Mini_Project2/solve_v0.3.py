import probability

class Problem:

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        
        self.vars,self.R,self.C,self.S,self.P,self.M=[],[],[],[],[],[]
        
        f1=fh.readlines()
        
        #sensors=[]
        edges=[]
        node_specs=[]
        parents={}
        T='True'
        F='False'
        
        for i in f1:
            if i[0] == 'R':
                self.R=i.rstrip()[2:].split()
                for j in self.R:
                    self.vars.append(j)
            elif i[0] == 'C':
                self.C=i.rstrip()[2:].split()
            elif i[0] == 'S':
                self.S=i.rstrip()[2:].split()
            elif i[0] == 'P':
                self.P.append(i.rstrip()[2:])
            elif i[0] == 'M':
                self.M.append(i.rstrip()[2:])
        
        for i in self.C:
            edges.append(i.split(','))
        
        #creates node_specs vector for root nodes and template parents dictionary (will serve the purpose of building the remaining node_specs vector)
        for i in self.vars:
             parents[i]=[i]
             for j in edges:
                for k in j:
                     if k==i:
                         a=[x for x in j if x != k]
                         parents[i].append(''.join(a))
             if i not in node_specs:
                 node_specs.append((i,'',{T:0.5, F:0.5}))
        
        parentes={}
        
        #creates the remaining node_specs vector for BayesNet excluding evidence nodes (sensors)
        for j in range(len(self.M)):
            for i in self.vars:
            
                if j==1:
                    node_specs.append((i+'_t+1', ' '.join(parents[i]),{T:0.5, F:0.5}))
                if j>1:
                    parentes=[]
                    for k in parents[i]:
                        parentes.append(k+'_t+'+str(j-1))
                    node_specs.append((i+'_t+'+str(j), ' '.join(parentes), {T:0.5,F:0.5}))
        
        #creates evidence nodes node_specs remaining for the BayesNet            
        for i in self.S:
            temp=i.split(':')
            for j in range(len(self.M)):
                if temp[0] in self.M[j]:
                    if j==0 :
                        node_specs.append((temp[0],temp[1],{T:0.5,F:0.5}))
                    if j>=1:
                        node_specs.append((temp[0]+'_t+'+str(j),temp[1]+'_t+'+str(j),{T:0.5,F:0.5}))
        print(node_specs)
    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        return (room, likelihood)

def solver(input_file):
    return Problem(input_file).solve()

fh = open("P1.txt","r")
p = Problem(fh)