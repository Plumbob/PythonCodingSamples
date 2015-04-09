#
# SendNoticeToLoggedUsers.py
#

"""
Coding challenge:
On a Host that is connected to a LAN, you have a log-file that contains a list
of users who have logged onto some of the machines on the network, in the past 24 hrs.

Write a script that searches for computers on the network that are currently online,
and then sends a text-file to appropriate users on the online computers.

At the end of the run, the script should mark in the log file, computers to
which the file has been transmitted. In the log file, it should also add computers 
that have been discovered in the current traversal, which were not listed originally.

Please specify any assumptions you make and explain how you test your code.

Assumptions:

 - Language: Python 3

 - Time: This is demonstration code that should function but is not expected
   to be complete, full-tested nor production ready.  Error-handling will
   likewise be minimal.

 - Due to lack of specification, a simple text logfile input and output
   format will be used.  A more sophisticated formats, such as database, XML, etc.
   could be used in the future to make manipulation faster, more flexible, etc.

 - Assuming that 'appropriate users' are those listed in the input logfile.

 - Assume that logfile will not be reorganized/sorted, but it is
   acceptable to simply list newly discovered computers into the output logfile.

 - Instead of a text file, this demo will send a simple 'Hello' string.
   
 - For ease of transmission and reading, classes, libraries, etc. that
   would normally be organized into separate files will be located into
   this single file.

Testing:
 - Due to time constraints, I will do only basic testing of this code.
   For more 'durable' programs (ones that will be used in production, or
   more than just 'throw-away' code such as this should have a more
   thorough testing strategy.  This could be as simple as a separate test
   file or as thorough as a test infrastructure such as Pytest, Nose, etc.

"""

class MessageSender():
    """
    Library to send a message to 'user_name' at server 'server_name'.
    Keeps track of 'user_name', 'server_name' pairs to make sure we don't
    send duplicate messages to the same user and the same server.

    To conserve resources and avoid annoying users with multiple messages,
    duplicate messages are not sent.
    
    Dev.Note: This function could be implemented in a variety of different
    ways.  For simplicity here, we will assume the messaging system is fast.
    Here, we will stub this out by printing a message to the console.

    """
    def __init__(self):
        """
        Initialize a MessageSender instance.
        """
        self.message_pairs_sent = set()
        
    def send_message(self, user_name, server_name, message):
        """
        @param str user_name   - Name of user to which to send a message.
        @param str server_name - Name of server to which to send a message.
        @param str message     - Message content.
        
        @returns True if message sent successfully
                 (Never False as message failures are not checke for
                  in this demo.)
        
        """
        if (user_name, server_name) not in self.message_pairs_sent:
            print("Message sent to user '%s' at server '%s'." % (user_name, server_name))
            self.message_pairs_sent.add((user_name, server_name))

        # We're not supporting error-handling here, so we'll assume message
        # transmission failures never happen in this demo.
        return True


def get_online_servers():
    """
    Library function to return a list of server names representing servers that
    are currently online.

    Dev.Note: There are often many servers and they may or may not respond
    quickly.  For these reasons, this function would best be implemented to
    attempt contact with many servers in parallel.
    
    @returns list - List of server names as strings.
                    The return list may be empty.

    """
    return ['server2', 'server3', 'server4', 'server5', 'server6']


def parse_inputfile_entry(entry):
    """

    @returns user_name, server_name as parsed from input logfile record.

    """
    server_name, user_name = entry.split()

    user_name   = user_name.strip()
    server_name = server_name.strip()

    return user_name, server_name
    

if __name__ == "__main__":

    # These could also be passed in as command-line arguments
    INPUTLOG_FILENAME  = "input_logfile.txt"
    OUTPUTLOG_FILENAME = "output_logfile.txt"
    
    # Instantiate a message sender object to send messages and help us to avoid
    # sending duplicate messages
    message_sender = MessageSender()
    
    # Get a list of all servers currently online
    online_servers = get_online_servers()

    # For demonstration purposes, list the servers "found online"
    print("\n")
    print("The following servers were found online:")
    for server in online_servers:
        print("  %s" % server)
    print("")
                    
    # Keep track of the servers we've found in the inputlogfile
    # Any currently online servers not found in the inputlogfile we will add
    # to the output logfile at the end
    servers_in_inputlogfile = set()
    
    # Keep track of messages already sent
    sent_messages = set()

    # Open and close the output logfile automatically
    with open(OUTPUTLOG_FILENAME, 'w') as output_logfile:

        # Process input logfile
        with open(INPUTLOG_FILENAME, 'r') as input_logfile:

            # Read input line by line
            for input_line in input_logfile.readlines():

                # Extract the user_name and server_name
                user_name, server_name = parse_inputfile_entry(input_line)
                
                # If the server is currently online, message the user at that
                # server.
                if server_name in online_servers:
                    message_sender.send_message(user_name   = user_name,
                                                server_name = server_name,
                                                message     = "Hello, %s" % user_name)
                
                    # Note in the output logfile that this user at this server has
                    # already been messaged
                    input_line = input_line.strip() + " messaged\n"
                
                # Write each line to the output logfile
                output_logfile.write(input_line)
                
                # Keep track of server names found in the input logfile.
                # Servers found online but not in the input logfile will be listed
                # at the end of the output logfile.    
                servers_in_inputlogfile.add(server_name)

        # When processing the input logfile is complete, add an entry to the output
        # logfile for each server found currently online but not in the input
        # logfile

        print("")
        for server_name in online_servers:
            if server_name not in servers_in_inputlogfile:
                print("Adding server '%s' to output logfile..." % server_name)
                server_name += "\n"
                output_logfile.write(server_name)
                
        print("")
        print("Done.")

    
    
