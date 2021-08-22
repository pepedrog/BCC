from collections import deque

U = {0, 1, 2, 3, 4}
W = {5, 6, 7, 8, 9}
c = [[None, None, None, None, None, 6, 17, 10, 1, 3],
    [None, None, None, None, None, 9, 23, 21, 4, 5],
    [None, None, None, None, None, 2, 8, 5, 0, 1],
    [None, None, None, None, None, 19, 31, 19, 20, 9],
    [None, None, None, None, None, 21, 25, 28, 3, 9],
    [6, 9, 2, 19, 21, None, None, None, None, None],
    [17, 23, 8, 31, 25, None, None, None, None, None],
    [10, 21, 5, 19, 28, None, None, None, None, None],
    [1, 4, 0, 20, 3, None, None, None, None, None],
    [3, 5, 1, 9, 9, None, None, None, None, None]]

def Hungarian(U, W, c):
    n = 2*len(U)
    M = set()
    M_v = set() #saturated vertices
    min_c = None
    for i in range(n):
        for j in range(n):
            if(min_c == None):
                min_c = c[i][j]
            elif(c[i][j] is not None and min_c > c[i][j]):
                min_c = c[i][j] 
    y = [min_c/2]*(n)
    t = 0
    while (True):
        print("\n ----------------------------------- t = " + str(t))
        if (len(M) == n/2):
            return (M, y)
        
        E = set()
        for i in range(n):
            for j in range(n):
                if (c[i][j] is not None and y[i] + y[j] == c[i][j]):
                    E.add(frozenset([i, j]))
        #print("E = " + str(E))

        R = set()
        for u in U:
            if (u not in M_v):
                R.add(u)
        for i in range(n):
            for w in W:
                R_list = list(R)
                for r in R_list:
                    for e in E:
                        if e not in M and r in e and w in e: R.add(w)
            for u in U:
                R_list = list(R)
                for r in R_list:
                    for e in E:
                        if e in M and r in e and u in e: R.add(u)
        #print("R = " + str(R))

        if len(R.intersection(W.difference(M_v))) > 0:
            print("\n-------- Matching Update ---------")
            #finds augmenting path
            for u in U:
                if u not in M_v:
                    #do a bfs
                    q = deque() #queue of vertices
                    q.append(u)

                    parents = [None]*n
                    parents[u] = u
                    final_w = None
                    while(len(q) > 0 and final_w is None):
                        v = q.popleft()
                        for e in E:
                            if v not in e:
                                continue
                            for w in e:
                                if (w != v and ((w in W and e not in M) or (w in U and e in M))):
                                    if (w in W and w not in M_v):
                                        final_w = w
                                    q.append(w)
                                    parents[w] = v
                    if final_w is not None:
                        #recover the path
                        P = deque()
                        P.append(final_w)
                        while (P[0] != u):
                            P.appendleft(parents[P[0]])
                        print('P =' + str(P))
                        P_edges = set()
                        for i in range(1,len(P)):
                            P_edges.add(frozenset([P[i], P[i-1]]))
                        break
            #  builds next matching
            M = (M.difference(P_edges)).union(P_edges.difference(M))
            M_v = set()
            for e in M:
                for v in e:
                    M_v.add(v) 
            print(M)
        #dual update
        else:
            print("\n-------- Dual Update ---------")
            K = (U.difference(R).union(W.intersection(R)))
            print("K = " + str(K))
            d = [1]*n
            for u in U:
                if u in K:
                    d[u] = 0
            for w in W:
                if w in K:
                    d[w] = -1
                else:
                    d[w] = 0
            print("d = " + str(d))

            l = None
            for i in range(n):
                for j in range(n):
                    if(c[i][j] is not None and d[i] + d[j] > 0 and {i, j} not in E):
                        if (l == None):
                            l = (c[i][j] - y[i] - y[j]) / (d[i] + d[j])
                        else:
                            l = min(l, (c[i][j] - y[i] - y[j]) / (d[i] + d[j]))
            print("lambda = " + str(l))

            for i in range(n):
                y[i] += l*d[i]  
            
            print("new y = " + str(y))

        t += 1

Hungarian(U, W, c)