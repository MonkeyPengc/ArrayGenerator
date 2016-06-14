# file: back_end.py
# brief: this script allows user specified parameters (data type, length, values range) to be used 
# to generate a corresponding array, contains input validator, and prints out messages in console.
# author: Cheng Peng

import sys

# -----------------------------------------------------------------------------
# define an abstract class
class ArrayUtils:
    def __init__(self, integer=False, char=False):
        self.array = []
        self.unique_array = []
        self.sorted_array = []
        self.consecutive_array = []
        self.is_integer = integer
        self.is_char = char
    
    # -----------------------------------------------------------------------------
    # remove duplicates
    def remove_duplicates(self):
        if len(self.array) <= 1:
            raise Exception("The array has less than two items.")
        
        unique_array = set()
        for item in self.array:
            unique_array.add(item)
        self.unique_array = list(unique_array)
        
    # -----------------------------------------------------------------------------
    # sort array
    def sort_array(self):
        
        ## the counting sort algorithm takes O(n) time, and O(n) space, where n is the length of array.
        ## another way to do it is to use the built-in sort function, which takes O(nlgn) time.
        if self.is_integer:
            highest_item = max(self.array)
            occurance_items = [0] * (highest_item + 1)

            for item in self.array:
                occurance_items[item] += 1

            for item, occurance in enumerate(occurance_items):
                for i in range(occurance):
                    self.sorted_array.append(item)
        
        elif self.is_char:
            self.sorted_array = sorted(self.array)
    
    # -----------------------------------------------------------------------------
    # find consecutive runs according to sort type
    def is_consecutive(self, prev, current):
        
        if self.is_integer:
            return current == prev + 1
    
        if self.is_char:
            return ord(current.lower()) == ord(prev.lower()) + 1  ## compare characters by lowercase
    
    def find_consecutive(self):
        
        if not self.array:
            return None
        
        if self.sorted_array:
            self.sorted_array = []
        self.sort_array()
        consecutive_tuple = []
        prev_item = self.sorted_array[0]
        
        for current_item in self.sorted_array[1:]:
            if self.is_consecutive(prev_item, current_item):
                if not consecutive_tuple:
                    consecutive_tuple.append(prev_item)
                consecutive_tuple.append(current_item)
            else:
                self.consecutive_array.append(consecutive_tuple)
                consecutive_tuple = []
            prev_item = current_item
        
        ## if the last consecutive tuple exists, add it to the consecutive array
        if consecutive_tuple:
            self.consecutive_array.append(consecutive_tuple)
    
    # -----------------------------------------------------------------------------
    # generate an array with a specified indexes, each item being random
    def random_generate(self, indexes, min_value, max_value):
        
        if self.is_integer == True:
            from random import randint
            self.array = [randint(min_value, max_value) for i in range(indexes)]
        elif self.is_char == True:
            from random import choice
            left = self.letters.index(min_value)
            right = self.letters.index(max_value)
            self.array = [choice(self.letters[left:right+1]) for i in range(indexes)]
    
    def generate_array(self, indexes, min_value, max_value):
        
        if not isinstance(indexes, int):
            raise Exception("Requires an integer as the length of array.")
    
        if indexes <= 0:
            raise Exception("The indexes of an array must be larger than 0.")

        if min_value >= max_value:
            raise Exception("Invalid array range.")
        
        if isinstance(min_value, int) and isinstance(max_value, int):
            if not self.is_integer:
                self.is_integer = True
            return self.random_generate(indexes, min_value, max_value)
        
        if isinstance(min_value, str) and isinstance(max_value, str):
            if not self.is_char:
                self.is_char = True
            return self.random_generate(indexes, min_value, max_value)

# -----------------------------------------------------------------------------
# define a class which extends ArrayUtils class
class IntArrayUtils(ArrayUtils):
    
    def __init__(self):
        self.is_integer = True
        self.sum_contents_array = []
        super().__init__()
        
    def remove_duplicates(self):
        super().remove_duplicates()
    
    def sort_array_ascend(self):
        super().sort_array()
    
    def find_consecutive(self):
        super().find_consecutive()
        
    def generate_array(self, indexes, min_value, max_value):
        super().generate_array(indexes, min_value, max_value)

    ## sum the contents of each consecutive array and store each of the results as an item in another array
    def sum_consecutive_tuple(self, c_array):
        for items_tuple in c_array:
            if items_tuple:
                self.sum_contents_array.append(sum(items_tuple))
    
    ## a function that implements auto function calls and prints out results 
    def function_call_stack(self, **user_args):
        self.generate_array(indexes=user_args['indexes'], min_value=user_args['min_val'], max_value=user_args['max_val'])
        self.remove_duplicates()
        self.sort_array_ascend()
        self.find_consecutive()
        self.sum_consecutive_tuple(self.consecutive_array)
        
        print("Auto generating the array...")
        print("orginal array: ", self.array)
        print("duplicates removed array: ", self.unique_array)
        print("sorted array: ", self.sorted_array)
        print("consecutive array: ", self.consecutive_array)
        print("sum of the contents of consecutive array: ", self.sum_contents_array)


# -----------------------------------------------------------------------------
# define a class, which extends ArrayUtils class
class CharArrayUtils(ArrayUtils):
    
    def __init__(self):
        self.is_char = True
        self.char_not_in_consecutive = []
        self.letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        super().__init__()
    
    def remove_duplicates(self):
        super().remove_duplicates()
    
    def sort_array_alphabetical(self):
        super().sort_array()
    
    def find_consecutive(self):
        super().find_consecutive()
    
    def generate_array(self, indexes, min_value, max_value):
        super().generate_array(indexes, min_value, max_value)
    
    ## find all characters from the alphabet that not in the consecutive arrays
    def find_missing_chars(self, c_array):
        char_seen_so_far = []  ## O(n) additional space
        for items_tuple in c_array: ## run time is O(n), where n is the number of consecutive char
            for item in items_tuple:
                if not item in char_seen_so_far:
                    char_seen_so_far.append(item)
        self.char_not_in_consecutive = [char for char in self.letters if not char in char_seen_so_far]
    
    def function_call_stack(self, **user_args):
        
        self.generate_array(indexes=user_args['indexes'], min_value=user_args['min_val'], max_value=user_args['max_val'])
        self.remove_duplicates()
        self.sort_array_alphabetical()
        self.find_consecutive()
        self.find_missing_chars(self.consecutive_array)
        
        print("Auto generating the array...")
        print("original array: ", self.array)
        print("duplicates removed array: ", self.unique_array)
        print("sorted array: ", self.sorted_array)
        print("consecutive array: ", self.consecutive_array)
        print("find missing characters in consecutive array: ", self.char_not_in_consecutive)


def main():
    
    # create a mapper that contains valid user inputs
    type_mapper = {'integers': 1, 'integer': 1, 'int': 1, 'characters': 2, 'character': 2, 'char': 2}
    
    def prompt():
        data_type = input("What's the data type of the array, integers or characters? ")
        return type_mapper[data_type]

    asktoplay = 1
    quit = 0
    
    while asktoplay and not quit:
        try:
            option = prompt()
        except KeyError:
            print("The data type is invalid, please try again.")
            print("Use integers/integer/int for 'int' type, or characters/character/char for 'char' type.")
            try:
                quit = int(input("Quit? (yes:1, no:0)"))
            except ValueError:
                print('Please type 1/0!')
                quit = int(input("Quit? (yes:1, no:0)"))
                continue
            else:
                if quit:
                    sys.exit(0)
                else:
                    continue
        else:
            if option == 1:
                child1 = IntArrayUtils()
                length = int(input("Enter the length of the array: "))
                min_val = int(input("Enter the minimum range of the int array: "))
                max_val = int(input("Enter the maximum range of the int array: "))
                user_args = {'indexes': length, 'min_val': min_val, 'max_val': max_val}
                try:
                    child1.function_call_stack(**user_args)
                except Exception as e:
                    print(e.args)
                    continue
                
            elif option == 2:
                child2 = CharArrayUtils()
                length = int(input("Enter the length of the array: "))
                min_val = input("Enter the minimum range of the char array: ")
                max_val = input("Enter the maximum range of the char array: ")
                user_args = {'indexes': length, 'min_val': min_val, 'max_val': max_val}
                try:
                    child2.function_call_stack(**user_args)
                except Exception as e:
                    print(e.args)
                    continue
 
        try:
            asktoplay = int(input("Replay the program? (yes:1, no:0)"))
        except ValueError:
            print("Please type 1/0!")
            asktoplay = int(input("Replay? (yes:1, no:0)"))

        if asktoplay == 1:
            continue
            
        else:
            print('Bye!')
            sys.exit(0)
        
# -----------------------------------------------------------------------------
# run script

if __name__ == "__main__":
    main()

