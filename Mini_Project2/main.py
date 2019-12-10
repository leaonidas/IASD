import probability

class Problem:

    def __init__(self, fh):
        # Place here your code to load problem from opened file object fh
        # and use probability.BayesNet() to create the Bayesian network
        
        self.BN,self.vars,self.R,self.C,self.S,self.P,self.M=[],[],[],[],[],[],[]
        
        f1=fh.readlines()
        
        edges=[]
        node_specs=[]
        parents={}
        T=True
        F=False
        
        
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
                 node_specs.append((i,'',0.5))
        
        parentes={}

        
        #Creates dict with ammount of parents per variable (useful for cpt tables creation)
        prnt_num={}
        tm=0
        for i in parents:
            prnt_num.update({i : len(parents[i]) })
            tm=max(prnt_num[i],tm)
        
     
             
        #Generates different size tables for cpt
        tt=[]
        table={}
        for i in range(tm):
            if i==0:
                table[i+1]={T:1,F:0}
            else:
                for j in range(2**(i+1)):
                
                    booltuple=tuple(list(map(bool,list(map(int,list(format(j, '#0'+str(i+1+2)+'b').split('b')[1]))))))
                    power=sum(list(map(int,booltuple[1:len(booltuple)])))
                    
                    prob=1-(1-float(''.join(self.P)))**(power)
                    if booltuple[0]:
                        tt={booltuple:1}
                    else:
                        tt={booltuple: prob}
                    
                    if (i+1) not in table.keys():
                        table[i+1]= tt
                    else:
                        table[i+1].update(tt)
                
        #creates the node_specs vector for BayesNet excluding evidence nodes (sensors)
        for j in range(len(self.M)):
            for i in self.vars:
                if j==1:
                    node_specs.append((i+'_t+1', ' '.join(parents[i]),table[prnt_num[i]]))
                if j>1:
                    parentes=[]
                    for k in parents[i]:
                        parentes.append(k+'_t+'+str(j-1))
                    node_specs.append((i+'_t+'+str(j), ' '.join(parentes), table[prnt_num[i]]))
        
        
        # Sensor: True | Variable: True - TPR
        # Sensor: True | Variable: False - FPR
        # Sensor: False | Variable: True - FNR
        # Sensor: False | Variable: False - TNR
        
        # P(S01=T|parent=T) =TPR (given)
        # P(S01=T|parent=F) = FPR (given)
        
        #creates evidence nodes node_specs remaining for the BayesNet            
        for i in self.S:
            temp=i.split(':')
            TPR=float(temp[2])
            FPR=float(temp[3])
            for j in range(len(self.M)):
                if temp[0] in self.M[j]:
                    if j==0 :
                        node_specs.append((temp[0],temp[1],{T:TPR,F:FPR}))
                    if j>=1:
                        node_specs.append((temp[0]+'_t+'+str(j),temp[1]+'_t+'+str(j),{T:TPR,F:FPR}))
        
        #build BayesNet        
        self.BN=probability.BayesNet(node_specs)
    
    def solve(self):
        # Place here your code to determine the maximum likelihood solution
        # returning the solution room name and likelihood
        # use probability.elimination_ask() to perform probabilistic inference
        #Run elimination and print results
        T=True
        F=False
        results={}
        a=[]
        c=[]
        evidence=[]
        it=0
        for j in self.M:
            if it==0:
                b=''.join(j)
                c.append(b)
            else:
                f=j.split(' ')
                #print(f)
                for k in f:
                    h=k.split(':')[0]+'_t+'+str(it)+':'+k.split(':')[1]
                    c.append(h)
            it=it+1
            d=' '.join(c)
            a=d.split(' ')
        
        paird={}
        for i in a:
            s=i.split(':')
            if s[1]=='T':
                paird[s[0]]=T
            if s[1]=='F':
                paird[s[0]]=F
        evidence=dict(paird)

        for i in self.vars:
            #print(i)
            if len(self.M)>1:
                results.update({i+'_t+'+str(len(self.M)-1):probability.elimination_ask(i+'_t+'+str(len(self.M)-1),evidence,self.BN).show_approx()})
            else:
                 results.update({i:probability.elimination_ask(i,evidence,self.BN).show_approx()})
        trues={}
        ml=0
        for i in results:
            
            trues[i]=(results[i].split(',')[1].split(':')[1])
            if float(trues[i])>ml:
                 maxtuple=(i,trues[i])
            ml=max(ml,float(trues[i]))
         
                
        room=maxtuple[0].split('_t')[0]
        likelihood=float(maxtuple[1])
        
        return (room, likelihood)

def solver(input_file):
    return Problem(input_file).solve()