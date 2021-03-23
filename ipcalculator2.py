from itertools import takewhile # for use in get supernet function

def class_finder(ipv4):
    ip = ipv4.split('.')
    if int(ip[0]) in range(0,128): # use range function of first index in each ip address to determine their classes.
        class1 = 'A'
        
    elif int(ip[0]) in range(128,192):
        class1 = 'B'

    elif int(ip[0]) in range(192,223):
        class1 = 'C'
        
    elif int(ip[0]) in range(224,240):
        class1 = 'D'
        
    else:
        class1 = 'E'
    return class1

def get_class_stats(ipv4): # fix this so that it only returns it for each class type 

    classes={
    'A':{
    'network_bits':7 ** 2,
    'host_bits':2 ** 24,
    'prefix': '0'

    },
    'B':{
    'network_bits':2 ** 14,
    'host_bits':2 ** 16,
    'prefix': '10'
    },
    'C':{
    'network_bits':2 ** 21,
    'host_bits':2 ** 8,
    'prefix': '110'
    },
    'D':{
    'network_bits':'N/A',
    'host_bits':'N/A',
    'prefix': '1110'
    },
    'E':{
    'network_bits':'N/A',
    'host_bits':'N/A',
    'prefix': '1111'
    },
    }

    classf = class_finder(ipv4)
    for key,value in classes.items():
        if classf == key: # if it is equal to class in dictionary 
            prefix = value['prefix'] # getting the first digit of the prefix
            address1 = prefix + (32 - (len(prefix))) * '0' # multiplying remainder of prefix by 0 to get first address
            address2 = prefix + (32 - (len(prefix))) * '1' # multiplying remainder of prefix by 1 to get last address

            first_address = []
            for index in range(0, len(address1),8):
                first_address.append(address1[index:index + 8]) # adding to a list

            last_address = []
            for index in range(0, len(address2),8):
                last_address.append(address2[index:index + 8]) # adding to a list so that each index in the list has length 8
            faddress = to_decimal_dot(first_address) # converts to decimal and '.' added
            laddress = to_decimal_dot(last_address) # # converts to decimal and '.' added
            return ('Class: {}\nNetwork: {}\nHost: {}\nFirst Address: {}\nLast Address: {}\n'.format(key,value['network_bits'], value['host_bits'],faddress,laddress))


def get_CIDR(submask):

    submask_to_bin = to_binary_string(submask) # FOR CLASS C functionality.

    CIDR = 0 # to see how many bits are turned on to get the CIDR of the subnet mask
    for item in submask_to_bin:
        for i in item:
            if i == '1': # if its equal to 1 then CIDR is increaded by 1 to get the CIDR number
                CIDR += 1
        
    return CIDR
def get_subnet_num(ip_addr,submask):
    
    submask_to_bin = to_binary_string(submask)
    #print(submask_to_bin)
   
    cidr = get_CIDR(submask)

    submask_bin_classC = submask_to_bin[-1] # for class C for counting bits that are 1
    submask_bin_classB = submask_to_bin[-2:] # for class B ^
    

    

    classf = class_finder(ip_addr) # to determine what class it is
    if classf == 'C':
        bits = submask_bin_classC # determining which submask variable to use as C only uses -1 but B uses last 2 bytes.
    else: # if its class B
        bits = ''.join(submask_bin_classB)  # putting the bits as a string 

    subnets = 0 # initialising subnets total at 0
    for n in bits:
        if n == '1': # if bytes are 1
            subnets += 1    

    subnet2 = 2 ** subnets# multiplying the subnet by the power of 2 to get the total subnet number
    return subnet2

    

def addressable_hosts(ip_addr,submask):

    submask_to_bin = to_binary_string(submask) # converting submask to binary to see what bits are turned on.
    classf = class_finder
    last_item_classc = submask_to_bin[-1] # class C last item
    last_item_classb = submask_to_bin[-2:] # for class B which uses last 2 bytes of submask
    

    borrow = 0
    if classf == 'C': # determining which classs it is
        last_item = last_item_classc
    else: # if its class b
        last_item = last_item_classb 
        last_item = ''.join(last_item) #joining bytes 3 and 4 together to get the unmasked bytes as a string

    for n in last_item:
        if n == '0': # if bits are 0
            borrow += 1 #unmasked bits

    address_hosts = (2 ** borrow) - 2 # calculation to get addressable hosts number
    return address_hosts


def get_valid_subnets(ip_addr,submask): # have to finish this off i think i just add 64 each time

    subnets = get_subnet_num(ip_addr,submask) # getting number of subnets
    submask_li = submask.split('.') # splitting the submask at '.'
    CIDR = get_CIDR(submask)

    byte = 0
    for i, item in enumerate(submask_li):
        if item != '255' and item != '0': # making sure that the byte isnt 255 or 0 which works for both class c and b adddress
                                        # ass class b has 2 host addresses and class C only has one host address in the submask
            byte = item # if it isnt then the i is equal to the byte.
            current_byte_position = int(i)
   
    #print(get_valid_subnets("136.206.16.0", "255.255.255.192"))
    #print(get_subnet_stats("172.16.0.0","255.255.192.0"))

    block_size = 256 - int(byte) # getting increment number
    valid_subnets = []

    classf = class_finder(ip_addr) # finding the class
                                  # because online it said class B address start counting at X.X.0.0 and 
                                  #the third octet for 
                                  # class B needs to be 0 for when the block size is added to it.
    if classf == 'B':
        ip_addr = ip_addr.split('.')
        ip_addr[-2] = '0'
        ip_addr = '.'.join(ip_addr)

    #CIDR = get_CIDR(submask)

    for i in range(subnets): 
        
            valid_subnets.append(ip_addr) # appending it to valid subnets list
            ip_addr = ip_addr.split('.') # splitting at '.'

            if classf == 'C': # if its class C 
                end_bit = int(ip_addr[-1]) + block_size # block size is added to -1
                if end_bit < 256:
                    ip_addr[-1] = str(end_bit)

            else: # what i made for calculating class b
                current = int(ip_addr[current_byte_position]) + block_size # takes position of byte in submask and adds to block size
                #current = 0 # resetting current to 0
                if current < 256: # if its less than 256
                    current = int(ip_addr[current_byte_position]) + block_size
                    end_bit = int(ip_addr[current_byte_position]) + block_size # it is added to the current byte position in the ip address
                    ip_addr[current_byte_position] = str(end_bit)
                else:
                    prev = int(ip_addr[current_byte_position - 1]) # getting previous byte before current byte
                    current = 0

                    ip_addr[current_byte_position] = str(current) # resetting current position back to 0


                    end_bit = int(ip_addr[current_byte_position - 1]) + 1 # initialising end bit
                    if end_bit < 256:
                        ip_addr[current_byte_position - 1] = str(end_bit) # if its less 256 then covert prev position  
                
            ip_addr = ".".join(ip_addr) # joining again so that when it goes through the for loop again it'll increment the blocksize number to the chosen index depending on what class it is.

    return valid_subnets # returning the list of valid subnets

def get_broadcast_address(ip_addr,submask):

    submask_list = submask.split('.')
    classf = class_finder(ip_addr) # finding IP address class
    subnets = get_subnet_num(ip_addr,submask) # calling subnet function i made to
    #submask_li = submask.split('.')[-1] # split the submask into lists
    
    valid_subnets = get_valid_subnets(ip_addr,submask)
    if classf == 'C':
        byte  = submask.split('.')[-1] # IF CLASS C split the submask into lists to get the -1 index in the list
        block_size = 256 - int(byte)
    else:
        byte = 0
        for i, item in enumerate(submask_list):
            if item != '255' and item != '0': # making sure that the byte isnt 255 or 0 which works for both class c and b adddress
                                        # ass class b has 2 host addresses and class C only has one host address in the submask
                byte = item # if it isnt then the i is equal to the byte.
                current_byte_position = int(i)
                block_size = 256 - int(byte)
    

    broadcast_address = list()
    
    for i in valid_subnets:
        address = i.split('.')
        if classf == 'C': # checking to see if its class C
            end = str(int(address[-1]) + (block_size - 1))  # minusing -1 from the block size each time
            address[-1] = end

        else: # otherwise it'll be class B
            end = str(int(address[-2]) + (block_size - 1))
            if current_byte_position == 2: #255 on broadcast addressees depend on the byte position in the submask. If its byte 2(as i have it in a list) but outside of list it'll be 3 then the position next to that in the submask will be 0 so i assign 255 to it.
                address[-1] = '255'
            address[-2] = end # takes -1 of last address and changes it to end variable
        address = ".".join(address) # joining again so for when it goes through the for loop again. Same as valid subnets
        
        broadcast_address.append(address) # appending to list.

    return broadcast_address
def get_first_address(ip_addr, submask):

    valid_subnets = get_valid_subnets(ip_addr,submask) # calls valid subnets function 

    first_address = []

    for i in valid_subnets:
        address = i.split('.') # splits string at '.'
        end = str(int(address[-1]) + 1) # adding 1 to the index - 1 each time it iterates through the valid subnets list to create the first address list
        address[-1] = end # initialising address[-1] as 'end' so that this is changed each time
        address = ".".join(address) # joining the splitted string with '.'
        first_address.append(address)
    return first_address # returning list of first addresses.

    
    
def get_last_address(ip_addr, submask): # GETTING LAST ADDRESS

    classf = class_finder(ip_addr)
    submask_list = submask.split('.')
    if classf == 'C':
        block_size = submask.split('.')[-1] # split the submask into lists to get the last int in the list
    else:
        byte = 0
        for i, item in enumerate(submask_list):
            if item != '255' and item != '0': # making sure that the byte isnt 255 or 0 which works for both class c and b adddress
                                        # ass class b has 2 host addresses and class C only has one host address in the submask
                byte = item # if it isnt then the i is equal to the byte.
                current_byte_position = int(i)
                block_size = 256 - int(byte)
    last_address = []

    if classf == 'C':
        broad_addr = get_broadcast_address(ip_addr,submask) # calling broadcast address to get list of broadcast addresses
        #print(broad_addr)
        for i in broad_addr:
            address = i.split('.')
            end = str(int(address[-1]) - 1) # for loop that goes through each index in the list and each address it'll minus 1 off of index -1
            address[-1] = end
            address = ".".join(address)
            last_address.append(address) # appending to list
    else: # IF IP ADDRESS IS CLASS B
        last_addr = get_broadcast_address(ip_addr,submask) # going to get this via using the subnet number and valid subnets 
        for i in last_addr:
            
            address = i.split('.')
            end = str(int(address[-1]) - 1) # subtracting index -1 by 1
            address[-1] =  end # if its class C index -1 will always be 254
            address = ".".join(address)
            last_address.append(address) # appending to list

    return last_address

     

def get_subnet_stats(ip_addr,subnet_mask): #PART 2

    
    # in this function im just calling all previous functions that I created to get the desired results and calling
    # them here to print the data.

    CIDR = get_CIDR(subnet_mask)
    subnets = get_subnet_num(ip_addr,subnet_mask)
    hosts = addressable_hosts(ip_addr,subnet_mask)
    valid_subnets = get_valid_subnets(ip_addr,subnet_mask)

    submask_to_bin = to_binary_string(subnet_mask) # converting submask to binary to see what bits are turned on.
    broadcast_address = get_broadcast_address(ip_addr,subnet_mask)
    first_address = get_first_address(ip_addr,subnet_mask)
    last_address = get_last_address(ip_addr,subnet_mask)
    

    return ('Address: {} / {} \nSubnets: {}\nAddressable hosts per subnet: {}\nValid subnets: {}\nBroadcast addresses: {}\nFirst addresses: {}\nLast addresses: {}'.format(ip_addr,CIDR,subnets,hosts,valid_subnets,broadcast_address,first_address,last_address))


def to_binary_string(ip_addr): # function to convert string to binary

    byte_split = ip_addr.split(".")

    return ['{0:08b}'.format(int(x)) for x in byte_split]

def to_decimal_dot(ip_addr_list): # function to join string with '.' and convert to decimal

    return ".".join([str(int(x,2)) for x in ip_addr_list])

def get_supernet_stats(ip_addr):

    ip_address = [] # list for ip address
    for ip in ip_addr:
        ip = ''.join(to_binary_string(ip))  # converting to binary
        ip_address.append(ip) # adding to ip_address list

    prefix = ''.join(t[0] for t in takewhile(lambda t: len(set(t)) == 1, zip(*ip_address))) # zip iterates through the numbers in the ip_address list and lambda is the condition created to make sure that that the slices through it with a set. Takewhile keeps going while this condition is true and will stop once it is false and  and t[0] joins it to a string.
    len_of_prefix = len(prefix) # length of prefix found
    len_needed = 32 # when an ip is converted to binary it has lenght of 38
    len_of_network_mask = len_needed - len_of_prefix # to get how many 0's needed to be added 
    
    network_mask = (len_of_prefix * '1') + (len_of_network_mask * '0') # converting prefix found to 1 and adding 0's needed to form length of 28
    
    array = []
    for index in range(0, len(network_mask),8):
        array.append(network_mask[index:index + 8]) # appending every 8th index to the list array
    
    network_mask_decimal = to_decimal_dot(array) # converting binary array to decimal
    
    return('Address: {} / {} \nNetwork Mask: {} \n'.format(ip_addr[0], len_of_prefix, network_mask_decimal))