# Creates routing info for the SH challenge
# Requires Python3

import itertools_ext_lib

SUPER_BASE_IP  = "10.0.4."
LARGE_BASE_IP  = "10.0.3."
MEDIUM_BASE_IP = "10.0.2."
SMALL_BASE_IP  = "10.0.1."

def binner(items):
    """
    Given a list of N items, split the elements of 'items' into 'bins' of the following
    sizes (lengths): 25, 10, 5, 1

    @param list items - list of N items

    @returns four tuples:
        tuple of subtuples of 25 elements each
        tuple of subtuples of 10 elements each
        tuple of subtuples of  5 elements each
        tuple of single elements

    Note: Any or all of the returned sub-tuples can be empty
    
    Preference is given to larger bins.  The subtuples assigned to each bin will
    consist of exactly bin_size sub-items.

    Examples:
        binner(range(30)) -> [[0,1,2,...24],],
                             [],
                             [[25,26,27,28,29]],
                             []

        binner(range(51)) -> [[0,1,2,...24],
                              [25,26,27,...49]],
                             [],
                             [],
                             [50]

        binner(range(13)) -> [],
                             [0,1,2,3...9],
                             [],
                             [10,11,12]

    """

    # Split items into the largest bin first, splitting remainders into progressively
    # smaller bins.
    bin_25, remainder = itertools_ext_lib.div_mod(items,     25)
    bin_10, remainder = itertools_ext_lib.div_mod(remainder, 10)
    bin_5,  remainder = itertools_ext_lib.div_mod(remainder,  5)
    bin_1,  remainder = itertools_ext_lib.div_mod(remainder,  1)

    return bin_25, bin_10, bin_5, bin_1


def get_routes(recipients):
    """
    Convert the list of recipient phone numbers to a dictionary of routes.

    @param list recipients - List of recipient phone numbers

    @returns dict - List of route dictionaries in the following format:

        {
            "ip": "10. 0. 1. 1",  # Small (1 pkt/transaction)
            "recipients": ["+15555555591"]
        },
        {
            "ip": "10. 0. 2. 1",  # Medium (5 pkts/transaction)
            "recipients": ["+15555555590", "+15555555589", "+15555555588",
                           "+15555555587", "+15555555586"]
        },
        {
            "ip": "10. 0. 3. 1",  # Large (10 pkts/transaction)
            "recipients": ["+15555555585", "+15555555584", "+15555555583",
                           "+15555555582", "+15555555581", "+15555555580",
                           "+15555555579", "+15555555578", "+15555555577",
                           "+15555555576"]
        },
        {
            "ip": "10. 0. 4. 1",  # Super (25 pkts/transaction)
            "recipients": ["+15555555575", "+15555555574", "+15555555573",
                           "+15555555572", "+15555555571", "+15555555570",
                           "+15555555569", "+15555555568", "+15555555567",
                           "+15555555566", "+15555555565", "+15555555564",
                           "+15555555563", "+15555555562", "+15555555561",
                           "+15555555560", "+15555555559", "+15555555558",
                           "+15555555557", "+15555555556", "+15555555555",
                           "+15555555554", "+15555555553", "+15555555552",
                           "+15555555551"]
        }

    """
 
    
    bin25, bin10, bin5, bin1 = binner(recipients)

    route_list = []
    
    # Iterate through the "25/Super" bin, creating dictionary entries
    # add adding them to the route list
    for index, block in enumerate(bin25):
        ip_addr = SUPER_BASE_IP + "%d" % (index+1)
        sub_dict = {}
        sub_dict['ip'] = ip_addr

        sub_dict['recipients'] = list(block)

        route_list.append(sub_dict)

    # Iterate through the "10/Large" bin, creating dictionary entries
    # add adding them to the route list
    for index, block in enumerate(bin10):
        ip_addr = LARGE_BASE_IP + "%d" % (index+1)
        sub_dict = {}
        sub_dict['ip'] = ip_addr

        sub_dict['recipients'] = list(block)

        route_list.append(sub_dict)

    # There will never be more than 1 entry in the 5/Medium bin.
    # If an entry exists, add it to the route list
    if bin5:
        sub_dict = {}
        sub_dict['ip'] = MEDIUM_BASE_IP + "1"
        sub_dict['recipients'] = bin5[0]

        route_list.append(sub_dict)

    # Iterate through the "1/Small" bin, creating dictionary entries
    # add adding them to the route list
    for index, block in enumerate(bin1):
        ip_addr = SMALL_BASE_IP + "%d" % (index+1)
        sub_dict = {}
        sub_dict['ip'] = ip_addr

        sub_dict['recipients'] = list(block)

        route_list.append(sub_dict)

    return route_list


    
   
if __name__ == '__main__':

    import sys

    #
    # Automatically test binner() if started from command line
    #

    MAX_LIST_LEN_TO_TEST = 500

    for num_items in range(0,MAX_LIST_LEN_TO_TEST):
        items = range(num_items)
        b25, b10, b5, b1 = binner(items)

        exp_num_bin25_entries, rem = divmod(num_items, 25)
        exp_num_bin10_entries, rem = divmod(rem, 10)
        exp_num_bin5_entries,  rem = divmod(rem, 5)
        exp_num_bin1_entries       = rem


        print("num_items = %d" % num_items)
        print("--------------")

        # Check number of sub-tuples in bin25
        print("b25 ", end="")
        if len(b25) == exp_num_bin25_entries:
            print("PASS: ", end="")
        else:
            print("FAIL: number of tuples in Bin 25 = %d" % len(bin25))
            print("FAIL: expected %d" % exp_num_bin25_entries)
            sys.exit(1)

        # verify each bin25 sub-tuple contains exactly 25 items
        for subtuple in b25:
            if len(subtuple) == 25:
                print("PASS ", end="")
            else:
                print("FAIL: bin25 sub-tuple contains %d items" % len(subtuple))
                print("FAIL: expected 25")
                sys.exit(1)
              
        print()

        
       # Check number of sub-tuples in bin10
        print("b10 ", end="")
        if len(b10) == exp_num_bin10_entries:
            print("PASS: ", end="")
        else:
            print("FAIL: number of tuples in Bin 10 = %d" % len(bin10))
            print("FAIL: expected %d" % exp_num_bin10_entries)
            sys.exit(1)

        # verify each bin10 sub-tuple contains exactly 10 items
        for subtuple in b10:
            if len(subtuple) == 10:
                print("PASS ", end="")
            else:
                print("FAIL: bin10 sub-tuple contains %d items" % len(subtuple))
                print("FAIL: expected 10")
                sys.exit(1)
              
        print()


       # Check number of sub-tuples in bin5
        print("b5 ", end="")
        if len(b5) == exp_num_bin5_entries:
            print("PASS: ", end="")
        else:
            print("FAIL: number of tuples in Bin 5 = %d" % len(bin5))
            print("FAIL: expected %d" % exp_num_bin5_entries)
            sys.exit(1)

        # verify each bin5 sub-tuple contains exactly 5 items
        for subtuple in b5:
            if len(subtuple) == 5:
                print("PASS ", end="")
            else:
                print("FAIL: bin5 sub-tuple contains %d items" % len(subtuple))
                print("FAIL: expected 5")
                sys.exit(1)
              
        print()

       # Check number of sub-tuples in bin1
        print("b1 ", end="")
        if len(b1) == exp_num_bin1_entries:
            print("PASS: ", end="")
        else:
            print("FAIL: number of tuples in Bin 1 = %d" % len(bin1))
            print("FAIL: expected %d" % exp_num_bin1_entries)
            sys.exit(1)

        # verify each bin1 sub-tuple contains exactly 1 items
        for subtuple in b1:
            if len(subtuple) == 1:
                print("PASS ", end="")
            else:
                print("FAIL: bin1 sub-tuple contains %d items" % len(subtuple))
                print("FAIL: expected 1")
                sys.exit(1)
              
        print()



        
        print("\n")
    
        
 #       print("%d %d %d %d %d"
 #             % ( num_items,
 #                 exp_num_bin25_entries,
 #                 exp_num_bin10_entries,
 #                 exp_num_bin5_entries,
 #                 exp_num_bin1_entries))

        
