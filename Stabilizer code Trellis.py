import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
import matplotlib.lines as mlines           ### for creating legend
from itertools import combinations          


paulis = ['I','X','Y','Z']

_xormap = {('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '0', ('0', '0'): '0'}
def xor(x, y):
    return ''.join([_xormap[a, b] for a, b in zip(x, y)])

def dec2bi(num):
    bin_string = np.binary_repr(num,width=n-k)
    return bin_string

def bi2dec(string):
    return int(string,2)

def single_pauliop(a,b):
    if a==b:
        return "I"
    elif a == "I":
        return b
    elif b == "I":
        return a
    else:
        if (a=="X" and b=="Z") or (a=="Z" and b=="X"):
            return "Y"
        elif (a=="Y" and b=="Z") or (a=="Z" and b=="Y"):
            return "X"
        else: 
            return "Z"

def pauliop(*args):
    aux = []
    n = len(args[1])
    for i in range(n):          ######## set auxiliary registeer to [II...I]_n
        aux += 'I'

    for pauli in args:
        result = []
        for i in range(n):
            result += single_pauliop(aux[i],pauli[i])
        
        aux = result
    product = ''.join(aux)          ######## list to string with no spaces
    return product

def inner_product(a,b):
    
    if len(a) == 1:                 ##### if 'a' is single bit Pauli, product is done element wise
        elem_wise_prod = []
        for i in range(len(b)):
            if a=='I' or b[i]=='I' or b[i]==a:
                elem_wise_prod.append('0')
            else:
                elem_wise_prod.append('1')
        return ''.join(elem_wise_prod)
    else:
        sum = 0
        if len(a) != len(b):
            raise Exception('Lengths do not match')
        else:
            for i in range(len(a)):
                if a[i]=="I" or b[i]=="I" or a[i]==b[i]:
                    sum += 0
                else:
                    sum += 1
        return sum%2

def pi_op(i,pauli):                         ##### pi operator from Ollivier et al.
    out = ""
    for n in range(i):
        out += pauli[n]
    for n in range(i+1,len(pauli)+1):
        out += "I"
    return out

def get_stabilizer_set(generators):
    identity = ''
    for i in range(len(generators[0])):          
        identity += 'I'
    stabilizers = [identity] + generators          

    comb_lists = []
    for i in range(1,r):                   ####### get combinations of stab generators
        comb = list(combinations(generators,i+1))
        comb_lists.append([pauliop(*pair) for pair in comb])
    
    for i in range(0,r-1):                 ###### add to list
        stabilizers += comb_lists[i]
    return stabilizers

def syndrome(pauli):
    syndrome = ""
    for elem in stab_gen:
        syndrome += str(inner_product(elem,pauli))
    return syndrome

def partial_syndrome_ollivier(i,pauli):
    state_i_pauli = pi_op(i,pauli)
    return syndrome(state_i_pauli)

def partial_syndrome_wolfbcjr(i,pauli):
        result = syndrome(stab_gen[0])
        for iter in range(i):
            ci_hi = inner_product(pauli[iter],H[:,iter])
            result = [int(result[j])^int(ci_hi[j]) for j in range(n-k)]
        str_result = ''.join(str(x) for x in result)                ### convert to string
        return str_result



############# FIVE QUBIT CODE (Trellis oriented form)################
# stab_gen = ['ZXIII','XZXII','IXZXI','IIXZX']   
## Logical operators on C #######
# X_bar1 = 'IIIIX'
# Z_bar1 = 'ZIZIZ'
# NqS_generators = [X_bar1,Z_bar1]      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

# error = 'IIIII'                   #### arbitrary error for a required syndrome (for Ollivier method)
# print("\n Syndrome for {} is {}".format(error,syndrome(error)))
### OR ###
# required_final_syndrome = '1001'            #### (n-k) bit; for Wolf-BCJR method

############# FIVE QUBIT CODE (Standard)################
stab_gen = ['XZZXI','IXZZX','XIXZZ','ZXIXZ']   
# Logical operators on C #######
X_bar1 = 'XXXXX'
Z_bar1 = 'ZZZZZ'
NqS_generators = [X_bar1,Z_bar1]      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

error = 'XIXXI'                   #### arbitrary error for a required syndrome (for Ollivier method)
print("\n Syndrome for {} is {}".format(error,syndrome(error)))
## OR ###
required_final_syndrome = '1001'            #### (n-k) bit;  for Wolf-BCJR method

################## 3 qubit rep code ############
# stab_gen = ['ZZI','IZZ']                        
# ####### Logical operators on C #####
# X_bar1 = 'XXX'
# Z_bar1 = 'ZZZ'
# NqS_generators = [X_bar1,Z_bar1]      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

# error = 'IIX'                   #### arbitrary error for a required syndrome (for Ollivier method)
# print("\n Syndrome for {} is {}".format(error,syndrome(error)))
# ## OR ###
# required_final_syndrome = '01'            #### (n-k) bit; for Wolf-BCJR method


################# 4 qubit code ############
# stab_gen = ['XXXX','ZZZZ']                    
# ## Logical operators on C #####
# X_bar1 = 'IXIX'
# Z_bar1 = 'IIZZ'
# X_bar2 = 'IIXX'
# Z_bar2 = 'IZIZ'
# NqS_generators = [X_bar1,Z_bar1,X_bar2,Z_bar2]      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

# error = 'IIIY'                   #### arbitrary error for a required syndrome (for Ollivier method)
# print("\n Syndrome for {} is {}".format(error,syndrome(error)))
# ## OR ###
# required_final_syndrome = '11'            #### (n-k) bit; for Wolf-BCJR method


# ################# 9 qubit code ############
# stab_gen = ['ZZIIIIIII','IZZIIIIII','IIIZZIIII','IIIIZZIII',
#             'IIIIIIZZI','IIIIIIIZZ','XXXXXXIII','IIIXXXXXX']
# #### Logical operators on C #####
# X_bar1 = 'ZZZZZZZZZ'
# Z_bar1 = 'XXXXXXXXX'
# NqS_generators = [X_bar1,Z_bar1]      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

# error = 'IIIZIIIII'                   #### arbitrary error for a required syndrome (for Ollivier method)
# print("\n Syndrome for {} is {}".format(error,syndrome(error)))
# ### OR ###
# required_final_syndrome = '11110000'            ####  (n-k) bit; for Wolf-BCJR method


##### Steane 7 qubit code  ############
# stab_gen = ['IIIXXXX','IXXIIXX','XIXIXIX','IIIZZZZ','IZZIIZZ','ZIZIZIZ']
# #### Logical operators on C #####
# X_bar1 = 'XXXXXXX'
# Z_bar1 = 'ZZZZZZZ'
# NqS_generators = [X_bar1,Z_bar1]      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

# error = 'IIIIIII'                   #### arbitrary error for a required syndrome (for Ollivier method)
# print("\n Syndrome for {} is {}".format(error,syndrome(error)))
# ### OR ###
# required_final_syndrome = '000000'            ####  (n-k) bit; for Wolf-BCJR method



##### ENTER YOUR STABILIZER CODE 'C'  ############
# stab_gen = []
# #### Logical operators on C #####
# ## Enter X1,Z1,...,Xk,Zk. If not provided, comment out Get normalizer and Lower bound sections below ## 
# NqS_generators = []      #### N(S)/S = set generated by X1,Z1,...,Xk,Zk

# error =                    #### arbitrary error for a required syndrome (for Ollivier method)
# print("\n Syndrome for {} is {}".format(error,syndrome(error)))
# ### OR ###
# required_final_syndrome =             ####  (n-k) bit; for Wolf-BCJR method



######### Code Parameters/Matrix form  ##########
n = len(stab_gen[0])
r = len(stab_gen)
k = n-r

generators = [list(stab_gen[i]) for i in range(len(stab_gen))]
H = np.reshape(generators,(len(generators),len(generators[0])))     #### stabilizer generators matrix form


stabilizers = get_stabilizer_set(stab_gen)
# print(stabilizers)

####### Get normalizer and same syndrome error sets (Comment out if logical operators not provided)######
N_quotient_S = get_stabilizer_set(NqS_generators)   #### |N(S)/S| = |P_(n-r)| ==> 4^(n-r) 

normalizer = []
for elem in N_quotient_S:
    for i in stabilizers:
        normalizer.append(pauliop(i,elem))

Err_NS = [pauliop(error,elem) for elem in normalizer]          #### P = Ps + S_dual

# Lower bound on number of vertices at time i (Upper bound = 2^(n-k))
def get_lowerbound(i,normalizer):
    future_subgroup=[]
    past_subgroup=[]
    for elem in normalizer:
        if all(l=="I" for l in elem[:i]):          ###  C_fi = first i cmponents are I
            future_subgroup.append(elem)
        if all(l=="I" for l in elem[i-n:]):         #### C_pi = last n-i components are I
            past_subgroup.append(elem)

    len_past = len(past_subgroup);  loglen_past = np.log2(len_past)
    len_future = len(future_subgroup);  loglen_future = np.log2(len_future)
    lowerbound = 2**(n+k-loglen_past-loglen_future)

    if i==0 or i==n:
        return 1
    else:
        return lowerbound

def get_minimal_trellis_node_lengths():
    for i in range(0,n+1):
        print(f"For i={i}, |V_i|=",get_lowerbound(i,normalizer))
get_minimal_trellis_node_lengths()
###### (Comment out if logical operators not provided) ######

def ollivier_method():
    
    part_syn_0 = partial_syndrome_ollivier(0,error)
    ###### dict containing all paths in trellis ####
    path_dict = ({pauli: [part_syn_0]+[partial_syndrome_ollivier(i,pauli) for i in range(1,n+1)] for pauli in Err_NS})

    # print(path_dict)

    listofstates=[[part_syn_0]]
    for i in range(1,n+1):
        states_i = []
        for elem in Err_NS:
            states_i.append(partial_syndrome_ollivier(i,elem))
        listofstates.append(sorted(set(states_i)))

    G =nx.MultiGraph()
    hspace = 1;vspace = 0.5

    posdict = {}
    labeldict = {}
    for x,V_i in enumerate(listofstates):
        for y,state in enumerate(V_i):
            node = (x,y) 
            G.add_node(node,label=state)
            posdict[node]= ((x),(len(V_i)-1)/2 - y)
            labeldict[node]=state

    # print(labeldict)


    I_attributes = {'pauli':'I','color':'black','style':'-'}
    X_attributes = {'pauli':'X','color':'blue','style':':'}
    Y_attributes = {'pauli':'Y','color':'red','style':'--'}
    Z_attributes = {'pauli':'Z','color':'lime','style':'-.'}
    pauli_attrib_dict={'I':I_attributes,'X':X_attributes,'Y':Y_attributes,'Z':Z_attributes}

    legend_handles = [mlines.Line2D([],[],color='Black',label='I'),mlines.Line2D([],[],color='Blue',label='X'),
                    mlines.Line2D([],[],color='red',label='Y'),mlines.Line2D([],[],color='lime',label='Z')]


    already_added = set()


    # key_counter = 0
    for elem in Err_NS:
        for i in range(1,n+1):
            start_node = path_dict[elem][i-1]
            end_node = path_dict[elem][i]
            start_index = (i-1,listofstates[i-1].index(start_node))
            end_index = (i,listofstates[i].index(end_node))
            edge_pauli = elem[i-1]
            edge_attr = pauli_attrib_dict[edge_pauli]
            edge_record = (start_index,end_index,edge_pauli)
            if edge_record not in already_added:
                G.add_edge(start_index,end_index,**edge_attr)
                # key_counter += 1
                already_added.add(edge_record)


    print("Number of edges:",len(already_added))

    # G.add_edges_from([(a,'00',{'pauli':'X','color':'blue','style':':'}),
                    #   (a,'01',{'pauli':'Y','color':'red','style':'--'})])
    # G.add_edge((0,0),(1,0),key=0,**X_attributes)
    # G.add_edge((0,0),(1,0),key=1,**Y_attributes)
    # G.add_edge((0,0),(1,1),**Z_attributes)


    edge_labels = {(n1, n2,key): d['pauli'] for n1, n2,key, d in G.edges(data=True,keys=True)}
    edge_color = {(n1, n2,key): d['color'] for n1, n2,key, d in G.edges(data=True,keys=True)}
    edge_style = {(n1, n2,key): d['style'] for n1, n2,key, d in G.edges(data=True,keys=True)}
    # print(G.edges(data=True,keys=True))
    # print(edge_color)
    ax = plt.gca()
    nx.draw_networkx_labels(G,labels=labeldict,pos=posdict)
    for e in G.edges:
        ax.annotate("",
                    xy=posdict[e[1]], xycoords='data',
                    xytext=posdict[e[0]], textcoords='data',
                    arrowprops=dict(arrowstyle="-",color=edge_color[e],
                                    shrinkA=16, shrinkB=16,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])
                                    ),
                                    ),
                    )
    plt.axis('off')
    nx.draw(G,pos=posdict,node_size=900)
            
    # nx.draw_networkx_edge_labels(G,pos=posdict,edge_labels=edge_labels)
    plt.axis('off')
    plt.legend(handles=legend_handles)
    plt.title("Ollivier method")
    plt.show()


def bcjr_wolf_method():

    G =nx.MultiDiGraph()
    hspace = 1;vspace = 0.5

    par_syn_0 = partial_syndrome_ollivier(0,stab_gen[0])

    posdict = {(0,0):(0,0)}
    labeldict = {(0,0): par_syn_0}

    I_attributes = {'pauli':'I','color':'black','style':'-'}
    X_attributes = {'pauli':'X','color':'blue','style':':'}
    Y_attributes = {'pauli':'Y','color':'red','style':'--'}
    Z_attributes = {'pauli':'Z','color':'lime','style':'-.'}
    pauli_attrib_dict={'I':I_attributes,'X':X_attributes,'Y':Y_attributes,'Z':Z_attributes}

    legend_handles = [mlines.Line2D([],[],color='Black',label='I'),mlines.Line2D([],[],color='Blue',label='X'),
                    mlines.Line2D([],[],color='red',label='Y'),mlines.Line2D([],[],color='lime',label='Z')]

    length_Vi = 2**(n-k)
    already_added = set()

    for V_t in range(length_Vi):                    ##### edges from 0 to t=1
        state = dec2bi(V_t)
        node0 = (1,V_t)
        G.add_node(node0,label = state)
        posdict[node0]= (1,(length_Vi-1)/2 - V_t)
        labeldict[node0] = state

        for a in paulis:
            end_node_label = xor(par_syn_0,inner_product(a,H[:,0]))
            end_node_ycord = bi2dec(end_node_label)
            pauli_attrs = pauli_attrib_dict[a]
            edge_record = ((0,0),(1,end_node_ycord),a)
            if edge_record not in already_added:
                G.add_edge((0,0),(1,end_node_ycord),**pauli_attrs)
                already_added.add(edge_record)
    

    for t in range(1,n):                                ###### further edges
        for V_t in range(length_Vi):
            state = dec2bi(V_t)
            node = (t+1,V_t) 
            G.add_node(node,label=state)
            posdict[node]= (t+1,(length_Vi-1)/2 - V_t)
            labeldict[node]=state

            for a in paulis:
                end_node_label = xor(state,inner_product(a,H[:,t]))
                end_node_ycord = bi2dec(end_node_label)
                pauli_attrs = pauli_attrib_dict[a]
                G.add_edge((t,V_t),(t+1,end_node_ycord),**pauli_attrs) 

    #### Removing extra nodes according to required syndrome #######
    for t in range(1,n+1):
        for V_t in range(length_Vi):
            node = (t,V_t)
            if G.in_degree(node) == 0:
                G.remove_node(node)
                del labeldict[node]
                del posdict[node]

    for V_t in range(length_Vi):
        node = (n,V_t)
        if node != (n,bi2dec(required_final_syndrome)):
            G.remove_node(node)
            del labeldict[node]
            del posdict[node]

    for t in range(n-1,0,-1):
        for V_t in range(length_Vi):
            node = (t,V_t)
            if G.out_degree(node) == 0:
                G.remove_node(node)
                del labeldict[node]
                del posdict[node]

    print("Number of edges=",G.number_of_edges())
    edge_labels = {(n1, n2,key): d['pauli'] for n1, n2,key, d in G.edges(data=True,keys=True)}
    edge_color = {(n1, n2,key): d['color'] for n1, n2,key, d in G.edges(data=True,keys=True)}
    edge_style = {(n1, n2,key): d['style'] for n1, n2,key, d in G.edges(data=True,keys=True)}
    # print(G.edges(data=True,keys=True))
    # print(edge_color)
    ax = plt.gca()
    nx.draw_networkx_labels(G,labels=labeldict,pos=posdict)
    for e in G.edges:
        ax.annotate("",
                    xy=posdict[e[1]], xycoords='data',
                    xytext=posdict[e[0]], textcoords='data',
                    arrowprops=dict(arrowstyle="-",color=edge_color[e],
                                    shrinkA=16, shrinkB=16,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr',str(0.3*e[2])
                                    ),
                                    ),
                    )
    plt.axis('off')
    nx.draw(G,pos=posdict,node_size=900,arrows=False)
            
    # nx.draw_networkx_edge_labels(G,pos=posdict,edge_labels=edge_labels)
    plt.axis('off')
    plt.legend(handles=legend_handles)
    plt.title("BCJR-Wolf Method")
    plt.show()

#### Select method ####
ollivier_method()
# bcjr_wolf_method()