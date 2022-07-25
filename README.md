# SimplePythonRaycaster
A simple raycaster implemented in Python using PyGame. The map is randomly generated using simplex noise, and the walls can be destroyed. Also features a 2d minimap.

## Controls
* __Up__ and __down__ to move forward and back
* __Left__ and __right__ to rotate view
* __Alt__ + (__Left__ or __right__) to strafe
* __M__ to toggle the 2d minimap
* __Space__ to delete the wall in front of the crosshair (use this if you spawn inside a wall)

## Screenshots
<img src="images/raycaster_screenshot1.png" alt="drawing" width="500px"/>
<img src="images/raycaster_screenshot2.png" alt="drawing" width="500px"/>

## Useful Resources
* [RayCastingTutorial](https://github.com/vinibiavatti1/RayCastingTutorial)
* [lodev.org - Raycasting](https://lodev.org/cgtutor/raycasting.html)

## Dependencies
Submit an issue if this project doesn't work with the latest versions of these libraries.
* [PyGame](https://pypi.org/project/pygame/)
* [opensimplex](https://pypi.org/project/opensimplex/)

Alternatively, you can install the libraries using:
`python -m pip install -r requirements.txt`

## Contributing
I don't plan on accepting pull requests, this is a small personal project.
