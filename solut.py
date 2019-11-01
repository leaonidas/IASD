# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 14:48:32 2019

@author: Fernando
"""

# DEFINITIONS

import heapq
import datetime as time
import search

class ASARProblem(search.Problem):

    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self,state =[]):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        f = open("simple1.txt","r")
        [airports, planes, legs, rot_times] = self.load(f)
        self.initial = tuple([tuple(['6','0','a320','LPFR','800','a330','LPMA','800']),tuple(['1','1','1','1','1','1'])])
        self.build_graph(legs)
        self.state_initial = [['6','0','a320','LPFR','800','a330','LPMA','800'],['1','1','1','1','1','1']]
        self.legs = legs
        self.airports = airports
        self.planes = planes
        self.rot_times = rot_times
        
    
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
            for j in range (len(self.planes)):
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
        
        print (action)   
        state = [list(state[0]),list(state[1])]
        indice = 0
        for k in self.legs:
            if k.split()[0] == action.split()[0] and k.split()[1] == action.split()[1]: 
                state[1][indice] = '0'
            indice += 1
        state[0][0] = str(int(state[0][0]) - 1)
        state[0][1] = str(int(state[0][1]) + int(action.split()[4]))
        i = 0
        for j in self.planes: 
            if j.split()[1] == action.split()[3]:
                state[0][3+3*i] = action.split()[1]
                state[0][4+3*i] = self.somar_horarios(int(state[0][4+3*i]),int(action.split()[2]))
                state[0][4+3*i] = self.somar_horarios(int(state[0][4+3*i]),int(self.rot_times[i].split()[1]))
            i += 1
        state = tuple([tuple(state[0]),tuple(state[1])])
        #print (state)
        return state
    
    def somar_horarios(self,hora1,hora2):    
        soma = (hora1%100+hora2%100)        
        if (soma>59): hora1 = (hora1//100)*100 + (hora2//100)*100 + 100 + (soma%60)
        else: hora1 += hora2   
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

    def h(self,node):
        
        profit = 0
        for i in self.legs_restantes(node.state):
            profits = []
            for j in range (len(self.planes)):
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
           
    def save(self,file_handler, state):
        state=0;
        
        return state
        
    def get_airports_PQ(self, airports):
        h=[]
        for i in airports:
            name=i.split()[0]
            t1=time.timedelta(hours=(int(i.split()[1][0]))*10+int(i.split()[1][1]), minutes=(int(i.split()[1][2]))*10+int(i.split()[1][3]))
            t2=time.timedelta(hours=(int(i.split()[2][0]))*10+int(i.split()[2][1]), minutes=(int(i.split()[2][2]))*10+int(i.split()[2][3]))
            deltat=t2-t1
            h.append([time.timedelta.total_seconds(deltat),name])
        heapq._heapify_max(h)
        return h
    
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
    
    
    
def main():
    """Estado = [[nºde legs restantes,profit_total,aviao_1,aeroporto,horario,...,aviao_n,aeroporto,horario][1,0,0,1,...,0,1]]"""    
    p = ASARProblem()
    print(search.astar_search(p))
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
