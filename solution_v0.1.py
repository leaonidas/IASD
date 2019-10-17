# DEFINITIONS

import heapq
import datetime as time



class Graph:
    """A graph connects nodes (vertices) by edges (links).  Each edge can also
    have a length associated with it.  The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C.  You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added. The graph
    stays undirected; if you add more links with g.connect('B', 'C', 3), then
    inverse link is also added.  You can use g.nodes() to get a list of nodes,
    g.get('A') to get a dict of links out of A, and g.get('A', 'B') to get the
    length of the link from A to B.  'Lengths' can actually be any object at
    all, and nodes can be any hashable object."""

    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        """Make a digraph into an undirected graph by adding symmetric edges."""
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed:
            self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graph_dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)
    
class ASARProblem(object):

# =============================================================================
#     def RBFS(problem, node, flimit):
#         if problem.goal_test(node.state):
#             return node, 0  # (The second value is immaterial)
#         successors = node.expand(problem)
#         if len(successors) == 0:
#             return None, infinity
#         for s in successors:
#             s.f = max(s.path_cost + h(s), node.f)
#         while True:
#             # Order by lowest f value
#             successors.sort(key=lambda x: x.f)
#             best = successors[0]
#             if best.f > flimit:
#                 return None, best.f
#             if len(successors) > 1:
#                 alternative = successors[1].f
#             else:
#                 alternative = infinity
#             result, best.f = RBFS(problem, best, min(flimit, alternative))
#             if result is not None:
#                 return result, best.f
# 
#     node = Node(problem.initial)
#     node.f = h(node)
#     result, bestf = RBFS(problem, node, infinity)
#     return result
# =============================================================================
    
    
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        possible_actions=['expand_tree','backtrack','assign_leg2plane']
        
        #################### AUXILIARY FUNCTIONS #################
        #expand_tree_node
        #backtrack
        #assign_leg2plane (when fastest plane is the most profitable)
        
        
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            1
            #return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError
        
    def load(f):
        """Loads problem file"""
        airports=[]
        planes=[]
        legs=[]
        rot_times=[]
        
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
        
        return [airports, planes, legs, rot_times]
    
    def find_path(origin, destination):
            
        return 0
        
    def save(file_handler, state):
        state=0;
        
        return state
    
    
    def get_airports_PQ(airports):
        h=[]
        for i in airports:
            name=i.split()[0]
            t1=time.timedelta(hours=(int(i.split()[1][0]))*10+int(i.split()[1][1]), minutes=(int(i.split()[1][2]))*10+int(i.split()[1][3]))
            t2=time.timedelta(hours=(int(i.split()[2][0]))*10+int(i.split()[2][1]), minutes=(int(i.split()[2][2]))*10+int(i.split()[2][3]))
            deltat=t2-t1
            h.append([time.timedelta.total_seconds(deltat),name])
        heapq._heapify_max(h)
        return h
    
    def build_graph(legs):
        
        graph_dict={}
        
        for i in legs:
            orig=i.split()[0]
            dest=i.split()[1]
            time=i.split()[2]
            
            if i.split()[0] in graph_dict.keys():
                graph_dict[orig].update({ dest : time})
            else:
                graph_dict[orig]={ dest : time} 
                
            print(str(graph_dict))
        
        G=Graph(graph_dict)
        
        return G
    

# =============================================================================
#     def get_class_assigned_legs(planes,legs,rot_times):            
#         for i in legs:
#             x=i.split()
#             for j in range(3,len(x))
#                 if x(j) in pclass and x(j-1) :
#         return assigned_legs
# ============================================================================
#get_airports_by_availability(airports)
#print(airports)
#def actions(state)
#possible_actions=legs
#check_arc_consistency(node,origin, lala)
#a=check_cycle_condition(legs, origin)
#get_possible_nodes(legs,origin,node)        
    
    
# SOLUTION
        
f = open("simple1.txt","r")

[airports, planes, legs, rot_times] = ASARProblem.load(f)

A= ASARProblem.build_graph(legs)
x= Graph.nodes(A)

# =============================================================================
# APQ=ASARProblem.get_airports_PQ(airports)
# 
# starting_airport=heapq.heappop(APQ)[1]
# 
# print(legs)
# =============================================================================