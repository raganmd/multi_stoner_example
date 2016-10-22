# IBERA #

## Contributing Programers / Artists ##

**Matthew Ragan** | [ matthewragan.com](http://matthewragan.com)  

## Overview ##

The large idea here is to sort out the complications of calibration, mapping, and previs for the next programmer. It's important to remember that in TouchDesigner, ideally you want to draw a single output window that spans all of your displays. Drawing additional windows nearly _always_ creates performance problems, and is not recommended. The developer working on the final output should know that they need only to format their final texture as a single continuous 6400 x 720 image. The container_calibration tox will break apart that texture into segments for each quad, and allow for any needed distortion to match the real world geometry.

A sample file has been included:
_*assets/sample_output.jpg*_

Here you can see how each section of the input texture is broken apart for the installation. 

For the most part, elements are broken into separate toxes based on their modular role. When possible the UI takes advantage of selecting components rather than drawing them all at once, you can see examples of this in the base_ui_elements directory. Here each side panel and body component are developed independently from the UI, and then selected when clicked. This generally makes for faster development, and allows for changes to single modules that won't affect the entire UI.

Nearly all functions / methods are kept out of execute operators. Instead, methods are written as class functions and then called by UI elements. For example, a function "Load_test_media()" is not located in the button to load media, but instead in the Calibration Class. The benefit here is a centralization of methods making for fast changes, file diffing, and easier development. A single method can be written and called from any number of locations, and changed in a single location... as opposed to functions spread across a network. 

When possible comments have been included inline in methods, print debugging lines have been left in for the next programmer, and to the best of my ability I've included doc strings. 

## Color Coding ##
Sea-foam Green - Indicates that a component is saved as a tox

## Calibration ##
Features:
* Easily move between mapping, previs, and loading test media
* Mapping uses a stoner component with key stoning and grid warping
* Mapping is unique per output display
* Offset maps are saved as their own look-ups
* Maps update output in real time
* Maps use a re-map top for faster performance - this vs. multiple stoner components

## Previs ##
Features:
* Multiple camera locations
* Test media is displayed on the model

## Test Media ##
* Load any panoramic media to see how it will look on the model
* Load and map media without needed the complete live input pipeline