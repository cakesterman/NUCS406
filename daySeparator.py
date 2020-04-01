from collections import Counter

user_list = []
num_of_corona_tweets = 0

date_list = []
date_counter = [] #counter for dates overall


unrelated_tweets = 0

day = 1

date = ("Mar %02d") %day
    
user_list = []
num_of_corona_tweets = 0

print("extracting data for: ", date)

with open("twogig.txt", encoding='utf8') as datafile:
   
    print("Opened 1st DATAFILE")
  
    with open("day1.txt",'w',encoding='utf8') as d:
      
        print("Opened 2nd DATAFILE")
      
        for line in datafile:
           
            if date in line:
                
                d.writelines(line)
          
            else:
                continue

print("Finished extraction")
  

