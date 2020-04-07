import time
import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities

input_file = "dayf29.txt"
output_file = "C:/Users/User/Desktop/CS406/Degrees_of_Seperation/february29_coroados.csv"

def read_text_file_and_search_keyword(keyword):

    user_tweet_list = []
    user_mentions = []
    user_hashtags = []

    with open(input_file, encoding='utf8') as datafile:

        #print("Reading in data...")

        line = datafile.readline()

        start = time.perf_counter()

        while line:

            if "Mon " in line or "Tue " in line or "Wed " in line or "Thu " in line or "Fri " in line or "Sat " in line or \
                    "Sun " in line:

                if keyword in line:

                    user_tweet = add_user(line)

                    if user_tweet is not None:

                        user_tweet_list.append(user_tweet)
                        mention = add_user_mention(line)

                        # if mention is not None means if the list of mentions is greater than 1
                        if mention is not None:
                            user_mentions.append(mention)


            line = datafile.readline()

        end = time.perf_counter()

        #print("Parsed data in {} seconds".format(end - start))

    return user_tweet_list, user_mentions, user_hashtags

def add_user(tweet):

    tweet_list = tweet.split("|")

    if len(tweet_list) == 3:

        return tweet_list[1], tweet_list[2]


def add_user_mention(tweet):

    mention_list = []

    temp_list = []

    temp_list = tweet.split('|')
    temp_list.pop(0)

    temp_list2 = []

    for items in temp_list:

        temp_list2.append(items.split())

    for x in temp_list2:

        for y in x:

            if y.startswith('@'):

                if y.endswith(':'):

                    y = y[0:len(y) - 1]

                mention_list.append(y)

    if len(mention_list) == 1 or len(mention_list) > 2:

        return None

    return tuple(mention_list)

def main():

    keyword = "coronavirus"

    all_user_tweets_corona, all_user_mentions_corona, all_user_hashtags_corona = read_text_file_and_search_keyword(
        keyword)

    make_network(all_user_tweets_corona, all_user_mentions_corona, keyword)
    
    keyword = "covid-19"
    
    #all_user_tweets_covid19, all_user_mentions_covid19, all_user_hashtags_covid19 = read_text_file_and_search_keyword(
         #keyword)

    #make_network(all_user_tweets_covid19, all_user_mentions_covid19, keyword)


def make_network(all_users, all_user_mentions, keyword):
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
    
    sys.stdout = open(output_file, "w")
    print("The number of communities, ",len(communities))
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
    
    #plt.figure(figsize=(55, 45))
    #plt.title(keyword)

    #start = time.perf_counter()
    
    #nx.draw(corona_network, with_labels=False)
    
    #plt.show()
    #plt.savefig("Test")

    #end = time.perf_counter()

    #print("Created graph in {} seconds".format(end - start))


if __name__ == '__main__':
    main()