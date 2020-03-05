import time
import networkx as nx
import matplotlib.pyplot as plt


def read_text_file_and_search_keyword(keyword):

    user_tweet_dict = {}
    user_tweet_list = []
    user_mentions = []
    user_hashtags = []
    user_sentiments = []

    #with open("G:/Downloads/twitter-data-timpestamped (1).txt", encoding='utf8') as datafile:
    with open("G:/Downloads/twitter-data-timpestamped.txt", encoding='utf8') as datafile:

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

                        #user_tweet_list.append((user_tweet, counter))
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

                        #counter += 1

            # user_tweet_list.append((add_user(line), counter))

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

    if len(mention_list) == 1:

        return None

    return tuple(mention_list)


def add_user_hashtags(tweet):

    user_hashtags = []

    temp_list = tweet.split('|')
    #print(temp_list)

    user_hashtags.append(temp_list[1])

    for x in temp_list[2].split():

        if x.startswith('#'):

            user_hashtags.append(x)

    #print(user_hashtags)

    if len(user_hashtags) == 1:

        return None

    else:

        return user_hashtags


def print_values(passed):

    for x in passed:

        print(x)


def main():

    keyword = "China"

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

    make_network(all_user_tweets_corona, all_user_mentions_corona, keyword)

# def add_user_sentiment(tweet):
#
#     word = [sentiment for sentiment in sentiments_list if(sentiment in tweet)]
#
#     user = tweet.split('|')[1]
#
#     return (user, word[0].strip())



def make_network(all_users, all_user_mentions, keyword):

    corona_network = nx.Graph()

    # Adding nodes to network from users who tweeted
    for user in all_users:

        corona_network.add_node(user[0])

    for mentions in all_user_mentions:

        for x in mentions:

            corona_network.add_node(x)

    try:
        corona_network.add_edges_from(all_user_mentions)
    except:
        # Fails if there are more than 3 tuples
        pass

    print(nx.info(corona_network))

    plt.figure(figsize=(50, 40))
    plt.title(keyword)

    start = time.perf_counter()

    nx.draw(corona_network, with_labels=True)
    plt.show()

    end = time.perf_counter()

    print("Created graph in {} seconds".format(end - start))

    for corona_network in nx.connected_component_subgraphs(corona_network):
        avg_degree = nx.average_shortest_path_length(corona_network) + avg_degree

    avg_degree = avg_degree / nx.number_of_nodes(corona_network)

    print(avg_degree)



if __name__ == '__main__':
    main()