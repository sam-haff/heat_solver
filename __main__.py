import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from .heat_sim import *
import click

class Viewer:
    def __init__(self):
        pass
    @classmethod
    def from_surface(cls, surf, iters_n, iters_per_vis):
        pass
    @classmethod
    def from_results(cls, results):
        pass
    def show(self):
        pass

timeIters = 60000

@click.group()
def cli():
    pass

@cli.command('1D')
@click.option('--x_grid', type=click.IntRange(3, 260), default=20, help='Simulation grid resolution on axis X.')
@click.option('--extent_x', type=click.FloatRange(1.0, max_open=True), help='Physical surface width.', prompt=True)
@click.option('--T_left', type=float, help='Boundary condition(constant temperature) on the left side of the surface.', prompt=True)
@click.option('--T_right', type=float, help='Boundary condition(constant temperature) on the right side of the surface. Only applicable to 2D simulation.', prompt=True)
@click.option('--T_mid', type=float, help='Starting temperature inside the boundary(simulated surface part).', prompt=True)
@click.option('--k', type=click.FloatRange(0.01, max_open=True), help='Conductivity coefficient.', prompt=True)
def init_sim_1D(x_grid, extent_x, t_left, t_right, t_mid, k):
    max_heat = max(t_left, t_mid, t_right)

    sim_surface = HeatSurface1D(T_left=t_left, T_right=t_right, T_middle=t_mid, x_extent=extent_x, x_grid=x_grid, dt=1, k_coef=k)

    sim_results = []
    i = 0
    for result in sim_surface.sim(1400, yield_step=250):
        sim_results.append(result)

    x = np.arange(0, sim_surface.x_grid) 
    
    # plotting
    extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
    fig, plts = plt.subplots(nrows=len(sim_results), sharex=True)
    for (i,p) in enumerate(plts):
        p.set_title(f'{200*i} seconds', y=1.0, pad=-14, fontsize=5)
        p.imshow(sim_results[i][np.newaxis,:], vmax=max_heat, cmap="plasma", aspect="auto", extent=extent)
        p.set_yticks([])
        p.set_xlim(extent[0], extent[1])

    plt.tight_layout()
    plt.show()


@cli.command('2D')
@click.option('--x_grid', type=click.IntRange(3, 60), default=20, help='Simulation grid resolution on axis X.')
@click.option('--y_grid', type=click.IntRange(3, 60), default=20, help='Simulation grid resolution on axis Y.')
@click.option('--extent_x', type=click.FloatRange(1.0, max_open=True), help='Physical surface width.', prompt=True)
@click.option('--extent_y', type=click.FloatRange(1.0, max_open=True), help='Physical surface height.', prompt=True)
@click.option('--T_left', type=float, help='Boundary condition(constant temperature) on the left side of the surface.', prompt=True)
@click.option('--T_right', type=float, help='Boundary condition(constant temperature) on the right side of the surface. Only applicable to 2D simulation.', prompt=True)
@click.option('--T_top', type=float, help='Boundary condition(constant temperature) on the top side of the surface. Only applicable to 2D simulation.', prompt=True)
@click.option('--T_bot', type=float, help='Boundary condition(constant temperature) on the bottom side of the surface.', prompt=True)
@click.option('--T_mid', type=float, help='Starting temperature inside the boundary(simulated surface part).', prompt=True)
@click.option('--k', type=click.FloatRange(0.01, max_open=True), help='Conductivity coefficient.', prompt=True)
def init_sim_2D(x_grid, y_grid, extent_x, extent_y, t_left, t_right, t_top, t_bot, t_mid, k):
    max_heat = max(t_left, t_right, t_top, t_bot, t_mid) 

    sim_surface = HeatSurface2D(
        x_extent=extent_x, y_extent=extent_y,
        x_grid=x_grid, y_grid=y_grid,
        T_boundary_bot=t_bot, T_boundary_top=t_top,
        T_boundary_left=t_left, T_boundary_right=t_right,
        T_init_mid=t_mid,
        dt=1,
        k_coef=k)
    sim_results = []
    for simulation_result in sim_surface.sim(200,10):
        sim_results.append(simulation_result)


    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    pl = ax.matshow(sim_results[0], vmax=max_heat, cmap="plasma", aspect="equal")

    class Index:
        ix = 0

        def next(self, event):
            self.ix += 1
            self.ix = self.ix % len(sim_results)
            pl.set_data(sim_results[self.ix])
            ax.set_title(f'{10*self.ix} seconds', y=1.0, pad=-14, fontsize=10)
            plt.draw()

        def prev(self, event):
            self.ix -= 1
            self.ix = self.ix % len(sim_results)#??
            pl.set_data(sim_results[self.ix])
            ax.set_title(f'{10*self.ix} seconds', y=1.0, pad=-14, fontsize=10)
            plt.draw()

    callback = Index()
    axprev = fig.add_axes([0.7, 0.05, 0.1, 0.075])
    axnext = fig.add_axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    plt.show()

cli()

'''
    nrows = 4 
    ncols = round(len(sim_results)/nrows)
    #extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
    fig, plts = plt.subplots(ncols=ncols, nrows=nrows, sharex=True)
    print(plts)
    print(plts[0])
    print(list(enumerate(plts)))
    for (i,r) in enumerate(plts):
        for (j, p) in enumerate(r):
            print((i, j))
            print(i*ncols+ j)
            if i*ncols+ j >= len(sim_results):
                break
            p.set_title(f'{200*(i*ncols+j)} seconds', y=1.0, pad=-14, fontsize=5)
            p.matshow(sim_results[i*ncols+ j], vmax=6000.0, cmap="plasma", aspect="equal")
        #p.imshow(sim_results[i][np.newaxis,:], vmax=500, cmap="plasma", aspect="auto", extent=extent)
        #p.set_yticks([])
        #p.set_xlim(extent[0], extent[1])

    plt.tight_layout()
    plt.show()'''