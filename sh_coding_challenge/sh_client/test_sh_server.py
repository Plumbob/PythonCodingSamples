# Test the server created for the SH challenge
# Requires Python3

import subprocess
import shlex
import requests
import json

SERVER_URI = "http://localhost:5000/route"
#SERVER_URI = "http://71.198.20.93:5000/route"

# Default request payload message value
MESSAGE = "SH Rocks"

# Request payload before addition of 'recipients'
BASE_PAYLOAD = {'message': MESSAGE}

 
def shell_cmd(cmdln):
    """
    Pass 'cmdln' to the shell and return the response.

    @param str $cmdln - Full string to be passed to the shell command line.

    @returns response as single string

    """
    commands = shlex.split(cmdln)

    return_val= subprocess.check_output(commands,
                                        shell              = False,
                                        universal_newlines = True,
                                        timeout            = None)

    return return_val


def send_via_curl(dictionary):
    """
    Convert dictionary to json format and send to SHChallenge server
    via curl.

    @param dict $dictionary

    @returns string containing curl response

    """
    curl_cmd_template = 'curl -i -H "Content-Type: application/json"'\
                        ' -X POST -d \'%s\' {0}'.format(SERVER_URI)

    json_str = json.dumps(dictionary)

    cmdln = curl_cmd_template % json_str

    try:
        response = shell_cmd(cmdln)
    except subprocess.CalledProcessError as exc:
        print("ERROR: Unable to contact SH Challenge server at %s."
              % SERVER_URI)
    else:
        return response

    
def send_via_requests(dictionary):
    """
    Convert dictionary to json format and send to SHChallenge server.

    @param dict $dictionary 

    @returns dict - response as a Python dictionary

    """
    headers = {'content-type': 'application/json'}

    r = requests.post(SERVER_URI, json=dictionary, headers=headers)

    response = r.json()

    return response

    
def build_recipient_list(num):
    """
    Return a list of 'num' imaginary telephone number strings.

    @param int $num - Number of telephone number strings to generate.

    @returns list  - list of 'num' telephone number strings
                     Each string is of the form '+1555555xxxx', where
                     'xxxx' is an incrementing value.

    Note: These numbers are not intended to be valid US telephone numbers.

    Example:
      build_recipients(5) -> ['+15555550000','+15555550001','+15555550002',
                              '+15555550003','+15555550004'] 

    """
    BASE = "+1555555"
    numbers = []

    for index in range(num):
        number = BASE + "%04d" % index
        numbers.append(number)

    return numbers


def build_test_payload(num_recipients):
    """
    Create a test payload.

    @num_recipients int $num_recipients - Number of recipient telephone numbers
                                          to be created.  Creates a list
                                          of 'num_recipients' fake telephone
                                          numbers.
    @returns dict - Valid input to SH server, ready to be converted to
                    json format.

    Example output for 'num_recipients' == 6:
        {
            "message": "SH Rocks",
            "recipients": ["+15555555556", "+15555555555", "+15555555554",
                           "+15555555553", "+15555555552", "+15555555551"]
        }
        
    """
    payload = BASE_PAYLOAD
    payload['recipients'] = build_recipient_list(num_recipients)

    return payload


def verify_num_entries_in_route(expected, actual):
    """
    Verify the number of telephone number present in a route matches the number expected
    for that route type.

    @param int $expected - Number of telephone numbers the route type is supposed
                           to contain.

    @param int $actual   - The number of telephone numbers actually contained in
                           the route.

    Side-effects:
        - Prints test message to console
        - sys.exit() if actual value does not match the expected value

    """
    print("Expected %d routes, received %d..."
           % (expected, actual), end="")
    
    if expected == actual:
        print("PASS")
    else:
        print("FAIL")
        sys.exit(1)
                               

def verify_routes(num_recipients, routes):
    """
    Verify the json response received from the SH router.

    @param int  $num_recipients - Total number of phone numbers sent to the
                                  SH server in the transaction.

    @param dict $routes_json    - routes dictionary as received from the SH
                                  server.

    Side-effects - Prints testing messages to screen.  Stops at first failure.
    
    Checks the number of route types, as well as the number of
    routes within each route type.

    """
    SIZEOF_BIN25 = 25 # Super
    SIZEOF_BIN10 = 10 # Large
    SIZEOF_BIN5  =  5 # Medium
    SIZEOF_BIN1  =  1 # Small

    SUPER_SUBNET_NUM  = 4   # IP 10.0.4.x
    LARGE_SUBNET_NUM  = 3   # IP 10.0.3.x
    MEDIUM_SUBNET_NUM = 2   # IP 10.0.2.x
    SMALL_SUBNET_NUM  = 1   # IP 10.0.1.x

       # Calculate the expected number of routes
    exp_num_bin25_entries, rem = divmod(num_recipients, SIZEOF_BIN25)
    exp_num_bin10_entries, rem = divmod(rem, SIZEOF_BIN10)
    exp_num_bin5_entries,  rem = divmod(rem, SIZEOF_BIN5)
    exp_num_bin1_entries       = rem

    num_super_routes  = 0   # IP 10.0.4.x
    num_large_routes  = 0   # IP 10.0.3.x
    num_medium_routes = 0   # IP 10.0.2.x
    num_small_routes  = 0   # IP 10.0.1.x
    

    for route in routes:
        # Determine route type by 3rd digit of IP address
        ip = route['ip']
        third_ip_digit = ip.split('.')[2]
        third_ip_digit = int(third_ip_digit,10)

        # Count by route type
        if third_ip_digit == SUPER_SUBNET_NUM:
            verify_num_entries_in_route(SIZEOF_BIN25, len(route['recipients']))
            num_super_routes += 1
            
        elif third_ip_digit == LARGE_SUBNET_NUM:
            verify_num_entries_in_route(SIZEOF_BIN10, len(route['recipients']))
            num_large_routes += 1

        elif third_ip_digit == MEDIUM_SUBNET_NUM:
            verify_num_entries_in_route(SIZEOF_BIN5, len(route['recipients']))
            num_medium_routes += 1

        elif third_ip_digit == SMALL_SUBNET_NUM:
            verify_num_entries_in_route(SIZEOF_BIN1, len(route['recipients']))
            num_small_routes += 1

        # IP error
        else:
            print("FAIL: Invalid IP number: %s" % ip)
            sys.exit(1)

    #
    # Verify we got the expected number of each route type
    #

    #
    # Super/25 routes
    print("Expected %d Super routes, received %d..."
           % (num_super_routes, exp_num_bin25_entries), end="")
    
    if num_super_routes == exp_num_bin25_entries:
        print("PASS")
    else:
        print("FAIL")
        sys.exit(1)
        
    #
    # Large/10 routes
    print("Expected %d Large routes, received %d..."
           % (num_large_routes, exp_num_bin10_entries), end="")
    
    if num_large_routes == exp_num_bin10_entries:
        print("PASS")
    else:
        print("FAIL")
        sys.exit(1)

    #
    # Medium/5 routes
    print("Expected %d Medium routes, received %d..."
           % (num_medium_routes, exp_num_bin5_entries), end="")
    
    if num_medium_routes == exp_num_bin5_entries:
        print("PASS")
    else:
        print("FAIL")
        sys.exit(1)

    #
    # Small/1 routes
    print("Expected %d Small routes, received %d..."
           % (num_small_routes, exp_num_bin1_entries), end="")
    
    if num_small_routes == exp_num_bin1_entries:
        print("PASS")
    else:
        print("FAIL")
        sys.exit(1)


    
if __name__ == '__main__':

    # ==========================================================================
    # Test SH server
    # ==========================================================================
    print()
    print("Testing SH server...")
    print("====================")

    NUM_TESTS = 30
    
    for num_recipients in range(1, NUM_TESTS+1):

        print("")
        msg = "%d-recipient test" % num_recipients
        print(msg)
        print("-" * len(msg))
        print("")
        
        #
        # Verify 'message' field
        #
        exp_message = MESSAGE
        print("Verify 'message' = '%s'... " % exp_message, end="")

        payload = build_test_payload(num_recipients)
        
        response = send_via_requests(payload)
        message = response['message']
    
        if message == exp_message:
             print("PASS")
        else:
            print("\n")
            print("FAIL: returned: %s" % message)
            print("FAIL: expected: %s" % MESSAGE)

        #
        # Verify routes
        #
        routes = response['routes']
        verify_routes(num_recipients=num_recipients, routes=routes)

    

    
 

