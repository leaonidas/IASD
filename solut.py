# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:48:32 2019

@author: Fernando
"""

import search


class ASARProblem(search.Problem):

    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self,state =[],initial = []):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        f = open("simple2.txt","r")
        [airports, planes, legs, rot_times] = self.load(f)
        self.initial = initial
        #self.build_graph(legs)
        self.state_initial = initial
        self.legs = legs
        self.airports = airports
        self.planes = planes
        self.rot_times = rot_times
        self.path = []
        
    
    def legs_restantes(self,state):        
        legs_rest,i = [],0
        for j in self.legs:
            if int(state[1][i]) == 1: legs_rest.append(j)
            i+=1
        return legs_rest             
    
    def actions(self, state):
        state = [list(state[0]),list(state[1])]
        possible_actions=[]      
        for i in self.legs_restantes(state):
            for j in range (self.dif_planes()):
                if i.split()[0] == state[0][3*j+3].split()[0] and self.horario_possivel(state,i,j):                    
                    possible_actions.append(i.split()[0]+' '+i.split()[1]+' '+i.split()[2]+' '+i.split()[3+2*j]+' '+i.split()[4+2*j])
        return possible_actions
        
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
    
    def horario_possivel(self,state,leg,aviao):
        for i in self.airports:
            if (leg.split()[0] == i.split()[0]) and (int(i.split()[2]) > (int(state[0][4+3*aviao])+int(leg.split()[2]))): 
                return True
        return False

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        
        #print (action)   
        state = [list(state[0]),list(state[1])]
        indice = 0
        for k in self.legs:
            if k.split()[0] == action.split()[0] and k.split()[1] == action.split()[1]: 
                state[1][indice] = '0'
            indice += 1
        state[0][0] = str(int(state[0][0]) - 1)
        state[0][1] = str(int(state[0][1]) + int(action.split()[4]))
        i,l,percorreu = 0,0,1
        for j in self.planes: 
            if j.split()[1] == action.split()[3] and percorreu:
                percorreu = 0
                state[0][3+3*i] = action.split()[1]
                state[0][4+3*i] = self.somar_horarios(int(state[0][4+3*i]),int(action.split()[2]))
                if self.rot_times[l].split()[0] != self.planes[i].split()[1]: l+=1
                state[0][4+3*i] = str(self.somar_horarios(int(state[0][4+3*i]),int(self.rot_times[l].split()[1])))
            i += 1
        state = tuple([tuple(state[0]),tuple(state[1])])
        #print (state)
        return state
    
    def somar_horarios(self,hora1,hora2):    
        soma = (hora1%100+hora2%100)        
        if (soma>59): hora1 = (hora1//100)*100 + (hora2//100)*100 + 100 + (soma%60)
        else: hora1 += hora2   
        if len(str(hora1))<4:
            hora1 = '%04d' % hora1
        return hora1
    
    def goal_test(self,state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        airplanes = len(self.planes)
        state = [list(state[0]),list(state[1])]
        for i in range (airplanes):
            if state[0][3+3*i] != self.state_initial[0][3+3*i]: return False
        if (state[0][0] == '0'): return True
        return False
        
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c - int(action.split()[4])

    def dif_planes(self):
        dif = []
        for i in self.planes:
            if i.split()[1] not in dif: dif.append(i.split()[1])
        return len(dif)
    
    def h(self,node):
        profit = 0
        for i in self.legs_restantes(node.state):
            profits = []
            for j in range (self.dif_planes()):
                profits.append(int(i.split()[4+2*j]))
            profit += max(profits)
        return profit*-1
    
    def load(self,f):
        """Loads problem file"""
        
        
        airports,planes,legs,rot_times=[],[],[],[]
        
        f1=f.readlines()
        
        for i in f1:
            if i[0] == 'A':
                airports.append(i.rstrip()[2:])
            elif i[0] == 'P':
                planes.append(i.rstrip()[2:])
            elif i[0] == 'L':
                legs.append(i.rstrip()[2:])
            elif i[0] == 'C':
                rot_times.append(i.rstrip()[2:])
                
        f.close()
        
        return [airports, list(reversed(planes)), legs, rot_times]
           
    def save(self,file_handler, path):
        k=0
        plane_mat = [ [ " " for i in range(len(self.planes)+1) ] for j in range(3) ]
        
        if path == None:
            auxToStr = "Infeasble"
            f = open(file_handler, "w+")
            f.write(auxToStr)
            f.close()
            return

        """Creates text to be written in the output file"""
        aux=[]
        for i in range (len(self.planes)):
            aux.append("S" + " " + self.planes[i][:6])
            if i==len(self.planes)-1:
                aux.append("P")
        
        """Writes states in the file"""
                        
        for leg in path:
            list_leg = list(str(leg.state).split(","))
            for i in range(1, len(list_leg)-len(self.legs)):
                if (i*3+1) >= len(list_leg)-len(self.legs): break
                if plane_mat[i-1][1] != list_leg[i*3][2:-1] and k < 2:
                    plane_mat[i-1][1] = list_leg[i*3][2:-1]
                    if len(list_leg[i*3+1]) < 8:
                        plane_mat[i-1][0] = list_leg[i*3+1][2:-1]
                    else:
                        plane_mat[i-1][0] = list_leg[i*3+1][2:-2]
                    k+=1
                elif plane_mat[i-1][1] != list_leg[i*3][2:-1] and k > 1:
                    plane_mat[i-1][2] = list_leg[i*3][2:-1]
                    aux[i-1] += " " + plane_mat[i-1][0] + " " + plane_mat[i-1][1] + " " + plane_mat[i-1][2]
                    plane_mat[i-1][1] = plane_mat[i-1][2]
                    if len(list_leg[i*3+1]) < 8:
                        plane_mat[i-1][0] = list_leg[i*3+1][2:-1]
                    else:
                        plane_mat[i-1][0] = list_leg[i*3+1][2:-2]
                elif '0' in list_leg[0]:
                    aux[-1] = aux[-1] + (" " + str(list_leg[1][2:-1]))

        """Converts list to string and writes in document"""
        auxToStr = ''.join([str(elem) + '\n' for elem in aux])
        
        f = open(file_handler, "w+")
        f.write(auxToStr)
        f.close()
        
    def build_graph(self,legs):
        
        graph_dict={}
        
        for i in legs:
            orig=i.split()[0]
            dest=i.split()[1]
            time=i.split()[2]
            
            if i.split()[0] in graph_dict.keys():
                graph_dict[orig].update({ dest : time})
            else:
                graph_dict[orig]={ dest : time} 
                        
        #print (graph_dict)
        return graph_dict
    
    
def d2b(n,base):
    if n == 0:
        return ''
    else:
        return d2b(n//base,base) + str(n%base)

def main():
    """Estado = [[nºde legs restantes,profit_total,aviao_1,aeroporto,horario,...,aviao_n,aeroporto,horario][1,0,0,1,...,0,1]]"""    
    p = ASARProblem()
    legs_feitas = len(p.legs) * ['1']
    best_solution = None
    for i in range (len(p.airports)**len(p.planes)): 
        p.initial = [len(p.legs),'0']
        if (d2b(i,len(p.airports))==''): num = 0
        else: num = int(d2b(i,len(p.airports)))
        for j in range (len(p.planes)):
           if j == (len(p.planes)-1): indice = num%10
           else: indice = num//(10**(j+1))
           p.initial.append(p.planes[j].split()[1])
           p.initial.append(p.airports[indice].split()[0])
           p.initial.append(p.airports[indice].split()[1])
        p.initial = tuple([tuple(p.initial),tuple(legs_feitas)])
        p.state_initial = p.initial
        solution = search.astar_search(p)
        if solution and not best_solution: best_solution = solution
        else:
            try:            
                if (int (solution.state[0][1]) > int(best_solution.state[0][1])):
                    best_solution = solution
            except:
                continue
    print (best_solution)
    print("\n")
    p.save("solution.txt", best_solution.path())
main()
# =============================================================================
#     p.state = [['6','0','a320','LPPT','800','a330','LPPT','800'],['1','1','1','1','1','1']]
#     node = search.Node(p.state)
#     print (node.state)
#     x = p.actions(node.state)
#     print(p.legs)
#     print (p.goal_test(p.state))
#     print (p.h(node))
#     print (p.legs_restantes(p.result(p.state,x[0])))
#     print (p.state)
#     print (p.path_cost(0,p.state, x[0],p.result(p.state,x[0])))
#     
# =============================================================================
