import hashlib
import random
import requests

SERVER_URL = "http://6857ust.csail.mit.edu"


# HASHING

def H(m):
    """ 
    return hash (256-bit integer) of string m, as long integer.
    If the input is an integer, treat it as a string.
    """
    m = str(m)
    return int(hashlib.sha256(m).hexdigest(),16)

def main():

    # This is the server's public key
    (n,e) = (134396116210830788484018767964013629489196469547696523589987670739352331298546935122669200918534934582132211415741993791432093579115340771967204360015313860402522803467667807760433738061050011496364124870297526881598059067254324554928263193228725822473875063136676943441129929543229462213961466613312291337393, 65537)

    # Replace this with the values you got from the course staff.  
    # This is the nonce and sig(hash(nonce)) that would be received 
    # through "subscription".
    (nonce, sig) = (0,0) 

    # Number of iterations.  Please don't make this very large.
    num_iterations = 10

    for i in xrange(0,num_iterations):
        #generate a new nonce (new_nonce) and blinded object (blinded_new_hash) to sign
        # FILL IN HERE

        #make a request to the server
        (text_string, new_blinded_sig) = send_request(sig, nonce, blinded_new_hash)
        new_blinded_sig = long(new_blinded_sig)

        #unblind the new sig (yielding new_sig)
        # FILL IN HERE

        # If you feel like printing out any other information, here's 
        # a good place to do it...
        print text_string

        #change to next nonce/signature for next iteration
        (nonce, sig) = (new_nonce, new_sig)
    
# Send a request of the form sig(hash(nonce)), nonce, blind(hash(new_nonce))
def send_request(signed_hash, nonce, blinded_new_hash):
    payload = {'sig': signed_hash, 'nonce': nonce, 'blinded': blinded_new_hash}
    r = requests.get(SERVER_URL, params=payload)
    if(r.status_code != 200):
        raise Exception(r.text)
    return r.text.splitlines()

main()

