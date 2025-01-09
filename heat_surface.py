import numpy as np

class HeatSurface:
    def __init__(self, *, t_left, t_right, t_middle, x_extent, x_grid, dt, k_coef):
        self.t_left = t_left
        self.t_right = t_right
        self.t_middle = t_middle
        self.x_grid = x_grid
        self.x_extent = x_extent
        self.dt = dt
        self.k_coef = k_coef
        self._dx = x_extent/x_grid

    def _make_init_T(self):
        T = [self.t_middle] * self.x_grid 
        T[0] = self.t_left
        T[-1] = self.t_right
        return np.array(T).transpose()

    def _make_P(self):
        K = self.k_coef/(self._dx*self._dx)
        neg_K = -K
        c = (1+2*K)

        Pls = [0] * self.x_grid 
        Pls = [Pls.copy() for _ in range(0, self.x_grid)]
        Pls[0][0] = 1.0
        Pls[self.x_grid-1][self.x_grid-1] = 1.0
        for i in range(1, self.x_grid-1):
            Pls[i][i-1] = neg_K 
            Pls[i][i] = c
            Pls[i][i+1] = neg_K

        return np.array(Pls)

    def sim(self, iterations, yield_step = 1):
        T = self._make_init_T()
        P = self._make_P()

        for t in range(0, iterations):
            if ((t % yield_step) == 0):
                yield T
            T = np.linalg.solve(P, T)


