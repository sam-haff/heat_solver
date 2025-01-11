import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from .heat_sim import *

class Viewer:
    def __init__(self):
        pass

    @classmethod
    def from_results(cls, results): 
        v = Viewer()
        v.simulation_results = results
        return v


    @classmethod
    def from_surface(cls, surf, iters_n, iters_per_vis, *, include_boundaries=True, plt_num_rows=None):
        def _rem_boundaries(res):
            if len(res.shape) == 1:
                return res[1:len(res)-1]
            if len(res.shape) != 2:
                raise RuntimeError('Malformed result')
            return res[1:res.shape[0]-1, 1:res.shape[1]-1]

        v = Viewer()
        sim_results = []
        for sim_res in surf.sim(iters_n, iters_per_vis):
            res = sim_res if include_boundaries else _rem_boundaries(sim_res)
            if len(sim_res.shape) == 1:
                res = sim_res[np.newaxis, :]
            sim_results.append(res)

        v.simulation_results = sim_results
        v.surf = surf
        v.simulation_iters_n = iters_n
        v.simulation_iters_per_result = iters_per_vis
        v.plt_dim = (1, 1)
        if plt_num_rows:
            ncols = round(len(sim_results)/plt_num_rows)
            v.fig, v.plts = plt.subplots(ncols=ncols, nrows=plt_num_rows, sharex=True)
            v.plt_dim = (plt_num_rows, ncols)
        else:
            v.fig, v.plts = plt.subplots()
            v.plts = [v.plts]
        return v

    def _show_paged_view(self, extent, hide_y_ticks): 
        ax = self.plts[0]
        if hide_y_ticks:
            ax.axes.yaxis.set_ticklabels([])
        pl = ax.matshow(self.simulation_results[0], vmax=self.surf.max_heat, cmap="plasma", aspect="equal", extent=extent)

        class Index:
            def __init__(self, viewer):
                self.viewer = viewer
                self.ix = 0
            def next(self, event):
                self.ix += 1
                self.ix = self.ix % len(self.viewer.simulation_results)
                pl.set_data(self.viewer.simulation_results[self.ix])
                ax.set_title(f'{self.viewer.simulation_iters_per_result*self.ix} seconds', y=1.0, pad=-14, fontsize=10)
                plt.draw()
            def prev(self, event):
                self.ix -= 1
                self.ix = self.ix % len(self.viewer.simulation_results)#??
                pl.set_data(self.viewer.simulation_results[self.ix])
                ax.set_title(f'{self.viewer.simulation_iters_per_result*self.ix} seconds', y=1.0, pad=-14, fontsize=10)
                plt.draw()

        callback = Index(self)
        axprev = self.fig.add_axes([0.7, 0.05, 0.1, 0.075])
        axnext = self.fig.add_axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(callback.next)
        bprev = Button(axprev, 'Previous')
        bprev.on_clicked(callback.prev)

        plt.show()


    def _show_table_view(self, extent, hide_y_ticks):
        n_rows = self.plt_dim[0]
        n_cols = self.plt_dim[1]
        for (i, row) in enumerate(self.plts):
            for (j, p) in enumerate(row):
                if (i*n_cols + j) >= len(self.simulation_results):
                    p.set_axis_off() # hide unused plots
                    continue 
                if hide_y_ticks:
                    p.axes.yaxis.set_ticklabels([])

                p.matshow(self.simulation_results[i*n_cols + j], vmax=self.surf.max_heat, cmap="plasma", aspect="equal", extent=extent)
        plt.show()

    def show(self):
        if not self.surf:
            raise RuntimeError("Not properly initialized")
        extent = None
        is_table_view = False
        hide_y_ticks = False
        if len(self.plts) == 0:
            raise RuntimeError("Should've initialized plots")
        if self.plt_dim != (1,1):
            is_table_view = True
        if isinstance(self.surf, HeatSurface1D):
            x = range(0, self.surf.x_grid)
            extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,5]
            hide_y_ticks = True
         
        if not is_table_view:
            self._show_paged_view(extent, hide_y_ticks)
        else:
            self._show_table_view(extent, hide_y_ticks)

