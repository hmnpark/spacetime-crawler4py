def _tokenize(page_content) -> [str]:
    '''This function takes in a string representing the visible text content on a page,
       and returns a list of tokens in that page
    '''
      
    result = []

    token = '' 
    for char in page_content: #O(m) where m is the amount of characters in the line
                
        if char.isalnum() and char.isascii(): #since utf-8 is used, non-english characters 
                                                          # need to be treated as delimeters, as the encoding
                                                          #will not remove them
            token+=char.lower() #makes every token lowercase so that later they are unified
        else:
            if token != '': #filters out empty strings
                result.append(token) #adds the whole current token to the list
                token = '' #starts over with an empty token
        
    return result

def _computeWordFrequencies(tokens: [str]) -> {str:int}:
    '''This function takes in a list of tokens and returns 
       a dict that maps each token to its number of 
       occurencies in the list, case-insensitive.
        
       The tokens are assumed to be all lower case as 
       tokenize handles this

       Overall, the complexity of this function is O(n) since
       every token in a list of n tokens is iterated over,
       and O(1) dict operations are completed for every
       token
    '''

    frequencies = {}
    for token in tokens: #O(n) 
        frequencies[token] = frequencies.get(token, 0) + 1 #O(1) + O(1) - dict operations are O(1)
        #Could also use a default dict. get has a default return value of 0 if token is not in dict
    return frequencies

def compute_word_frequencies_for_page(page_content: str) -> {str:int}:
    '''Returns a dictionary of tokens and their frequency for a string storing the contents of a page'''

    return _computeWordFrequencies(_tokenize(page_content))