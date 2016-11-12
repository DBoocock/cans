cans
====

Bulletin
--------

11/11/16 - The code here was written for a masters project. I am
currently in the process of refactoring and creating examples. The
features of cans were intertwined with its original application\: to
infer parameters for a model describing cell growth in QFA
experiments. I intend to create separate packages: one for
constructing, simulating, and fitting models; the other for the
specific application of fitting QFA data. The description below is
likely to change during this process as I add new features and
capabilities.
.. see the todo list

Features
--------

- Construct reaction-diffusion models using a 2D rectangular array
  of compartments
- Define reactions within compartments
- Define diffusion reactions between nearest neighbouring
  compartments
- Generate SBML models for an arbitrary sized array
- Simulate models using libRoadRunner
- Fit models to species timecourse observations using a gradient
  method
- Plot observed, simulated, and estimated timecourses
- So far, I have only used the package to simulate deterministic ODE
  models

Related Packages
----------------

- The (to be) separate qfa package uses cans for fitting a predefined
  model (described below) to QFA data. It can make quick initial
  parameter guesses for this specific model.

Description
-----------

cans was originally developed to model the growth of an array of cell
cultures on the surface of a solid agar, and in particular, to account
for interactions between neighbouring cultures. cans is an acronym for
Cells, Arrest, Nutrients, and Signalling - species and processes
considered in the original model.

It is possible to model other systems by defining new reactions and
species. cans will generate SBML models for an arbitrary array size
from a set of reactions common to each compartment. Models can be
simulated, and results can be plotted. Given a set of initial
parameters, cans will also fit models to species timecourses. The
original application of cans, to model microbial growth in
Quantitative Fitness Analysis (QFA) experiments, provides an
illustrative example of the intended use and capabilities.

An Example: Modelling QFA and fitting data
------------------------------------------

The image below is from a typical QFA experiment showing a rectangular
array of cell cultures growing on the surface of a solid agar. Cell
density timecourses are measured for as each spot grows. These are fit
with a growth model and inferred parameters are used to quantify cell
fitness.

.. image:: http://farm6.staticflickr.com/5310/5658435523_c2e43729f1_b.jpg
   :width: 600px
   :alt: Photograph of an array of cell cultures on a QFA agar

To grow, cells consume nutrients which diffuse through the agar. The
locations of cells are fixed; there is some outward growth, but
cultures should not merge and cell density is measured rather than
culture area. Nutrients, on the other hand, are free to diffuse
through the agar between culture locations, creating a possible
competition effect between fast and slow growing neighbours. Below is
a schematic of the model: each culture and its surrounding area is
given a compartment; arrows represent nutrient diffusion between
compartments.

.. image:: https://cloud.githubusercontent.com/assets/14029228/20231386/56343f2e-a859-11e6-9bdb-6eb92a36ba5d.png
   :width: 400px
   :alt: Schematic of a network growth-diffusion model for QFA

We may model nutrient fuelled cell division within a compartment by
the reaction equation

.. math::
    C + N \rightarrow 2C,

where C is a cell and N is an amount of nutrients required for a
division. Assuming
`mass-action kinetics`_ and
assuming that the number of cells is continuous, we model the cell
dynamics as a simple first order reaction in a well-stirred vessel:

.. _mass-action kinetics: https://en.wikipedia.org/wiki/Law_of_mass_action

.. math::
   \frac{dC}{dt} &= bNC,\ \ \ \ \ \ \ \ \ \ \frac{dN}{dt} &= -bNC,

where N and C are concentrations and b is a rate constant for the
reaction. We may model the diffusion of nutrients out of a culture
:math:`i` by the reaction equation(s)

.. math::

  N_{i} \rightarrow N_{j} \ \ \ \ \ \forall\ j \in \delta_{i},

where :math:`\delta_{i}` are the nearest neighbours (dark blue
spots). We can again assume mass action kinetics for these
reactions. Considering the sum of diffusion reactions in both
directions between :math:`i` and its nearest neighbours, we modify the
rate equation for N to arrive at a model of competition:

.. math::
   \frac{dC_{i}}{dt} = b_{i}N_{i}C_{i},\ \ \ \ \ \ \ \ \ \ \frac{dN_{i}}{dt} = - b_{i}N_{i}C_{i} - k\sum_{j \epsilon \delta_i}(N_{i} - N_{j}).

Here k is a nutrient diffusion constant which is the same for all
diffusion reactions.

Defining a Model
________________

The QFA model can be defined using the following syntax:

::

   height = 1
   width = 1
   edge_width = 1
   consts = k, C(0), N(0)
   C + N -> 2C; b*C*N
   N -> _N; k*N

The two reactions can be repeated for each compartment in an array to
model networks of arbitrary size. The definition is explained as
follows:

- The first three lines define internal, edge, and corner compartment
  sizes (defaults to unit volume). Currently, the four edges must be
  treated equally.
- consts is a list of parameters that are constant for all
  compartments in the array. For this model, this is :math:`k`, and
  the initial amount of cells and nutrients. The notation X(0) is
  reserved to specify the initial amount of species X.
- Notice that b is not contained is consts causing each compartment to
  be given a separate parameter.
- The underscore in the second reaction "_N" signifies that the
  species has left the original reaction volume.
- The rate of each reaction is given by an expression after the
  semicolon where species from the left hand side now represent
  concentrations. These can be changed to represent dynamics other
  than mass action kinetics.


Simulating and fitting
______________________


Simulation from inferred parameters for a 12x20 zone of a QFA
plate. Crosses are cell density observations, blue lines are inferred
cells, yellow lines are inferred nutrients (unobserved).

.. image:: https://cloud.githubusercontent.com/assets/14029228/20231510/58eacd04-a85a-11e6-92bf-487db9c04f91.png
   :width: 800px
   :alt: 12x20 simulation of a fit to a QFA plate

A larger plot of the boxed zone above, showing fits of two models: the
competition model (solid yellow and blue) and the logistic model (solid
red). The logistic model is equivalent to the competition model with
k=0, i.e. with no diffusion.  Also plotted is a simulation of the
competition model from initial parameters (dashed yellow and
blue). Objective function values from least squares fits are displayed
for both models.


.. image:: https://cloud.githubusercontent.com/assets/14029228/20234291/04e28ae6-a871-11e6-8590-41a20f073626.png
   :width: 600px
   :alt: 3x3 simulation of a fit to a QFA plate using two models


TODO
----

1. [ ] Todo list
2. [ ] Add examples to the README for how to create a Model, solve it,
   and plot the simulation.
3. [ ] Other examples can go in a wiki or scripts
