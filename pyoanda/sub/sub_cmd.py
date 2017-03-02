import sys
import getopt
# ==================================command line=======================================
def sub_cmd():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'm:')
    except getopt.GetoptError:
        print ('sys arguments error, check help')
        sys.exit()

    print ("opts :", opts)
    if not opts:
        print ("Please enter mode = train/test")
        sys.exit(0)
        
    for o, a in opts:
        if o == '-m' and a == 'test':
            is_test = True
            is_train = False
        elif o == '-m' and a == 'train':
            is_train = True
            is_test = False
        else:
            print ("error!!!")
    
    return is_test, is_train
# ==================================command line end====================================