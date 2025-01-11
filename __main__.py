import numpy as np
from .heat_sim import *
import click
from .viewer import Viewer

@click.group()
@click.option('--k', type=click.FloatRange(0.01, max_open=True), help='Conductivity coefficient.', prompt='Thermal diffusivity constant(--k)')
@click.option('--iters_num', type=click.IntRange(1, max_open=True), default=None, help='Number of simulation iterations overall')
@click.option('--iters_per_vis', type=click.IntRange(1, max_open=True), help='Number of iterations per visualisation. Total number of visulisations/plots is then (iters_num/iters_per_vis + 1).', prompt='Simulation time steps per visualisation(--iters_per_vis)')
@click.option('--num_vis', type=click.IntRange(1, max_open=True), help='Number of visualisations generated. Total number of computed simulation iterations is then (num_vis*iters_per_vis)', prompt='Number of desired visualisations(--num_vis)')
@click.option('--vis_num_rows', type=click.IntRange(1, max_open=True), default=None, help='Visualize all plots on one page in <vis_num_rows> rows.',)
@click.option('--vis_remove_boundaries', is_flag=True, help='Dont show boundaries.',)
@click.pass_context
def cli(ctx, k, iters_num, iters_per_vis, num_vis, vis_num_rows, vis_remove_boundaries):
    ctx.ensure_object(dict)
    ctx.obj['k'] = k
    ctx.obj['iters_num'] = iters_num
    ctx.obj['iters_per_vis'] = iters_per_vis
    ctx.obj['num_vis'] = num_vis
    ctx.obj['vis_num_rows'] = vis_num_rows
    ctx.obj['vis_remove_boundaries'] = bool(vis_remove_boundaries)


def unpack_cli_ctx(ctx):
    ctx.ensure_object(dict)
    k = ctx.obj['k']
    num_vis = ctx.obj['num_vis']
    iters_per_vis = ctx.obj['iters_per_vis']
    iters_num = num_vis * iters_per_vis
    if ctx.obj['iters_num']:
        iters_num = ctx.obj['iters_num']
    vis_num_rows = ctx.obj['vis_num_rows']
    vis_remove_boundaries = ctx.obj['vis_remove_boundaries']
    
    return (k, num_vis, iters_per_vis, iters_num, vis_num_rows, vis_remove_boundaries)


@cli.command('simulate1D')
@click.option('--x_grid', type=click.IntRange(3, 260), default=20, help='Simulation grid resolution on axis X.')
@click.option('--extent_x', type=click.FloatRange(1.0, max_open=True), help='Physical surface width.', prompt='Physical surface width(--extent_x)')
@click.option('--T_left', type=float, help='Boundary condition(constant temperature) on the left side of the surface.', prompt='Boundary(is not changed under simulation) temperature on the left(--T_left)')
@click.option('--T_right', type=float, help='Boundary condition(constant temperature) on the right side of the surface. Only applicable to 2D simulation.', prompt='Boundary temperature on the right(--T_right)')
@click.option('--T_mid', type=float, help='Starting temperature inside the boundary(simulated surface part).', prompt='Starting surface temperature(--T_mid)')
@click.pass_context
def init_sim_1D(ctx, x_grid, extent_x, t_left, t_right, t_mid):
    k, _, iters_per_vis, iters_num, vis_num_rows, vis_remove_boundaries = unpack_cli_ctx(ctx)

    sim_surface = HeatSurface1D(T_left=t_left, T_right=t_right, T_middle=t_mid, x_extent=extent_x, x_grid=x_grid, dt=1, k_coef=k)

    viewer = Viewer.from_surface(sim_surface, iters_num, iters_per_vis, include_boundaries=not vis_remove_boundaries, plt_num_rows=vis_num_rows)
    viewer.show()
    
@cli.command('simulate2D')
@click.option('--x_grid', type=click.IntRange(3, 60), default=20, help='Simulation grid resolution on axis X.')
@click.option('--y_grid', type=click.IntRange(3, 60), default=20, help='Simulation grid resolution on axis Y.')
@click.option('--extent_x', type=click.FloatRange(1.0, max_open=True), help='Physical surface width.', prompt='Physical surface width(--extent_x)')
@click.option('--extent_y', type=click.FloatRange(1.0, max_open=True), help='Physical surface height.', prompt='Physical height(--extent_y)')
@click.option('--T_left', type=float, help='Boundary condition(constant temperature) on the left side of the surface.', prompt='Boundary(is not changed under simulation) temperature on the left(--T_left)')
@click.option('--T_right', type=float, help='Boundary condition(constant temperature) on the right side of the surface. Only applicable to 2D simulation.', prompt='Boundary(is not changed under simulation) temperature on the right(--T_right)')
@click.option('--T_top', type=float, help='Boundary condition(constant temperature) on the top side of the surface. Only applicable to 2D simulation.', prompt='Boundary(is not changed under simulation) temperature on the top(--T_top)')
@click.option('--T_bot', type=float, help='Boundary condition(constant temperature) on the bottom side of the surface.', prompt='Boundary(is not changed under simulation) temperature on the bottom(--T_bot)')
@click.option('--T_mid', type=float, help='Starting temperature inside the boundary(simulated surface part).', prompt='Starting surface temperature(--T_mid)')
@click.pass_context
def init_sim_2D(ctx, x_grid, y_grid, extent_x, extent_y, t_left, t_right, t_top, t_bot, t_mid):
    k, _, iters_per_vis, iters_num, vis_num_rows, vis_remove_boundaries = unpack_cli_ctx(ctx)

    sim_surface = HeatSurface2D(
        x_extent=extent_x, y_extent=extent_y,
        x_grid=x_grid, y_grid=y_grid,
        T_boundary_bot=t_bot, T_boundary_top=t_top,
        T_boundary_left=t_left, T_boundary_right=t_right,
        T_init_mid=t_mid,
        dt=1,
        k_coef=k)
    
    iters_per_result = iters_per_vis 
    viewer = Viewer.from_surface(sim_surface, iters_num, iters_per_result, include_boundaries=not vis_remove_boundaries, plt_num_rows=vis_num_rows)
    viewer.show()

cli()