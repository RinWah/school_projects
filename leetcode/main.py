class Solution(object):
    def findTheDifference(self, s, t):
        counts = {}
        
        # Part 1: Count letters in s
        for char in s:
            if char in counts:
                counts[char] += 1
            else:
                counts[char] = 1
        
        # Part 2: Look at letters in t
        for char in t:
            # How do we check if 'char' is the extra letter?
            # Hint: Either it's not in the dictionary, 
            # OR its count has already hit 0.
            
            if ___ not in ___ or ___ == 0:
                return char
            else:
                # Subtract 1 from the count so we know we "used" one
                counts[char] -= 1