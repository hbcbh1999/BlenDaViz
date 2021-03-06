# plot3d.py
"""
Contains routines to three-dimensional plots.

Created on Wed Dec 16 10:34:00 2018

@authors: Simon Candelaresi, Chris Smiet (csmiet@pppl.gov)
"""

'''
Test:
import numpy as np
import importlib
import sys
sys.path.append('~/codes/blendaviz')
import blender as blt
importlib.reload(blt.plot3d)
importlib.reload(blt.colors)
importlib.reload(blt)
x0 = np.linspace(-3, 3, 20)
y0 = np.linspace(-3, 3, 20)
z0 = np.linspace(-3, 3, 20)
x, y, z = np.meshgrid(x0, y0, z0, indexing='ij')
phi = np.exp(-(x**2+y**2+z**2))*np.cos(z)
alpha = np.sin(np.linspace(phi.min(), phi.max(), 100))
vol = blt.vol(phi, x, y, z)
vol.plot()
'''

def vol(phi, x, y, z, emission=None, color_map=None):
    """
    Plot a 3d volume rendering of a scalar field.

    call signature:

    vol(phi, x, y, z, alpha=None, color_map=None)

    Keyword arguments:

    *phi*:
      Scalar field in 3d of shape [nx, ny, nz].

    *x, y, z*:
      1d arrays for the coordinates.

    *emission*:
      1d or 2d array of floats containing the emission values for phi.
      If specified as 2d array fo shape [2, n_emission] the emission[0, :] are the values
      phi which must be monotonously increasing and emission[1, ;] are their corresponding
      emission values.

    *color_map*:
      Color map for the values stored in the array 'c'.
      These are the same as in matplotlib.
    """

    import inspect

    # Assign parameters to the Volume objects.
    volume_return = Volume()
    argument_dict = inspect.getargvalues(inspect.currentframe()).locals
    for argument in argument_dict:
        setattr(volume_return, argument, argument_dict[argument])
    volume_return.plot()
    return volume_return


class Volume(object):
    """
    Volume class including the data, 3d texture and parameters.
    """

    def __init__(self):
        """
        Fill members with default values.
        """

        self.phi = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.emission = None
        self.color_map = None
        self.mesh_object = None
        self.mesh_material = None


    def plot(self):
        """
        Plot the 3d texture.
        """

        import bpy
        import numpy as np
        import matplotlib.cm as cm

        # Check the validity of the input arrays.
        if (not isinstance(self.x, np.ndarray) or not isinstance(self.y, np.ndarray)
                or not isinstance(self.z, np.ndarray)):
            print("Error: x OR y OR z array invalid.")
            return -1
        if not isinstance(self.phi, np.ndarray):
            print("Error: phi must be numpy array.")
            return -1
        if self.emission:
            if not isinstance(self.emission, np.ndarray):
                print("Error: emission must be numpy array.")
                return -1

        # Using volumetric textures or voxels?

        # Delete existing meshes.
        if not self.mesh_object is None:
            bpy.ops.object.select_all(action='DESELECT')
            self.mesh_object.select = True
            bpy.ops.object.delete()
            self.mesh_object = None

        # Delete existing materials.
        if not self.mesh_material is None:
            bpy.data.materials.remove(self.mesh_material)

        # Create cuboid.
        bpy.ops.mesh.primitive_cube_add()
        self.mesh_object = bpy.context.object

        # Define the RGB value for each voxel.
        phi_max = np.max(self.phi)
        phi_min = np.min(self.phi)
        if self.color_map is None:
            self.color_map = cm.viridis
        pixels[0::3] = self.color_map((self.phi.flatten() - phi_min)/(phi_max - phi_min))[:, 0]
        pixels[1::3] = self.color_map((self.phi.flatten() - phi_min)/(phi_max - phi_min))[:, 1]
        pixels[2::3] = self.color_map((self.phi.flatten() - phi_min)/(phi_max - phi_min))[:, 2]

        # Define the emission for each voxel.
        emission = np.zeros_like(self.phi)
        if self.emission.ndim == 1:
            phi_emission = np.zeros([2, self.emission.size])
            phi_emission[0, :] = np.linspace(self.phi.min(), self.size.max(), self.emission.size)
            phi_emission[1, :] = self.emission
        else:
            phi_emission = self.emission

        for emission_idx in self.emission.shape[-1]-1:
            mask = self.phi >= phi_emission[0, emission_idx] and self.phi < phi_emission[0, emission_idx+1]
            weight_left = self.phi[mask] - phi_emission[0, emission_idx]
            weight_right = -self.phi[mask] + phi_emission[0, emission_idx+1]
            emission[mask] = (weight_left*phi_emission[1, emission_idx] + \
                              weight_right*phi_emission[1, emission_idx+1]) \
                             /(weight_left + weight_right)
        del(emission)

        # Assign a material to the cuboid.
        self.mesh_material = bpy.data.materials.new('MaterialMesh')
        self.mesh_material.use_nodes = True

        # Add the RGB and emission values to the material.
        nodes = node_tree.nodes
        # Remove diffusive BSDF node.
        nodes.remove(nodes[1])
        # Add the emission shader.
        node_emission = nodes.new(type='ShaderNodeEmission')
        # Link the emission output to the material output.
        node_tree.links.new(node_emission.outputs['Emission'],
                            nodes[0].inputs['Volume'])
        # Add the RGB source node.

        # Link the RGB output to the emission shader  color input.

        # Add the emission source node.

        # Link the emission output to the emission shader strength input.


        return 0



'''
Test:
import numpy as np
import importlib
x = np.linspace(-2, 2, 5)
y = np.linspace(-2, 2, 5)
z = np.linspace(-2, 2, 5)
u = np.array([1, 0, 0, 1, 0])
v = np.array([0, 1, 0, 1, 1])
w = np.array([0, 0, 1, 0, 1])
import sys
sys.path.append('~/codes/blendaviz')
import blendaviz as blt
importlib.reload(blt)
importlib.reload(blt.plot3d)
importlib.reload(blt.colors)
qu = blt.quiver(x, y, z, u, v, w, pivot='mid', color='magnitude')
qu = blt.quiver(x, y, z, u, v, w, pivot='mid', color='red')
qu = blt.quiver(x, y, z, u, v, w, pivot='mid', color='red', alpha=np.random.random(5))
qu = blt.quiver(x, y, z, u, v, w, pivot='mid', color='red', emission=np.random.random(5))
qu = blt.quiver(x, y, z, u, v, w, pivot='mid', color=['r', 'b', 'green', 'y', 'black'])
qu = blt.quiver(x, y, z, u, v, w, pivot='mid', color=np.random.random(len(x)))
'''

def quiver(x, y, z, u, v, w, pivot='middle', length=1,
           radius_shaft=0.25, radius_tip=0.5, scale=1,
           color=(0, 1, 0, 1), emission=None, roughness=1,
           vmin=None, vmax=None, color_map=None):
    """
    Plot arrows for a given vector field.

    call signature:

    quiver(x, y, z, u, v, w, pivot='middle', length=1,
           radius_shaft=0.25, radius_tip=0.5,
           color=(0, 1, 0), emission=None, roughness=1,
           vmin=None, vmax=None, color_map=None)

    Keyword arguments:
    *x, y, z*:
      x, y and z position of the data. These can be 1d arrays of the same length
      or of shape [nx, ny, nz].

    *u, v, w*
      x, y and z components of the vector field. Must be of the same shape as the
      x, y and z arrays.

    *pivot*:
      Part of the arrow around which it is rotated.
      Can be 'tail', 'mid', 'middle' or 'tip'.

    *length*:
      Length of the arrows.
      Can be a constant, an array of the same shape as
      x, y and z. If specified as string 'magnitude' use the vector's magnitude.

    *radius_shaft, radius_tip*:
      Radii of the shaft and tip of the arrows.
      Can be a constant, an array of the same shape as
      x, y and z. If specified as string 'magnitude' use the vector's magnitude
      and multiply by 0.25 for radius_shaft and 0.5 for radius_tip.

    *scale*:
        Scale the arrows (length, raddius_shaft and radius_tip).
        Can be constant or array of the same shape as x, y and z.

    *color*:
      rgba values of the form (r, g, b) with 0 <= r, g, b <= 1, or string,
      e.g. 'red' or character, e.g. 'r', or list of strings/character,
      or [n, 3] array with rgba values or array of the same shape as input array
      or 'magnitude' (use vector length).

    *emission*
      Light emission by the arrows. This overrides 'alpha' and 'roughness'.
      Real number or array or 'magnitude' (use vector length).

    *roughness*:
      Texture roughness.

    *vmin, vmax*
      Minimum and maximum values for the colormap. If not specify, determine
      from the input arrays.

    *color_map*:
      Color map for the values stored in the array 'c'.
      These are the same as in matplotlib.
    """

    import inspect

    # Assign parameters to the arrow objects.
    quiver_return = Quiver3d()
    argument_dict = inspect.getargvalues(inspect.currentframe()).locals
    for argument in argument_dict:
        setattr(quiver_return, argument, argument_dict[argument])
    quiver_return.plot()
    return quiver_return


class Quiver3d(object):
    """
    Quiver class containing geometry, parameters and plotting function.
    """

    def __init__(self):
        """
        Fill members with default values.
        """

        self.x = 0
        self.y = 0
        self.z = 0
        self.u = 0
        self.v = 0
        self.w = 0
        self.length = 1
        self.radius_shaft = 0.25
        self.radius_tip = 0.5
        self.scale = 1
        self.color = (0, 1, 0, 1)
        self.emission = None
        self.roughness = 1
        self.vmin = None
        self.vmax = None
        self.color_map = None
        self.arrow_mesh = None
        self.mesh_material = None


    def plot(self):
        """
        Plot the arrows.
        """

        import bpy
        import numpy as np
        from mathutils import Vector
        from . import colors

        # Check the validity of the input arrays.
        if not isinstance(self.x, np.ndarray) or not isinstance(self.y, np.ndarray) \
           or not isinstance(self.z, np.ndarray):
            print("Error: x OR y OR z array invalid.")
            return -1
        if not isinstance(self.u, np.ndarray) or not isinstance(self.v, np.ndarray) \
           or not isinstance(self.w, np.ndarray):
            print("Error: u OR v OR w array invalid.")
            return -1
        if not (self.x.shape == self.y.shape == self.z.shape == \
                self.u.shape == self.v.shape == self.w.shape):
            print("Error: input array shapes invalid.")
            return -1

        # Check the shape of the optional arrays.
        if isinstance(self.length, np.ndarray):
            if not (self.x.shape == self.length.shape):
                print("Error: length array invalid.")
                return -1
            else:
                self.length = self.length.ravel()
        if isinstance(self.radius_shaft, np.ndarray):
            if not (self.x.shape == self.radius_shaft.shape):
                print("Error: radius_shaft array invalid.")
                return -1
            else:
                self.radius_shaft = self.radius_shaft.ravel()
        if isinstance(self.radius_tip, np.ndarray):
            if not (self.x.shape == self.radius_tip.shape):
                print("Error: radius_tip array invalid.")
                return -1
            else:
                self.radius_tip = self.radius_tip.ravel()

        # Scale the arrows.
        self.length *= self.scale
        self.radius_shaft *= self.scale
        self.radius_tip *= self.scale

        # Flatten the input array.
        self.x = self.x.ravel()
        self.y = self.y.ravel()
        self.z = self.z.ravel()
        self.u = self.u.ravel()
        self.v = self.v.ravel()
        self.w = self.w.ravel()

        # Delete existing meshes.
        if not self.arrow_mesh is None:
            bpy.ops.object.select_all(action='DESELECT')
            self.arrow_mesh.select = True
            bpy.ops.object.delete()
            self.arrow_mesh = None
        self.arrow_mesh = []

        # Delete existing materials.
        if not self.mesh_material is None:
            if isinstance(self.mesh_material, list):
                for mesh_material in self.mesh_material:
                    bpy.data.materials.remove(mesh_material)
            else:
                bpy.data.materials.remove(self.mesh_material)

        # Prepare the material colors.
        if isinstance(self.color, str):
            if self.color == 'magnitude':
                self.color = np.sqrt(self.u**2 + self.v**2 + self.w**2)
        color_rgba = colors.make_rgba_array(self.color, self.x.shape[0],
                                          self.color_map, self.vmin, self.vmax)

        # Prepare the materials list.
        self.mesh_material = []

        # Plot the arrows.
        for idx in range(len(self.x)):
            # Determine the length of the arrow.
            magnitude = np.sqrt(self.u[idx]**2 + self.v[idx]**2 + self.w[idx]**2)
            normed = np.array([self.u[idx], self.v[idx], self.w[idx]])/magnitude
            rotation = Vector((0, 0, 1)).rotation_difference([self.u[idx], self.v[idx], self.w[idx]]).to_euler()

            # Define the arrow's length.
            if isinstance(self.length, np.ndarray):
                length = self.length[idx]
            elif self.length == 'magnitude':
                length = magnitude
            else:
                length = self.length

            # Define the arrow's radii.
            if isinstance(self.radius_shaft, np.ndarray):
                radius_shaft = self.radius_shaft[idx]
            else:
                radius_shaft = self.radius_shaft
            if isinstance(self.radius_tip, np.ndarray):
                radius_tip = self.radius_tip[idx]
            else:
                radius_tip = self.radius_tip

            if self.pivot == 'tail':
                location = [self.x[idx] + length*normed[0]/2,
                            self.y[idx] + length*normed[1]/2,
                            self.z[idx] + length*normed[2]/2]
            if self.pivot == 'tip':
                location = [self.x[idx] - length*normed[0]/2,
                            self.y[idx] - length*normed[1]/2,
                            self.z[idx] - length*normed[2]/2]
            if self.pivot == 'mid' or self.pivot == 'middle':
                location = [self.x[idx], self.y[idx], self.z[idx]]
            location = np.array(location)

            # Construct the arrow using a cylinder and cone.
            bpy.ops.mesh.primitive_cylinder_add(radius=radius_shaft, depth=length/2,
                                                location=location-normed*length/4, rotation=rotation)
            self.arrow_mesh.append(bpy.context.object)
            bpy.ops.mesh.primitive_cone_add(radius1=radius_tip, radius2=0, depth=length/2,
                                            location=location+normed*length/4, rotation=rotation)
            self.arrow_mesh.append(bpy.context.object)

            self.__set_material(idx, color_rgba)

        # Group the meshes together.
        for mesh in self.arrow_mesh[::-1]:
            mesh.select_set(state=True)
        bpy.ops.object.join()
        self.arrow_mesh = bpy.context.object
        self.arrow_mesh.select_set(state=False)

        return 0


    def __set_material(self, idx, color_rgba):
        """
        Set the mesh material.

        call signature:

        __set_material(idx, color_rgba):

        Keyword arguments:

        *idx*:
          Index of the material.

        *color_rgba*:
          The rgba values of the colors to be used.
        """

        import bpy
        import numpy as np

        # Deterimne if we need a list of materials, i.e. for every arrow mesh one.
        if any([isinstance(self.color, np.ndarray),
                isinstance(self.emission, np.ndarray),
                isinstance(self.roughness, np.ndarray),
                isinstance(self.color, list),
                isinstance(self.emission, list),
                isinstance(self.roughness, list)]):
            list_material = True
        else:
            list_material = False

        # Transform single values to arrays.
        if list_material:
            if color_rgba.shape[0] != self.x.shape[0]:
                print('color_rgba.shape = {0}'.format(color_rgba.shape))
                color_rgba = np.repeat(color_rgba, self.x.shape[0], axis=0)
                print('color_rgba.shape = {0}'.format(color_rgba.shape))
            if not isinstance(self.roughness, np.ndarray):
                self.roughness = np.ones(self.x.shape[0])*self.roughness
            if not self.emission is None:
                if not isinstance(self.emission, np.ndarray):
                    self.emission = np.ones(self.x.emission[0])*self.emission

        # Set the material.
        if list_material:
            self.mesh_material.append(bpy.data.materials.new('material'))
            self.arrow_mesh[2*idx].active_material = self.mesh_material[idx]
            self.arrow_mesh[2*idx+1].active_material = self.mesh_material[idx]
        else:
            if idx == 0:
                self.mesh_material.append(bpy.data.materials.new('material'))
                self.mesh_material[0].diffuse_color = color_rgba[idx]
            self.arrow_mesh[2*idx].active_material = self.mesh_material[0]
            self.arrow_mesh[2*idx+1].active_material = self.mesh_material[0]

        # Set the diffusive color.
        if list_material:
            self.mesh_material[idx].diffuse_color = color_rgba[idx]
        else:
            self.mesh_material[0].diffuse_color = color_rgba[0]

#        # Set the material alpha value.
#        if list_material:
#            if isinstance(self.alpha, np.ndarray):
#                self.mesh_material[idx].alpha = self.alpha[idx]
#                if self.alpha[idx] < 1.0:
#                    self.mesh_material[idx].transparency_method = 'Z_TRANSPARENCY'
#                    self.mesh_material[idx].use_transparency = True
#            else:
#                self.mesh_material[idx].alpha = self.alpha
#                if self.alpha < 1.0:
#                    self.mesh_material[idx].transparency_method = 'Z_TRANSPARENCY'
#                    self.mesh_material[idx].use_transparency = True
#        elif idx == 0:
#            self.mesh_material[0].alpha = self.alpha
#            if self.alpha < 1.0:
#                self.mesh_material[0].transparency_method = 'Z_TRANSPARENCY'
#                self.mesh_material[0].use_transparency = True

        # Set the material roughness.
        if list_material:
            if isinstance(self.roughness, np.ndarray):
                self.mesh_material[idx].roughness = self.roughness[idx]
            else:
                self.mesh_material[idx].roughness = self.roughness
        elif idx == 0:
            self.mesh_material[0].roughness = self.roughness

        # Set the material emission.
        if not self.emission is None:
            if list_material:
                self.mesh_material[idx].use_nodes = True
                node_tree = self.mesh_material[idx].node_tree
                nodes = node_tree.nodes
                # Remove Diffusive BSDF node.
                nodes.remove(nodes[1])
                node_emission = nodes.new(type='ShaderNodeEmission')
                # Change the input of the ouput node to emission.
                node_tree.links.new(node_emission.outputs['Emission'],
                                    nodes[0].inputs['Surface'])
                # Adapt emission and color.
                node_emission.inputs['Color'].default_value = tuple(color_rgba[idx]) + (1, )
                if isinstance(self.emission, np.ndarray):
                    node_emission.inputs['Strength'].default_value = self.emission[idx]
                else:
                    node_emission.inputs['Strength'].default_value = self.emission
            else:
                self.mesh_material[0].use_nodes = True
                node_tree = self.mesh_material[0].node_tree
                nodes = node_tree.nodes
                # Remove Diffusive BSDF node.
                nodes.remove(nodes[1])
                node_emission = nodes.new(type='ShaderNodeEmission')
                # Change the input of the ouput node to emission.
                node_tree.links.new(node_emission.outputs['Emission'],
                                    nodes[0].inputs['Surface'])
                # Adapt emission and color.
                node_emission.inputs['Color'].default_value = color_rgba[idx] + (1, )
                if isinstance(self.emission, np.ndarray):
                    node_emission.inputs['Strength'].default_value = self.emission
                else:
                    node_emission.inputs['Strength'].default_value = self.emission



'''
Test:
import numpy as np
import importlib
import sys
sys.path.append('~/codes/blendaviz')
import blendaviz as blt
importlib.reload(blt)
importlib.reload(blt.plot3d)
x = np.linspace(-2, 2, 5)
y = np.linspace(-2, 2, 5)
z = np.linspace(-2, 2, 5)
xx, yy, zz = np.meshgrid(x, y, z)
phi = np.sin(3*xx) + np.cos(2*yy) + np.sin(zz)
iso = blt.contour(phi)
'''

# TODO:
# - 1) Find surface of constant phi.
# - 2) Define mesh for constant phi.
# - 3) Add material.
# - 4) Add custom contour levels.

def contour(phi, x, y, z, contours=3,
           color=(0, 1, 0), alpha=1, emission=None, roughness=1,
           vmin=None, vmax=None, color_map=None):
    """
    Plot contours to a given scalar field.

    call signature:

    quiver(phi, x, y, z, contours=3,
           color=(0, 1, 0), alpha=1, emission=None, roughness=1,
           vmin=None, vmax=None, color_map=None):

    Keyword arguments:
    *phi*:
      Scalar of shape [nx, ny, nz].

    *x, y, z*:
      x, y and z position of the data. These can be 1d arrays of the same length
      or of shape [nx, ny, nz].

    *contours*
      Number of contours to be plotted, or array of contour levels.

    *color*:
      rgba values of the form (r, g, b) with 0 <= r, g, b <= 1, or string,
      e.g. 'red' or character, e.g. 'r', or list of strings/character,
      or [n, 3] array with rgba values or array of the same shape as input array.

    *alpha*:
      Alpha (opacity) value for the contours.

    *emission*
      Light emission by the contours. This overrides 'alpha' and 'roughness'.

    *roughness*:
      Texture roughness.

    *vmin, vmax*
      Minimum and maximum values for the colormap. If not specify, determine
      from the input arrays.

    *color_map*:
      Color map for the values stored in the array 'c'.
      These are the same as in matplotlib.
    """

    import inspect

    # Assign parameters to the arrow objects.
    contour_return = Contour3d()
    argument_dict = inspect.getargvalues(inspect.currentframe()).locals
    for argument in argument_dict:
        setattr(contour_return, argument, argument_dict[argument])
    contour_return.plot()
    return contour_return


class Contour3d(object):
    """
    Contour class containing geometry, parameters and plotting function.
    """

    def __init__(self):
        """
        Fill members with default values.
        """

        self.phi = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.color = (0, 1, 0)
        self.alpha = 1
        self.emission = None
        self.roughness = 1
        self.vmin = None
        self.vmax = None
        self.color_map = None
        self.contour_mesh = None
        self.mesh_material = None


    def plot(self):
        """
        Plot the contours.
        """

        import bpy
        import numpy as np
        from . import colors

        # Check the validity of the input arrays.
        if not isinstance(self.x, np.ndarray) or not isinstance(self.y, np.ndarray) \
           or not isinstance(self.z, np.ndarray):
            print("Error: x OR y OR z array invalid.")
            return -1
        if not (self.x.shape == self.y.shape == self.z.shape == self.phi.shape):
            print("Error: input array shapes invalid.")
            return -1

        # Flatten the input array.
        self.phi = self.phi.ravel()
        self.x = self.x.ravel()
        self.y = self.y.ravel()
        self.z = self.z.ravel()

        # Delete existing meshes.
        if not self.contour_mesh is None:
            bpy.ops.object.select_all(action='DESELECT')
            self.contour_mesh.select = True
            bpy.ops.object.delete()
            self.contour_mesh = None
        self.contour_mesh = []

        # Delete existing materials.
        if not self.mesh_material is None:
            if isinstance(self.mesh_material, list):
                for mesh_material in self.mesh_material:
                    bpy.data.materials.remove(mesh_material)
            else:
                bpy.data.materials.remove(self.mesh_material)

        # Prepare the material colors.
        if isinstance(self.color, str):
            if self.color == 'magnitude':
                self.color = np.sqrt(self.u**2 + self.v**2 + self.w**2)
        color_rgba = colors.make_rgba_array(self.color, self.x.shape[0],
                                          self.color_map, self.vmin, self.vmax)

        # Prepare the materials list.
        self.mesh_material = []

        # Plot the arrows.
        for idx in range(len(self.x)):
            # Determine the length of the arrow.
            magnitude = np.sqrt(self.u[idx]**2 + self.v[idx]**2 + self.w[idx]**2)
            normed = np.array([self.u[idx], self.v[idx], self.w[idx]])/magnitude
            rotation = Vector((0, 0, 1)).rotation_difference([self.u[idx], self.v[idx], self.w[idx]]).to_euler()

            # Define the arrow's length.
            if isinstance(self.length, np.ndarray):
                length = self.length[idx]
            elif self.length == 'magnitude':
                length = magnitude
            else:
                length = self.length

            # Define the arrow's radii.
            if isinstance(self.radius_shaft, np.ndarray):
                radius_shaft = self.radius_shaft[idx]
            else:
                radius_shaft = self.radius_shaft
            if isinstance(self.radius_tip, np.ndarray):
                radius_tip = self.radius_tip[idx]
            else:
                radius_tip = self.radius_tip

            if self.pivot == 'tail':
                location = [self.x[idx] + length*normed[0]/2,
                            self.y[idx] + length*normed[1]/2,
                            self.z[idx] + length*normed[2]/2]
            if self.pivot == 'tip':
                location = [self.x[idx] - length*normed[0]/2,
                            self.y[idx] - length*normed[1]/2,
                            self.z[idx] - length*normed[2]/2]
            if self.pivot == 'mid' or self.pivot == 'middle':
                location = [self.x[idx], self.y[idx], self.z[idx]]
            location = np.array(location)

            # Construct the arrow using a cylinder and cone.
            bpy.ops.mesh.primitive_cylinder_add(radius=radius_shaft, depth=length/2,
                                                location=location-normed*length/4, rotation=rotation)
            self.arrow_mesh.append(bpy.context.object)
            bpy.ops.mesh.primitive_cone_add(radius1=radius_tip, radius2=0, depth=length/2,
                                            location=location+normed*length/4, rotation=rotation)
            self.arrow_mesh.append(bpy.context.object)

            self.__set_material(idx, color_rgba)

        # Group the meshes together.
        for mesh in self.arrow_mesh[::-1]:
            mesh.select = True
        bpy.ops.object.join()
        self.arrow_mesh = bpy.context.object
        self.arrow_mesh.select = False

        return 0


    def __set_material(self, idx, color_rgba):
        """
        Set the mesh material.

        call signature:

        __set_material(idx, color_rgba):

        Keyword arguments:

        *idx*:
          Index of the material.

        *color_rgba*:
          The rgba values of the colors to be used.
        """

        import bpy
        import numpy as np

        # Deterimne if we need a list of materials, i.e. for every arrow mesh one.
        if any([isinstance(self.color, np.ndarray),
                isinstance(self.alpha, np.ndarray),
                isinstance(self.emission, np.ndarray),
                isinstance(self.roughness, np.ndarray)]):
            list_material = True
        else:
            list_material = False

        # Transform single values to arrays.
        if list_material:
            if color_rgba.shape[0] != self.x.shape[0]:
                print('color_rgba.shape = {0}'.format(color_rgba.shape))
                color_rgba = np.repeat(color_rgba, self.x.shape[0], axis=0)
                print('color_rgba.shape = {0}'.format(color_rgba.shape))
            if not isinstance(self.alpha, np.ndarray):
                self.alpha = np.ones(self.x.shape[0])*self.alpha
            if not isinstance(self.roughness, np.ndarray):
                self.roughness = np.ones(self.x.shape[0])*self.roughness
            if not self.emission is None:
                if not isinstance(self.emission, np.ndarray):
                    self.emission = np.ones(self.x.emission[0])*self.emission

        # Set the material.
        if list_material:
            self.mesh_material.append(bpy.data.materials.new('material'))
            self.arrow_mesh[2*idx].active_material = self.mesh_material[idx]
            self.arrow_mesh[2*idx+1].active_material = self.mesh_material[idx]
        else:
            if idx == 0:
                self.mesh_material.append(bpy.data.materials.new('material'))
                self.mesh_material[0].diffuse_color = color_rgba[idx]
            self.arrow_mesh[2*idx].active_material = self.mesh_material[0]
            self.arrow_mesh[2*idx+1].active_material = self.mesh_material[0]

        # Set the diffusive color.
        if list_material:
            self.mesh_material[idx].diffuse_color = color_rgba[idx]
        else:
            self.mesh_material[0].diffuse_color = color_rgba[0]

        # Set the material alpha value.
        if list_material:
            if isinstance(self.alpha, np.ndarray):
                self.mesh_material[idx].alpha = self.alpha[idx]
                if self.alpha[idx] < 1.0:
                    self.mesh_material[idx].transparency_method = 'Z_TRANSPARENCY'
                    self.mesh_material[idx].use_transparency = True
            else:
                self.mesh_material[idx].alpha = self.alpha
                if self.alpha < 1.0:
                    self.mesh_material[idx].transparency_method = 'Z_TRANSPARENCY'
                    self.mesh_material[idx].use_transparency = True
        elif idx == 0:
            self.mesh_material[0].alpha = self.alpha
            if self.alpha < 1.0:
                self.mesh_material[0].transparency_method = 'Z_TRANSPARENCY'
                self.mesh_material[0].use_transparency = True

        # Set the material roughness.
        if list_material:
            if isinstance(self.roughness, np.ndarray):
                self.mesh_material[idx].roughness = self.roughness[idx]
            else:
                self.mesh_material[idx].roughness = self.roughness
        elif idx == 0:
            self.mesh_material[0].roughness = self.roughness

        # Set the material emission.
        if not self.emission is None:
            if list_material:
                self.mesh_material[idx].use_nodes = True
                node_tree = self.mesh_material[idx].node_tree
                nodes = node_tree.nodes
                # Remove Diffusive BSDF node.
                nodes.remove(nodes[1])
                node_emission = nodes.new(type='ShaderNodeEmission')
                # Change the input of the ouput node to emission.
                node_tree.links.new(node_emission.outputs['Emission'],
                                    nodes[0].inputs['Surface'])
                # Adapt emission and color.
                node_emission.inputs['Color'].default_value = tuple(color_rgba[idx]) + (1, )
                if isinstance(self.emission, np.ndarray):
                    node_emission.inputs['Strength'].default_value = self.emission[idx]
                else:
                    node_emission.inputs['Strength'].default_value = self.emission
            else:
                self.mesh_material[0].use_nodes = True
                node_tree = self.mesh_material[0].node_tree
                nodes = node_tree.nodes
                # Remove Diffusive BSDF node.
                nodes.remove(nodes[1])
                node_emission = nodes.new(type='ShaderNodeEmission')
                # Change the input of the ouput node to emission.
                node_tree.links.new(node_emission.outputs['Emission'],
                                    nodes[0].inputs['Surface'])
                # Adapt emission and color.
                node_emission.inputs['Color'].default_value = color_rgba[idx] + (1, )
                if isinstance(self.emission, np.ndarray):
                    node_emission.inputs['Strength'].default_value = self.emission
                else:
                    node_emission.inputs['Strength'].default_value = self.emission



