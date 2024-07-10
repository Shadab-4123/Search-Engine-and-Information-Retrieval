import webpage_scraping as w
import requests
import numpy as np


def frequency(url):
    text = w.body_content(url)
    text = text.lower()
    lines = text.split("\n")
    word_freq = {}
    
    for line in lines:
        line = line.lower()
        clean_text = ''
        for word in line:
            if word.isalnum():
                clean_text += word
            else:
                clean_text += ' '  
        words_list = clean_text.split()
        # I am taking n = 5, fivegrams as default. 
        words= n_grams(words_list, 5)
        for word in words:
            if not word in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
    return word_freq

def n_grams(words_list, n):
    gramlist = []
    length = len(words_list)
    for i in range(length-n+1):
        ngram = ""
        for j in range(n):
            ngram += words_list[i+j] + " "
        gramlist.append(ngram)    
    return gramlist    
    

def hash(p,m, url):
    freq = frequency(url)
    words = list(freq.keys())
    hashcodes = {}
    for word in words:
        n = len(word)
        i = 0
        code = 0
        while i <= n-1:
            code += ord(word[i])*p**(i)
            i += 1
        wordcode = code % m 
        hashcodes[word] =  format(wordcode, '064b')
   
    return hashcodes   


def Simhash(p,m, url):
    frequ = list(frequency(url).values())
    hash_val = list(hash(p,m, url).values())
    weight_vector = np.zeros(64)
    for i in range(len(weight_vector)):
        for j in range(len(hash_val)):
            if int(hash_val[j][i]) == 1:
                weight_vector[i] += frequ[j]
            elif int(hash_val[j][i]) == 0:
                weight_vector[i] -= frequ[j]
    
    simhash = ''
    for k in range(len(weight_vector)):
        if weight_vector[k] >= 0:
            simhash += '1'
        else:
            simhash += '0'
    print(simhash)  
    return simhash          
        

def comparison(a, b, p, m):
    simhash1 = Simhash(p,m,a)
    simhash2 = Simhash(p,m,b) 
    common_bits = 0 
    for i in range(len(simhash1)):
        if simhash1[i] == simhash2[i]:
            common_bits += 1
    print("Number of common bits:", common_bits)        
    return ("common percentage: " + str((common_bits/64)*100) + " %" )              
            
if __name__ == '__main__':
    p = 53
    m = 2**64
    url1 = input("Enter first URL to check: ")
    url2 = input("Enter second URL to check: ")
    a = requests.get(url1)   
    b = requests.get(url2)
    print(comparison(a, b, p, m))
