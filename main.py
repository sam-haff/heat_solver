import numpy as np
import matplotlib.pyplot as plt
import heat_surface

timeIters = 60000
sim_surface = heat_surface.HeatSurface(t_left=30.0, t_right=30.0, t_middle=500.0, x_extent=100.0, x_grid=30, dt=1, k_coef=0.5)

sim_results = []
i = 0
for result in sim_surface.sim(1200, 200):
    sim_results.append(result)

x = np.arange(0, sim_surface.x_grid) 
 
# plotting
extent = [x[0]-(x[1]-x[0])/2., x[-1]+(x[1]-x[0])/2.,0,1]
fig, plts = plt.subplots(nrows=len(sim_results), sharex=True)
for (i,p) in enumerate(plts):
    p.set_title(f'{200*i} seconds', fontsize=10)
    p.imshow(sim_results[i][np.newaxis,:], vmax=500, cmap="plasma", aspect="auto", extent=extent)
    p.set_yticks([])
    p.set_xlim(extent[0], extent[1])

plt.tight_layout()
plt.show()