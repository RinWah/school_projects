class Solution(object):
    def findTheDifference(self, s, t):
        # --- YOUR LOGIC GOES HERE ---
        for char in s: 
            for cha in t:
                if char != cha:
                    break
        # Remember to return a string
        return char
        pass

# This part stays the same regardless of your logic
if __name__ == "__main__":
    sol = Solution()
    
    # Test Case 1
    s1, t1 = "abcd", "abcde"
    print(f"Test 1 - Expected: 'e', Got: '{sol.findTheDifference(s1, t1)}'")
    
    # Test Case 2
    s2, t2 = "", "y"
    print(f"Test 2 - Expected: 'y', Got: '{sol.findTheDifference(s2, t2)}'")