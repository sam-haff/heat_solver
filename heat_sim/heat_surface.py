import numpy as np

__all__=['HeatSurface1D', 'HeatSurface2D']

class HeatSurface1D:
    def __init__(self, *,T_left, T_right, T_middle, x_extent, x_grid, dt, k_coef):
        self.T_left = T_left
        self.T_right = T_right
        self.T_middle = T_middle
        self.x_grid = x_grid
        self.x_extent = x_extent
        self.dt = dt
        self.k_coef = k_coef
        self._dx = x_extent/x_grid

    def _make_init_T(self):
        '''Create initial temperature vector(flattened T/grid cell)'''
        T = [self.T_middle] * self.x_grid 
        T[0] = self.T_left
        T[-1] = self.T_right
        return np.array(T).transpose()

    def _make_P(self):
        '''Linear equation coefficients'''
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
        '''Simulation by steps. Produces T vector(T/grid cell, values for positions from 0 to x_extent physically).'''
        T = self._make_init_T()
        P = self._make_P()

        for t in range(0, iterations):
            if ((t % yield_step) == 0):
                yield T
            T = np.linalg.solve(P, T)

class HeatSurface2D:
    def __init__(self, x_extent, x_grid, y_extent, y_grid, T_boundary_top, T_boundary_bot, T_boundary_left, T_boundary_right, T_init_mid, dt, k_coef):
        #physical size of surface
        self.x_extent = x_extent 
        self.y_extent = y_extent
        #simulation grid
        self.x_grid = x_grid
        self.y_grid = y_grid
        #boundary
        self.T_boundary_top = T_boundary_top
        self.T_boundary_bot = T_boundary_bot
        self.T_boundary_left = T_boundary_left
        self.T_boundary_right = T_boundary_right
        self.T_init_mid = T_init_mid
        self.k_coef = k_coef
        #diffs
        self.dt = dt
        self._dx = x_extent/x_grid
        self._dy = y_extent/y_grid

    def _make_init_T(self):
        '''Create initial temperature vector(flattened T/grid cell)'''
        T = [self.T_boundary_top] * self.x_grid # top boundary
        for _ in range(1, self.y_grid - 1):
            ls = [self.T_init_mid] * self.x_grid
            ls[0] = self.T_boundary_left
            ls[-1] = self.T_boundary_right
            T.extend(ls)
        T.extend([self.T_boundary_bot] * self.x_grid) # bot boundary
        return np.array(T)
    
    def _flat_index(self, x, y):
        '''2D grid idex into flattened T matrix from _make_init_T'''
        return y * self.x_grid + x

    def _make_P(self):
        '''Linear equation coefficients'''
        # len(T) = x_grid * y_grid
        # T = [ T_0_0, T_0_1.., T_0_xgr, ... T_ygr_0, T_ygr_1,.., T_ygr_xgr ]
        Kx = self.k_coef/(self._dx*self._dx)
        Ky = self.k_coef/(self._dy*self._dy)
        P = []
        for i in range(self.x_grid): # vertical top boundary
            ls = [0.0] * self.x_grid * self.y_grid
            ls[i] = 1.0
            P.append(ls)
        for i in range(1, self.y_grid - 1):
            ls_left = [0.0] * self.x_grid * self.y_grid
            ix = self._flat_index(0, i)
            ls_left[ix] = 1.0
            P.append(ls_left) # horizontal left boundary 
            for k in range(1, self.x_grid-1):  
                ls = [0.0] * self.x_grid * self.y_grid
                ix_center = self._flat_index(k, i)
                ix_left = self._flat_index(k - 1, i)
                ix_right = self._flat_index(k + 1, i)
                ix_top = self._flat_index(k, i + 1)
                ix_bot = self._flat_index(k, i - 1)
                ls[ix_center] = 1 + 2*(Kx + Ky)
                ls[ix_left] = -Kx
                ls[ix_right] = -Kx
                ls[ix_top] = -Ky
                ls[ix_bot] = -Ky
                P.append(ls)
            ix = self._flat_index(self.x_grid-1, i)
            ls_right = [0.0] * self.x_grid * self.y_grid
            ls_right[ix] = 1.0
            P.append(ls_right) # horizontal right boundary

        for i in range(self.x_grid): # vertical bot boundary
            ls = [0.0] * self.x_grid * self.y_grid
            ix = self._flat_index(i, self.y_grid-1)
            ls[ix] = 1.0
            P.append(ls)

        return np.array(P)
    
    def sim(self, iterations, yield_step = 1):
        '''Simulation by steps. Produces unflattened T(t+1) matrix.'''
        T = self._make_init_T()
        P = self._make_P()

        for t in range(0, iterations):
            if ((t % yield_step) == 0):
                yield T.reshape((-1, self.x_grid))
            T = np.linalg.solve(P, T)