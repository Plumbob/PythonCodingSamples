

def simple_caesar_cypher(input_str, shift_mag):
    """
    A simple implementation of a Caesar text cypher.  Input text is rotated 'shift_mag'
    characters to the right.

    @param str input_str - Any string.  Only lower-case chars 'a'-'z' are shifted.
                           All other characters are passed unchanged.

    @param int shift_mag - Magnitude of the shift.
                           In range 0 - 25.

    """

    ORD_A = ord('a')
    ORD_Z = ord('z')
    RANGE = ORD_Z - ORD_A

    # Make sure 'shift_mag' in range 'a-z' (0-25)
    offset = shift_mag % RANGE

    output_str = ""
    
    # Iterate through the input string
    for c in input_str:

        # Convert 'c' to it's ordinal value to each processing
        ord_c = ord(c)
        
        # Only translate characters in the range 'a' - 'z', pass all others
        # untouched.
        if ord_c in range(ORD_A, ORD_Z + 1):

            # Calculate the new character value
            new_ord_c = ord_c + offset
            
            # "Roll" back around to 'a' if our result is greater than 'z'
            if new_ord_c > ORD_Z:
                new_ord_c = new_ord_c - RANGE - 1

            # Convert back to char before
            output_str += chr(new_ord_c)

        # Pass on character unchanged
        else:
            output_str += c

    return output_str
