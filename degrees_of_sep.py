    print(keyword)
    corona_network = nx.Graph()
    corona_network.add_edges_from(all_user_mentions)
    
    print(nx.info(corona_network))
    
    communities = list(greedy_modularity_communities(corona_network))
    
    """
    for i in range(0,len(communities)):
        community_size = len(sorted(communities[i]))
        if(community_size < 10):
            continue
        print(community_size)
    """
    
    sys.stdout = open("C:/Users/User/Desktop/CS406/Degrees_of_Seperation/march1_coroados.csv", "w")
    print("The number of communities, ", len(communities))
    print("Biggest Community Length, ", len(communities[0]))
    #print(communities[0])
    for i in range(0,len(communities)):
        all_path_length_values = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]   
        for node_s in communities[i]:
            for node_t in communities[i]:
                if node_s != node_t:
                    if nx.has_path(corona_network, node_s, node_t) :
                        shortest_path = nx.shortest_path(corona_network, node_s, node_t)
                        #print(shortest_path, 'has a length of = >', len(shortest_path))
                        if(len(shortest_path) > 13):
                            all_path_length_values[0]+=1
                        else:
                            all_path_length_values[len(shortest_path)]+=1
        print("Community ", i+1, ":")              
        for numbers in range(0,14):
            if(numbers == 0 or numbers == 1 or (all_path_length_values[numbers] == 0)):
                continue
            print("Length ", numbers,",", all_path_length_values[numbers])
        #print("Paths greater than thirteen: ", all_path_length_values[0])
        
        numerator = 0
        denominator = 0
        for j in range(2,14):
            numerator += (all_path_length_values[j] * j)
            denominator += all_path_length_values[j]
        if denominator != 0:
            print("Average Degree of Seperation, ",(numerator/denominator))
        else:
            print("No path")
    sys.stdout.close()