from my_db.pd_client import queryUserData

def add(x,y):
    print queryUserData(1)
    return x+y

if __name__=='__main__':
    print add(1,2)
    print add(1,-1)