import numpy as np

def flac(x):
    if x==1:
        return 1

    return x*flac(x-1)

class Board:
    def __init__(self,N):

        field=np.random.permutation(range(0,N**2))
        field=field.reshape([N,N])
        self.field=field
        self.N=N
        self.getpos0()

        l=[(j,i)for j in range(N) for i in range(N)]
        nn={}
        for k in range(N**2):
            nn[k]=l[k]
        self.nn=nn

    def getpos0(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.field[i,j]==0:
                    self.pos0=np.array((i,j))
                    break

    def fielda(self,x):
        return self.field[x[0],x[1]]

    def field_in(self,x1,x2):
        if type(x2)==np.ndarray:
            self.field[x1[0],x1[1]]=self.fielda(x2)
        else:
            self.field[x1[0],x1[1]]=x2

    def random_slide(self):
        directions=[[1,0],[0,1],[-1,0],[0,-1]]

        field=self.field
        while True:
            rn=np.random.randint(4)
            nx=self.pos0+directions[rn]
            if self.inner(nx):
                self.swap(nx,self.pos0)
                self.sbefore=[self.pos0,nx]
                self.pos0=nx
                break

    def inner(self,x):
        N=self.field.shape[0]
        if 0<=x[0] and x[0]<N and 0<=x[1] and x[1]<N:
            return True
        else:
            return False


    def swap(self,x1,x2):
        tmp=self.fielda(x1)
        self.field_in(x1,x2)
        self.field_in(x2,tmp)

    def modosu(self):
        self.swap(self.sbefore[0],self.sbefore[1])

    def dist(self,x,y):
        return np.abs(x[0]-y[0])+np.abs(x[1]-y[1])


    def f(self):
        field=self.field
        res=0
        for i in range(self.N):
            for j in range(self.N):
                res+=self.dist((i,j),self.nn[field[i][j]])

        return res

def annealingoptimize():

    cool_rate=0.999
    _fval=999
    x=Board(4)
    T=1000

    while T>0.00001:
        print("x=")
        print(x.field)
        print(x.f())

        T=T*cool_rate
        x.random_slide()


        fval=x.f()

        dE=fval-_fval

        if dE<=0:
            _fval=fval
            continue

        p=np.e**(-dE/T)
        if np.random.rand(1)<=p:
            _fval=fval
            continue

        x.modosu()

    return(x)


annealingoptimize()
