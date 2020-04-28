import time
import networkx as nx
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import string
import csv
import os


def read_text_file_and_search_keyword(keyword, file):

    user_tweet_dict = {}
    user_tweet_list = []
    user_mentions = []
    user_hashtags = []
    user_sentiments = []

    with open(f"Data by Day/{file}", encoding='utf8') as datafile:

        # print(f"Reading in data from {file[12:len(file)]}...")
        print(f"Reading in data from {file}...")

        line = datafile.readline()

        start = time.perf_counter()

        counter = 1
        while line:

            if "Mon " in line or "Tue " in line or "Wed " in line or "Thu " in line or "Fri " in line or "Sat " in line or \
                    "Sun " in line:

                if keyword in line:

                    user_tweet = add_user(line)
                    # user_dict = add_user(line)

                    if user_tweet is not None:

                        user_tweet_list.append(user_tweet)

                        mention = add_user_mention(line)
                        hashtags = add_user_hashtags(line)

                        # if mention is not None means if the list of mentions is greater than 1
                        if mention is not None:
                            user_mentions.append(mention)

                        if hashtags is not None:
                            user_hashtags.append(hashtags)

                        # counter += 1

            line = datafile.readline()

        end = time.perf_counter()

        print("Parsed data in {} seconds".format(end - start))

    return user_tweet_list, user_mentions, user_hashtags


def add_user(tweet):
    final_tweet_list = []

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

    # print(tuple(mention_list))
    return tuple(mention_list)


def add_user_hashtags(tweet):
    user_hashtags = []

    temp_list = tweet.split('|')
    # print(temp_list)

    user_hashtags.append(temp_list[1])

    for x in temp_list[2].split():

        if x.startswith('#'):

            hashtag = ""

            for letters in x:

                # print(letters)

                if letters != '.' and letters != ',' and letters != ':' and letters != '…' and letters != '?' and letters != '!':
                    # print(letters)
                    hashtag += letters


            user_hashtags.append(hashtag)

    if len(user_hashtags) <= 2 or len(user_hashtags) > 4:

        return None

    else:

        return tuple(user_hashtags)


def print_values(passed):
    for x in passed:
        print(x)


def main():

    keyword = ""

    all_data_files = os.listdir("Data by Day/")

    # file_to_read = "Data by Day/Mon_Apr_06.txt"

    print(all_data_files)

    for file_to_read in all_data_files:

        all_user_tweets_corona, all_user_mentions_corona, all_user_hashtags_corona = read_text_file_and_search_keyword(
            keyword, file_to_read)
        make_network_hashtags(all_user_hashtags_corona, file_to_read)

    # file_to_read = "Mon_Mar_16.txt"
    # all_user_tweets_corona, all_user_mentions_corona, all_user_hashtags_corona = read_text_file_and_search_keyword(
    #     keyword, file_to_read)
    #
    # make_network_hashtags(all_user_hashtags_corona, file_to_read)

    # corona_network = make_network(all_user_tweets_corona, all_user_mentions_corona, keyword)
    # # analyze_network(corona_network, all_user_mentions_corona, file_to_read)
    #

    # analyze_network(corona_hashtag_network, _, all_user_hashtags_corona)

    # covid_network = make_network(all_user_tweets_covid19, all_user_mentions_covid19, "Covid-19")


def make_network(all_users, all_user_mentions, keyword):

    corona_network = nx.Graph()

    corona_network.add_edges_from(all_user_mentions)

    print(nx.info(corona_network))

    plt.figure(figsize=(55, 45))
    plt.title(keyword)

    start = time.perf_counter()

    # nx.draw(corona_network, with_labels=False)
    #nx.draw_networkx_edges(corona_network, pos=nx.spring_layout(corona_network))
    # plt.show()
    #plt.savefig("Test")

    end = time.perf_counter()

    print("Created graph in {} seconds".format(end - start))

    return corona_network

def make_network_hashtags(all_user_hashtags, file):

    corona_hashtag_network = nx.Graph()

    for x in all_user_hashtags:

        try:
            corona_hashtag_network.add_nodes_from(x[0])

            corona_hashtag_network.add_edge(x[1], x[2])

        except Exception as e:
            print("FAIL", e)

    print(nx.info(corona_hashtag_network))

    degree_centrality_dict = nx.degree_centrality(corona_hashtag_network)

    highest_value = 0
    hashtag = ''
    for key in degree_centrality_dict:

        if degree_centrality_dict[key] > highest_value:
            highest_value = degree_centrality_dict[key]
            hashtag = key

    # Delete everything related to coronavirus
    # del degree_centrality_dict["#coronavirus"]
    # del degree_centrality_dict["#COVID19"]
    # del degree_centrality_dict["#Coronavirus"]
    # del degree_centrality_dict["#COVIDー19"]
    # del degree_centrality_dict["#covid19"]
    # del degree_centrality_dict["#CoronaVirus"]
    # del degree_centrality_dict["#Covid19"]
    # del degree_centrality_dict["#COVID2019"]
    # del degree_centrality_dict["#covidー19uk"]

    top_10_values = Counter(degree_centrality_dict).most_common(20)
    print(top_10_values)

    print(f"Highest hashtag {hashtag} with degree centrality of {highest_value}")

    centraility = [x[1] for x in top_10_values]
    labels = [x[0] for x in top_10_values]
    y_pos = np.arange(len(labels))
    # print(centraility)
    # print(labels)


    # Plots a horizontal bar graph
    fig, ax = plt.subplots()

    ax.barh(y_pos, centraility, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Degree Centrality")
    ax.set_title(f"{file[:len(file) - 4]} Top 20 Degree Centrality")
    plt.savefig(f"Degree Centrality Graphs/Degree Centrality Matplotlib/{file[4:len(file) - 4]} Top 20 Degree Centrality", bbox_inches='tight', dpi=300)
    plt.show()


    # Code for PIE CHART, only shows a wedge tho
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=None, labels=labels, autopct='%1.1f%%', startangle=90)
    # ax1.axis('equal')
    # plt.axis("equal")
    # plt.show()

    # Writes the hashtags and centrality to a CSV file
    #with open(f"{file[16:len(file)-3]}_Degree-Centrality_1.csv", 'w', newline='', encoding='utf-8') as csvfile:
    # with open(f"Degree Centrality Graphs/Degree Centrality CSV/{file[4:len(file) - 3]}_Degree-Centrality_1.csv", 'w', newline='', encoding='utf-8') as csvfile:
    #
    #     writer = csv.writer(csvfile)
    #
    #     writer.writerow(("Hashtag", "Degree Centrality"))
    #
    #     for x in top_10_values:
    #
    #         writer.writerow((x[0], x[1]))

    return corona_hashtag_network


def analyze_network(network, all_user_mentions, file):

    # Analzye clustering
    def analyze_clustering():

        print("Average clustering:", nx.average_clustering(network))
        print("Clustering:", nx.clustering(network))
        print("Generalized degree:", nx.generalized_degree(network))

    # Analyze communities
    def analyze_communities():

        community = greedy_modularity_communities(network)

        print("Community length:", len(community))

        community_list = []

        biggest_community_len = 0
        biggest_community = None

        for x in community:

            if len(x) > biggest_community_len:

                biggest_community_len = len(x)
                biggest_community = x

            min_community_size = 50
            if len(x) >= min_community_size:

                community_list.append(x)

        # print(community_list)

        print("Biggest community length:", biggest_community_len)
        print(biggest_community)

        def graph_community(community):

            new_mention_list = []

            for mentions in all_user_mentions:

                for users in mentions:

                    if users in community:

                        new_mention_list.append(mentions)

            community_network = nx.Graph()

            community_network.add_edges_from(new_mention_list)

            print(nx.info(community_network))
            # print(nx.info(community_network)[36:38])

            plt.figure(figsize=(55, 45))
            plt.title("{} -- Community Length: {} -- {}".format(file[0:10], len(community), nx.info(community_network)))

            nx.draw(community_network, with_labels=True)

            plt.savefig("Communities/{}_Community_Nodes-{}.png".format(
                file[0:10], nx.number_of_nodes(community_network)))

            plt.show()

        for communities in community_list:

            # graph_community(communities)
            analyze_degree_centrality(communities)

    # Might not use this
    def analyze_degree_centrality(network):

        community_network = nx.Graph()

        # community_network.add_edges_from(new_mention_list)

        print(nx.info(community_network))
        # print(nx.info(community_network)[36:38])
        # print(nx.degree_centrality(community_network))

        degree_centrality_dict = nx.degree_centrality(community_network)

        highest_value = 0
        hashtag = ''
        for key in degree_centrality_dict:

            if degree_centrality_dict[key] > highest_value:

                highest_value = degree_centrality_dict[key]
                hashtag = key

        print(f"Highest hashtag {hashtag} with degree centrality of {highest_value}")




        #graph_community()


    # analyze_clustering()
    analyze_communities()


if __name__ == '__main__':
    main()