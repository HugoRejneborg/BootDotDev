def count_words(text):
    words = text.split()
    num_words = len(words)
    return num_words

def count_characters(text):
    text = text.lower()
    char_count = {}
    for char in text:
        if char not in char_count:
            char_count[char] = 1
        else:
            char_count[char] += 1
    return char_count

# helper function for the sort function
def sort_on(items):
    return items["num"]

def sort(dict):
    sorted_list = []
    for key, value in dict.items():
        sorted_list.append({"char": key, "num": value})
    sorted_list.sort(key=sort_on, reverse=True)
    return sorted_list


        
