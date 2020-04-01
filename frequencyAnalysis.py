from collections import Counter

#from collections import counter
user_list = []
num_of_corona_tweets = 0

date_list = []
date_counter = [] #counter for dates overall


unrelated_tweets = 0

day = 1

while day < 2:

    date = ("mar %02d") %day
    
    user_list = []
    num_of_corona_tweets = 0
    
    day += 1
    
    with open("twogig.txt", encoding='utf8') as datafile:
   
        line = datafile.readline()
    
        remove_col = ":"
    
        tempword = ""
    
        while line:
        
            line = line.lower()
        
            if ("#covid" in line or "#covid-19" in line) and date in line:
           
                for word in line.split():
              
                    if word.startswith("@"):
              
                        if word == '@':
                            unrelated_tweets +=1
                        
                        elif word.endswith(remove_col):
                            tempword = word.replace(":", "")
                            user_list.append(tempword)
                            num_of_corona_tweets +=1
                        else:
                            user_list.append(word)
                            num_of_corona_tweets +=1
                    else:
                        unrelated_tweets += 1
            
            line = datafile.readline()
        
        user_counter = Counter(user_list)
        print("Date: ", date)
        print("Number of tweets mentioning COVID-19: ", num_of_corona_tweets)
        print(user_counter.most_common(10))
        print("-------------------------------------")
        
print("END OF PROGRAM")
#print("Unrelated tweets: ", unrelated_tweets) # debug purposes only
