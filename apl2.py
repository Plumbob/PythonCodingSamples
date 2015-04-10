"""
Implementation notes:

The following routines were designed with clarity as the main goal, rather than
speed or succinctness.

The original requirement was for get_random_subnet_address() to accept an IPv4
addresses and subnets in dotted-decimal string notation and return a new IPv4 in
dotted-decimal string notation.

To minimize conversions to/from integer lists and dotted-decimal strings, all
other support functions included here were designed to use integer lists
for I/O.  These functions could easily be re-designed to handle either format.

Python's preferred approach is to use polymorphism.  Each function would accept
arguments in either dotted-decimal string or integer list form.

Another approach might be to create two libraries, the first operating exclusively
with integer lists and a second library working with the more human-friendly
dotted-decimal strings.  The dotted-decimal library would simply convert its
arguments into integer lists and call upon the first first library to perform
the work.

"""
import random

NUM_OCTETS     = 4
BITS_PER_OCTET = 8


def dotted_decimal_str_to_list(dotted_decimal_str):
    """
    Convenience function to convert a dotted decimal string to a list of ints.

    Humans prefer passing IP addresses and subnet masks as strings, whereas
    their values are easier to manipulate in Python as a list of ints.
 
    @param str dotted_decimal_str - String in the form "XXX.XXX.XXX.XXX"

    @returns list of NUM_OCTETS integers

    """
    ints = [int(x) for x in dotted_decimal_str.split('.')]

    # Raise an error if too many or too few octets
    num_octets = len(ints)
    if num_octets != NUM_OCTETS:
        err_msg = "Argument 'dotted_decimal_str' contains %d numbers, but should "\
                  "contain exactly %d numbers." % (num_octets, NUM_OCTETS)
        raise ValueError(err_msg)
       
    return ints


def list_to_dotted_decimal_str(int_list):
    """
    Convenience function to convert a list of NUM_OCTETS integers to a dotted
    decimal string.

    Humans prefer passing IP addresses and subnet masks as strings, whereas
    their values are easier to manipulate in Python as a list of ints.

    @param list int_list - List of NUM_OCTETS integers, each within the range
                           0 to 255.

    @returns str dotted_decimal_str - String in the form "XXX.XXX.XXX.XXX"

    @raises ValueError if list does not contain exactly NUM_OCTETS values.

    """
    # Raise error on too many or too few octets
    num_octets = len(int_list)
    
    if num_octets != NUM_OCTETS:
        err_msg = "Argument 'int_list' contains %d integers, but should contain "\
                  "exactly %d integers." % (num_octets, NUM_OCTETS)
        raise ValueError(err_msg)
    
    return ".".join([str(x) for x in int_list])


def get_random_ip_address():
    """
    Return a list of NUM_OCTETS integers in the range 0 to 255.

    @returns list - [int, int, int, int]

    Ex: [26, 62, 88, 244]

    """
    new_ip_list = []
    
    for octet in range(NUM_OCTETS):
        rand_octet = random.getrandbits(BITS_PER_OCTET)
        new_ip_list.append(rand_octet)

    return new_ip_list


def invert_octet(octet):
    """
    Given a integer in range 0 - 255, return its value with all bits logically
    inverted.

    @param int octet - Integer in range 0 to 255.
                       Values > 255 are masked using 0xFF to force them into the
                       range of 0 to 255.)

    @returns int in range 0 - 255

    """
    # Mask off 'octet' to make sure in range 0 to 255.
    norm_octet = octet & 255

    # Invert the bits in norm_octet
    inv_octet = ~norm_octet + 256

    return inv_octet


def mask_ip_address(ip_addr, subnet_mask):
    """
    Given an IPv4 address and a subnet_mask, return the address with the mask applied.

    @param list ip_addr     - IPv4 address represented as a list of NUM_OCTETS integers
                              in the range 0 to 255.
                              Ex: [192, 168, 0, 1]

    @param list subnet_mask - Subnet mask as a list of NUM_OCTETS integers in
                              the range 0 to 255.
                              0 bits indicate values that are allowed to change.
                              1 bits indicate values that must not change.
                              Ex. [255, 255, 255, 0]
                             
    @returns list - New IPv4 address as a list of NUM_OCTETS integers
          
    For example:
        IP: [192, 168, 0, 1]
        Subnet Mask: [255, 255, 254, 0]

        Will return: [192, 168, 0, 0]

    """
    # Perform the masking operations on each octet
    masked_octets = []
    for i in range(NUM_OCTETS):
        masked_octets.append(ip_addr[i] & subnet_mask[i])

    return masked_octets



def get_random_subnet_address(ip_addr, subnet_mask):
    """
    Given an IPv4 address and a subnet mask, generate a random IP which falls within the same subnet.

    @param str ip_addr     - IP address.
                             A string in the form "XXX.XXX.XXX.XXX"
                             Ex: "192.168.0.1"

    @param str subnet_mask - Subnet mask.  0 bits indicate values that are
                             allowed to change.
                             1 bits indicate values that must not change.
                             Ex. "255.255.255.0"
                             
    @returns  str - New, random IP address within the subnet specified.                            

    For example:
        IP: "192.168.0.1"
        Subnet Mask: "255.255.254.0"

        Might return: "192.168.1.217"
        
    """
    # Convert inputs to integer list form to ease operations
    ip_addr_list     = dotted_decimal_str_to_list(ip_addr)
    subnet_mask_list = dotted_decimal_str_to_list(subnet_mask)

    # Use the subnet mask to convert all masked bits in 'ip_addr' to 0.
    # This will lessen the influence of the original 'ip_addr' value on the
    # randomness of our output.
    masked_ip_addr = mask_ip_address(ip_addr_list, subnet_mask_list)

    # Generate a new, random IP address, then mask it with the inverse
    # of 'subnet_mask'
    random_ip_addr        = get_random_ip_address()
    invert_subnet_mask    = [invert_octet(x) for x in subnet_mask_list]
    masked_random_ip_addr = mask_ip_address(random_ip_addr, invert_subnet_mask)

    # OR the two addresses together to create a new, random subnet address
    random_ip_addr = []
    for x,y in zip(masked_ip_addr, masked_random_ip_addr):
        new_octet = x | y
        random_ip_addr.append(new_octet)

    # Convert final result back to dotted decimal form
    return list_to_dotted_decimal_str(random_ip_addr)

    
        
        
