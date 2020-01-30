import numpy as np

def get_distr_normal(mean, variance):
    '''Wrapper that returns a function for drawing `n` 
    fitness values from a normal distribution.'''
    def distr_normal(n):
        return np.random.normal(mean, scale=np.sqrt(variance), size=n)
    
    return distr_normal

class Model(object):

    def __init__(self, **params):

        # Model parameters 
        # (default values will be updated if params given)
        self.m0 = 2
        self.c = 0.8
        self.distr_r = get_distr_normal(0,0.001)
        self.r0 = None

        self.__dict__.update(params)
        self.initialise()

    #================================================================

    def _get_m(self):
        self.m = len(self.idx)

    def _get_r(self, r):
        self.r = r - r.mean()

    #================================================================

    def initialise(self):
        self.n_mut = 0

        self.idx = np.arange(self.m0)
        self.idx_max = self.idx.max()
        self._get_m()

        if self.r0 is None:
            self.r0 = self.distr_r(self.m)

        self._get_r(self.r0)

        self.r_mut = None
        self.m_del = 0

    def mutate(self):
        self.n_mut += 1
        self.m_del = 0

        self.idx_max += 1
        self.idx = np.append(self.idx, self.idx_max)
        self._get_m()

        self.r_mut = self.distr_r(1)
        self.r = np.append(self.r, self.r_mut)
        self._get_r(self.r)

    def eliminate(self):
        self.m_del += 1
        self.idx_del = np.argmin(self.r)

        self.idx = np.delete(self.idx, self.idx_del)
        self._get_m()

        self.r = np.delete(self.r, self.idx_del)
        self._get_r(self.r)

    def get_fixedPoint(self):
        self.x = 1/self.m *( 1 +(self.m*(1+self.c)/(1-self.c) - 1) *self.r )
                
    def get_stability(self):
        if ( (self.x > 0).all() and (self.x <= 1).all() ):
            self.stability = True
        else:
            self.stability = False

    def get_fixedPoint_stable(self):
        while True:
            self.get_fixedPoint()
            self.get_stability()

            if self.stability:
                break
            else:
                self.eliminate()

    #================================================================

    def arrays2lists(self):
        self.idx = self.i.tolist()
        self.x = self.x.tolist()
        self.r = self.r.tolist()
        
    def data(self):
        return self.__dict__