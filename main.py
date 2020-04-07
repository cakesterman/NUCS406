import time
import networkx as nx
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt


def read_text_file_and_search_keyword(keyword):

    user_tweet_dict = {}
    user_tweet_list = []
    user_mentions = []
    user_hashtags = []
    user_sentiments = []

    with open("Data by Day/Mon_Mar_16.txt", encoding='utf8') as datafile:

        print("Reading in data...")

        # data = csv.reader(csvfile)

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

                        # user_tweet_list.append((user_tweet, counter))
                        user_tweet_list.append(user_tweet)

                        mention = add_user_mention(line)
                        hashtags = add_user_hashtags(line)

                        # if any(ele in line for ele in sentiments_list):
                        #     user_sentiments.append(add_user_sentiment(line))

                        # if mention is not None means if the list of mentions is greater than 1
                        if mention is not None:
                            user_mentions.append(mention)

                        if hashtags is not None:
                            user_hashtags.append(hashtags)

                        # counter += 1

            # user_tweet_list.append((add_user(line), counter))

            line = datafile.readline()

        end = time.perf_counter()

        print("Parsed data in {} seconds".format(end - start))

    return user_tweet_list, user_mentions, user_hashtags


def read_text_file_search_keyword_by_day(keyword):
    user_tweet_list = []
    user_mentions = []
    user_hashtags = []
    user_sentiments = []

    # with open("G:/Downloads/twitter-data-timpestamped (1).txt", encoding='utf8') as datafile:
    # with open("G:/Downloads/twitter-data-timpestamped.txt", encoding='utf8') as datafile:
    # with open("G:/Downloads/twitter-data-timpestamped (2).txt", encoding='utf8') as datafile:
    # with open("G:/Downloads/twitter-data-timpestamped-03192020.txt", encoding='utf8') as datafile:
    with open("C:/Users/Cakesterman/Downloads/day3.txt", encoding='utf8') as datafile:

        print("Reading in data...")

        # data = csv.reader(csvfile)

        line = datafile.readline()

        start = time.perf_counter()

        counter = 1
        while line:

            # Checks to make sure that the line is a valid line
            if "Mon " in line or "Tue " in line or "Wed " in line or "Thu " in line or "Fri " in line or "Sat " in line or \
                    "Sun " in line:

                current_date = line[8:9]
                current_month = line[4:6]

                # Search day by day

                if keyword in line:

                    user_tweet = add_user(line)
                    # user_dict = add_user(line)

                    if user_tweet is not None:

                        # user_tweet_list.append((user_tweet, counter))
                        user_tweet_list.append(user_tweet)

                        mention = add_user_mention(line)
                        hashtags = add_user_hashtags(line)

                        # if any(ele in line for ele in sentiments_list):
                        #     user_sentiments.append(add_user_sentiment(line))

                        # if mention is not None means if the list of mentions is greater than 1
                        if mention is not None:
                            user_mentions.append(mention)

                        if hashtags is not None:
                            user_hashtags.append(hashtags)

                        # counter += 1

            # user_tweet_list.append((add_user(line), counter))

            line = datafile.readline()

        end = time.perf_counter()

        print("Parsed data in {} seconds".format(end - start))

    make_network(user_tweet_list, user_mentions, keyword)

    # return user_tweet_list, user_mentions, user_hashtags


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
            user_hashtags.append(x)

    # print(user_hashtags)

    if len(user_hashtags) == 1:

        return None

    else:

        return user_hashtags


def print_values(passed):
    for x in passed:
        print(x)


def main():
    keyword = "coronavirus"

    all_user_tweets_corona, all_user_mentions_corona, all_user_hashtags_corona = read_text_file_and_search_keyword(
        keyword)

    # print_values(all_user_tweets_corona)
    # print()
    # print_values(all_user_mentions_corona)
    # print()
    # print_values(all_user_hashtags_corona)

    all_user_tweets_covid19, all_user_mentions_covid19, all_user_hashtags_covid19 = read_text_file_and_search_keyword(
        "covid-19")
    # print_values(all_user_tweets_covid19)
    # print()
    # print_values(all_user_mentions_covid19)
    # print()
    # print_values(all_user_hashtags_covid19)

    corona_network = make_network(all_user_tweets_corona, all_user_mentions_corona, keyword)
    analyze_network(corona_network, all_user_mentions_corona)


    covid_network = make_network(all_user_tweets_covid19, all_user_mentions_covid19, "Covid-19")


# def add_user_sentiment(tweet):
#
#     word = [sentiment for sentiment in sentiments_list if(sentiment in tweet)]
#
#     user = tweet.split('|')[1]
#
#     return (user, word[0].strip())


def make_network(all_users, all_user_mentions, keyword):

    corona_network = nx.Graph()

    corona_network.add_edges_from(all_user_mentions)

    print(nx.info(corona_network))

    plt.figure(figsize=(55, 45))
    plt.title(keyword)

    start = time.perf_counter()

    #nx.draw(corona_network, with_labels=False)
    #nx.draw_networkx_edges(corona_network, pos=nx.spring_layout(corona_network))
    #plt.show()
    #plt.savefig("Test")

    end = time.perf_counter()

    print("Created graph in {} seconds".format(end - start))

    return corona_network


def analyze_network(network, all_user_mentions):

    # Analzye clustering
    def analyze_clustering():

        print("Average clustering:", nx.average_clustering(network))
        print("Clustering:", nx.clustering(network))
        print("Generalized degree:", nx.generalized_degree(network))

    # Analyze communities
    def analyze_communities():

        community = greedy_modularity_communities(network)

        biggest_community_len = 0
        biggest_community = None

        for x in community:

            if len(x) > biggest_community_len:

                biggest_community_len = len(x)
                biggest_community = x

        print("Biggest community length:", biggest_community_len)
        print(biggest_community)

        def graph_community():

            new_list = []

            for mentions in all_user_mentions:

                for users in mentions:

                    if users in biggest_community:

                        # print("TRUE")
                        new_list.append(mentions)

            community_network = nx.Graph()

            community_network.add_edges_from(new_list)

            print(nx.info(community_network))

            plt.figure(figsize=(55, 45))

            nx.draw(community_network, with_labels=True)
            plt.show()

        graph_community()


    # analyze_clustering()
    analyze_communities()


if __name__ == '__main__':
    main()