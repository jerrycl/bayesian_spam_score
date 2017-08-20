#! /usr/bin/env python

# A common first example of a coroutine is a running average. How about a little Bayesian spam filter instead?

# Assume we did supervised learning on 1000 emails, a human flagging which were spam,
# then a program ran through the words in the email, and adding/updating a dict entry for each,
# consisting of a list of two numbers: the number of spams which contain the word,
# and the number of innocent emails which contain the word.
   
priors = [200.0,800.0]  # 200 of the emails were judged to be spam, 800 were innocent

# A hypothetical word count dictionary: 'viagra' appears in 40 spams, and 4 innocents; etc. 
wordList = { 'viagra': [40,4], 'v1agra': [45,0], 'das': [0,55], 'credit': [39,20], 'today': [45,65],
 'order': [98,55], 'offer': [66,34], 'cialis': [40,1], 'c1ali$': [35,0], 'theory': [1,24], 'bayes':[1,15] }

# the coroutine:
def bayes_rule():
    ratio = [1.0,1.0]
    while True:
        term = yield ratio
        ratio[0] *= term[0]
        ratio[1] *= term[1]
        if ratio[0] == 0.0 and ratio[1] == 0.0:
            ratio = [1.0,1.0]   ## call that even money
        #and normalize,if we can:
        if ratio[0] != 0.0:
            ratio[1] = float(ratio[1]) / float(ratio[0])
            ratio[0] = 1.0

def update_likelihood(ratio):
    ratio = bayes.send(ratio)
    print "likelihood this is spam: ", (float(ratio[0]) / (float(ratio[0]) + float(ratio[1]))) * 100.0, "%"
    

messages = (
    # if it's from my friend Das, it's almost certainly not spam:
    "I can order you some books today, best, Das",

    # if they misspell viagra, it's almost certainly spam:
    "Order today! Get v1agra with your credit card!",

    # here's one that is not certain, but does tip the scale:
    "Order today with your credit card. This offer is available for a limited time",
    
    "Using Bayes theory, innocent words offer reduced likelihood.")
    

for message in messages:
    bayes = bayes_rule()
    next(bayes)
    # assume we decided that of the 1000 emails, 200 were spam, and 800 were innocent.  
    # Initialize the likelihood of spam:
    bayes.send(priors)
    message = message.lower().split(' ')
    print
    print message
    wordsConsidered = []
    for word in message:
        word = word.strip(' ,')
        if word in wordsConsidered:
            continue
        if word in wordList:
            wordsConsidered.append(word)
            a,b = wordList[word][0] / priors[0],wordList[word][1] / priors[1]
            print word, ' ',
            
            update_likelihood([a,b])
