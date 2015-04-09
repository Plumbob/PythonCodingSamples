# Provides itertools-related functions not available in the Python3 intertools library
# Requires Python3


import itertools

    
def grouper(items, n):
    """
    Collect data into fixed-length chunks or blocks.
    @param itr $items     - List to be split into M N-length chunks
                            If len('items') is not evenly divisible
                            by 'n', the last chunk will be padded with
                            'fillvalue'.

    @param int $n        - Desired length of each chunk/block returned

    @returns - A single tuple, composed of ceil(len(items)/n) sub-tuples

    Note:
    This function will return an empty tuple if 'items' is empty.

    Example usage:
    grouper([1,2,3,4,5,6,7], 3) --> ((1,2,3), (4,5,6), (7, None, None))

    """
    # Dev.Note: This function is adapted from the Python 3.3 itertools doc examples at:
    # https://docs.python.org/3.3/library/itertools.html#itertools.zip_longest

    args = [iter(items)] * n
    generator = itertools.zip_longest(*args, fillvalue=None)
    
    return tuple(generator)


def div_mod(items, n):
    """
    Equivalent of divmod(), but for lists.
    Spit list 'items' into M tuples of N items each.  "Remainder" elements
    are returned in a second tuple.
    
    @param itr $items     - List to be split into M N-length tuples.

    @param int $n         - Desired length of each sub-tuple

    @returns - A two item tuple (quotient, remainder)
               The quotient contains M N-length tuples.
               The remainder contains the "remainder" items when len(items)/n
               is a non-integer value.
               Either or both tuples can be empty

    Example usage:
    grouper([1,2,3,4,5,6,7], 3) --> ((1,2,3), (4,5,6)), (7,)

    """

    # Pre-process arguments to handle corner cases:
    if (not items) or (n == 0):
        quotient_tuple = ()
        remainder_tuple = ()
        return quotient_tuple, remainder_tuple

    
    # Split 'items' into M N-element tuples.  If 'items' doesn't split evenly
    # into 'n' chunks, the last typle will be padded with None values
    groups = grouper(items, n)

    # Split result into "quotient" and "remainder" tuples.
    # The "quotient" tuple will contain M sub-tuples contain of N elements each.
    # The "remainder" typle will contain all "leftover" values, if any
    # Either or both tuples can be empty
    num_items = len(items)

    quotient, remainder = divmod(num_items, n)

    # No quotient values, just remainders
    if quotient == 0:
        quotient_tuple = ()
        remainder_tuple = groups[0]

    # Even split, no remainders
    elif remainder == 0:
        quotient_tuple = groups
        remainder_tuple = ()

    # Both quotients and remainders
    else:
        quotient_tuple = groups[:-1]
        remainder_tuple = groups[-1]

    # Remove any None entries from remainder tuple
    if remainder_tuple:
        remainder_tuple = tuple(filter(lambda x: x is not None, remainder_tuple))
        
    return quotient_tuple, remainder_tuple



    
if __name__ == '__main__':

    import math

    print("\n")
    print("Running self-tests")
    print("==================")
    print("\n")

    
    # ==========================================================================
    # Test grouper()
    # ==========================================================================
    print("Testing grouper()")
    print("-----------------")

    #
    # Given an empty list, verify grouper() will return an empty tuple
    #
    print("Verify grouper([],x) returns empty tuple...", end="")

    return_val = grouper([], 3)
    if return_val != ():
        print("\n")
        print("FAIL: returned %r" % (return_val,))
        print("FAIL: expected: ()")
    else:
        print("PASS")

    #
    # Verify grouper splits into correct number of sub-tuples
    #
    test_list    = [1,2,3,4,5,6,7]
    test_modulus = 3
    expected_number_of_subtuples = math.ceil(len(test_list) / test_modulus)

    print("Verify grouper(%r, %d) returns correct number of sub-tuples..."
          % (test_list, test_modulus), end="")

    return_val = grouper(test_list, test_modulus)

    if len(return_val) != expected_number_of_subtuples:
        print("\n")
        print("FAIL: grouper(%r, %r) returned %r" % (test_list, test_modulus, return_val))
        print("FAIL: expected %d sub-tuples, not %d" % (expected_number_of_subtuples,
                                                       len(return_val)))
    else:
        print("PASS")

    #
    # Verify grouper doesn't re-arrange items in the original list
    #
    test_list    = [1,2,3,4,5,6,7]
    test_modulus = 3
    
    print("Verify grouper(%r, %d) does not rearrange items when splitting into "
          "sub-tuples..." % (test_list, test_modulus), end="")

    return_val = grouper(test_list, test_modulus)

    # Unsplit back into a single tuple
    unsplit_tuple = itertools.chain(*return_val)
    
    # Remove any Nones that might have been inserted by grouper()
    unsplit_list = list(filter(lambda x : x is not None, unsplit_tuple))
    
    if unsplit_list != test_list:
        print("\n")
        print("FAIL: grouper(%r, %r) rearranged list items" % (test_list, test_modulus))
        print("FAIL: received: %r" % unsplit_list)
        print("FAIL: expected: %r" % test_list)

    else:
        print("PASS")

        
    # ==========================================================================
    # Test div_mod()
    # ==========================================================================
    print("\n")
    print("Testing div_mod()")
    print("-----------------")

    #
    # Given an empty list, verify div_mod() will return two empty
    # tuples
    #
    print("Verify div_mod([],x) returns (), ()...", end="")

    quot, rem = div_mod([], 3)
    if not quot and not rem:
        print("PASS")
    else:
        print("\n")
        print("FAIL: returned %r" % (quotient, remainder))
        print("FAIL: expected: (), ()")

    #
    # Verify div_mod when quotient is zero, remainder is non-zero
    #
    test_list    = [1]
    test_modulus = 3
  
    expected_quot = ()
    expected_rem  = (1,)

    print("Verify div_mod(%r, %d) returns %r, %r..."
          % (test_list, test_modulus, expected_quot, expected_rem), end="")
  
    quot, rem = div_mod(test_list, test_modulus)

    if ((quot != expected_quot) or
       (rem  != expected_rem)):
        print("\n")
        print("FAIL: div_mod(%r, %r) returned %r, %r"
              % (test_list, test_modulus, quot, rem))
        print("FAIL: expected %r %r" % (expected_quot, expected_rem))
    else:
        print("PASS")
 

    #
    # Verify div_mod when quotient non-zero, remainder is zero
    #
    test_list    = [1,2,3,4,5,6]
    test_modulus = 3
  
    expected_quot = ((1,2,3),(4,5,6))
    expected_rem  = ()

    print("Verify div_mod(%r, %d) returns %r, %r..."
          % (test_list, test_modulus, expected_quot, expected_rem), end="")
  
    quot, rem = div_mod(test_list, test_modulus)

    if ((quot != expected_quot) or
       (rem  != expected_rem)):
        print("\n")
        print("FAIL: div_mod(%r, %r) returned %r, %r"
              % (test_list, test_modulus, quot, rem))
        print("FAIL: expected %r %r" % (expected_quot, expected_rem))
    else:
        print("PASS")
 


    #
    # Verify div_mod when both quotient and remainder are non-zero
    #
    test_list    = [1,2,3,4,5,6,7]
    test_modulus = 3
  
    expected_quot = ((1,2,3),(4,5,6))
    expected_rem  = (7,)

    print("Verify div_mod(%r, %d) returns %r, %r..."
          % (test_list, test_modulus, expected_quot, expected_rem), end="")
  
    quot, rem = div_mod(test_list, test_modulus)

    if ((quot != expected_quot) or
       (rem  != expected_rem)):
        print("\n")
        print("FAIL: div_mod(%r, %r) returned %r, %r"
              % (test_list, test_modulus, quot, rem))
        print("FAIL: expected %r %r" % (expected_quot, expected_rem))
    else:
        print("PASS")
 










        
 #   # Verify grouper doesn't re-arrange items in the original list
 #   #
 #   test_list    = [1,2,3,4,5,6,7]
 #   test_modulus = 3
 #   
 #   print("Testing grouper(%r, %d) does not rearrange items when splitting into "
 #         "sub-lists..." % (test_list, test_modulus), end="")
 #
 #   return_val = grouper(test_list, test_modulus)
 #
 #   # Unsplit back into a single list
 #   unsplit_list = itertools.chain(*return_val)
 #   
 #   # Remove any Nones that might have been inserted by grouper()
 #   unsplit_list = list(filter(lambda x : x is not None, unsplit_list))
 #   
 #   if unsplit_list != test_list:
 #       print("\n")
 #       print("FAIL: grouper(%r, %r) rearranged list items" % (test_list, test_modulus))
 #       print("FAIL: received: %r" % unsplit_list)
 #       print("FAIL: expected: %r" % test_list)
 #
 #   else:
 #       print("PASS")
 
   
   


