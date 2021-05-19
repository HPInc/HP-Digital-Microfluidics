# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 17:09:02 2020

@author: shkolniv

Author: Viktor Shkolnikov
Inspired by: Anand Jebakumar, wombat
"""


import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import imageio


class Visualizer():
    """
    This class takes the state of a DMF board and draws it as a matplotlib figure.
    
    To use the class, the user calls public methods set_x_and_show() to update
    the particular part of the board state. To clear the board and prepare
    it for the next state, the user calls clear_board().
    
    There is also an option to create an animation gif of the visualized board
    for the duration of instace session via make_gif method.
    
    Symbols:
    --------
    
    blue circle - liquid drop, where drop diameter scales as sqrt of volume. 
    green square - electrode is in ON state
    purple square - magnet is ON under that electrode
    orange circle - magnetic beads present in liquid
    small gray square - well 
    red square - temperature on electrode above threshold (temp_cut_off)
    black square - permanent obstacle (e.g. post, empty area)
    
    """
    
    
    
    def __init__(self, 
                 initial_volumes_array: np.ndarray, 
                 inital_states_array: np.ndarray, 
                 init_mag_particles_array: np.ndarray, 
                 init_mag_states_array: np.ndarray, 
                 init_temp_array: np.ndarray, 
                 well_volumes_array: np.ndarray, 
                 permanent_obstacles_array: np.ndarray = None,
                 to_file: bool = True):
        
        """
        Parameters
        ----------
        initial_volumes_array : Array of float64
            Volumes of each droplet at the intial state of the board. 
        inital_states_array : Array of bool
            Electrode states at the intial state of the board, True = ON.
        init_mag_particles_array : Array of float64
            Amount of magnetic particles on each electrode pad at the intial 
            state of the board. Note that magnetic particles do not have to be 
            inside of a droplet.
        init_mag_states_array : Array of bool
            Magnet states at the intial state of the board, True = ON.
        init_temp_array : Array of float64
            Temperatures, in Kelvin, at each electrode at the intial state of the board    
        well_volumes_array : Array of float64
            Volumes of each well at the intial state of the board    
        permanent_obstacles_array : Array of bool
            Permanent obstacles (e.g. posts, empty areas) with True indicating presence of obstacle.
        to_file: bool
            Flag, if true, an animation gif of the states during duration of 
            the instance will be created and saved. 
                         
        """
        
        self._volumes_array = initial_volumes_array
        self._mag_particles_array = init_mag_particles_array
        
        self._states_array = inital_states_array
        self._mag_states_array = init_mag_states_array
        
        self._temp_array = init_temp_array
        
        self._well_volumes_array = well_volumes_array
        
        self._ny = initial_volumes_array.shape[0]
        self._nx = initial_volumes_array.shape[1]
        
        
        if permanent_obstacles_array is None:
            self._obstacles_array = np.zeros(self._volumes_array.shape).astype(bool)
        else:
            self._obstacles_array = permanent_obstacles_array
        
        
        self._LINE_WIDTH = 1.0 
        self._GRID_SIZE = 0.25
        
        self._fig, self._ax = self._draw_board()
        
        # Writing file
        self._to_file = to_file # Flag deciding to create a gif 
        self._counter = 0
        self._file_names: list[str] = []

    def _draw_board(self):
        fig = plt.figure(figsize=(self._nx*self._GRID_SIZE,self._ny*self._GRID_SIZE))
        ax = fig.add_subplot(111, aspect='equal')
        self._draw_grid(ax)
        

        ax.axis('off')
        
        return fig, ax

    def _draw_grid(self,ax):
        for i in range(self._nx+1):
            ax.plot([i,i],[0,self._ny],'-k',linewidth=self._LINE_WIDTH)
        for j in range(self._ny+1):
            ax.plot([0,self._nx],[j,j],'-k',linewidth=self._LINE_WIDTH)
            
        
            
                
    def _show_drops(self):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                drop_volume = self._volumes_array[j0, j1]
                if drop_volume > 0:

                    shape = patches.Circle((j1+0.5 ,j0+0.5), 0.5*np.sqrt(drop_volume), color='b', alpha=0.5) # Note the convention of the first colum is colum 0
                    self._ax.add_patch(shape)
        
        # When drawing drops, also draw obstacles
        self._show_obstacles()
                    

    def _show_mag_particles(self):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                content = self._mag_particles_array[j0, j1]
                if content > 0:

                    shape = patches.Circle((j1+0.5 ,j0+0.5), 0.25*np.sqrt(content), color='darkorange', alpha=0.5) # Note the convention of the first colum is colum 0
                    self._ax.add_patch(shape)


    def _show_states(self):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                if self._states_array[j0, j1]:
                    shape = patches.Rectangle((j1 ,j0), 1, 1,color='g',alpha=0.5)
                    self._ax.add_patch(shape)
                    
                    
    def _show_mag_states(self):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                if self._mag_states_array[j0, j1]:
                    shape = patches.Rectangle((j1 ,j0), 0.9, 0.9, color='purple',alpha=0.5)
                    self._ax.add_patch(shape)                
    
    
    def _show_temp(self, temp_cut_off = 293.0):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                if self._temp_array[j0, j1] > temp_cut_off:
                    shape = patches.Rectangle((j1 ,j0), 0.9, 0.9, color='r',alpha=0.5)
                    self._ax.add_patch(shape) 
        
    
    def _show_wells(self):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                if self._well_volumes_array[j0, j1] > 1.0:
                    shape = patches.Rectangle((j1+0.25 ,j0+0.25), 0.5, 0.5, color='k',alpha=0.5)
                    self._ax.add_patch(shape) 
                    
    def _show_obstacles(self):
        for j0 in range(self._ny):
            for j1 in range(self._nx):
                if self._obstacles_array[j0, j1]:
                    shape = patches.Rectangle((j1 ,j0), 1, 1,color='k',alpha=0.9)
                    self._ax.add_patch(shape)        
        
        

    def _save_plot_to_file(self):
        

        file_name = 'imgs/img_{}.png'.format(str(self._counter).zfill(5))         
        self._counter += 1
        
        plt.savefig(file_name)
        self._file_names.append(file_name)
        
        
        
    # Public functions -------------------------------------------------------
        
    def make_gif(self, gif_name = 'dmf.gif', duration = 0.05):
        """
        https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python
        
        duration : float
            Duration for each frame of the gif (1/fps).
        
        """
        with imageio.get_writer(gif_name, mode='I', duration = duration) as writer:
            for file_name in self._file_names:
                writer.append_data(imageio.imread(file_name))


                    
    def clear_board(self):
        if self._to_file:
            self._save_plot_to_file()
        
        self._ax.patches = []
        self._fig.canvas.draw_idle()
        
    def set_volumes_and_show(self, volumes_array):
        self._volumes_array = volumes_array
        self._show_drops()
        
    def set_mag_particles_and_show(self, mag_particles_array):
        self._mag_particles_array = mag_particles_array
        self._show_mag_particles()
        
    def set_states_and_show(self, states_array):
        self._states_array = states_array
        self._show_states()
    
    def set_mag_states_and_show(self, mag_states_array):
        self._mag_states_array = mag_states_array
        self._show_mag_states()
      
    def set_temp_and_show(self, temp_array):
        self._temp_array = temp_array
        self._show_temp()
     
    def set_wells_and_show(self, well_volumes_array):
        self._well_volumes_array = well_volumes_array
        self._show_wells()

if __name__ == '__main__':  
    
    # Testing
    volumes_array = np.zeros((32,32))
    volumes_array[1,1] = 1
    
    well_volumes_array = np.ones((32,32))
    well_volumes_array[3,3] = 10.0
    
    
    mag_particles_array = np.zeros((32,32))
    mag_particles_array[2,2] = 1
    
    states_array = np.full((32, 32), False, dtype=bool)
    states_array[1,2] = True
    states_array[1,5] = True
    
    mag_states_array = np.full((32, 32), False, dtype=bool)
    mag_states_array[1,3] = True
    mag_states_array[1,5] = True
    
    
    temp_array = np.full((32,32), 293.0, dtype=float)
    temp_array[5,5] = 300
    
    obstacles_array = np.zeros(volumes_array.shape).astype(bool)
    obstacles_array[6,6] = True
    
    visualizer = Visualizer(volumes_array, states_array, mag_particles_array, mag_states_array, temp_array, well_volumes_array, obstacles_array)
    
    visualizer._show_drops()
    visualizer._show_states()
    
    visualizer._show_mag_particles()
    visualizer._show_mag_states()
    visualizer._show_temp()
    visualizer._show_wells()
    
    # Visualizer._save_plot_to_file()
    

    
    
    plt.pause(10)
    visualizer.clear_board()


