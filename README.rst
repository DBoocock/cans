cans
====
Mechanistic modelling and parameter estimation in microbial growth
assays

Quantitative fitness analysis creates different mutant and double
mutant microbial strains and aims to compare growth rates (a proxy for
fitness) in order to detect pairwise genetic interactions. To increase
experimental throughput many colonies are seeded and grown on the same
agar plate, potentially causing a competition effect as nutrients
diffuse through the gel.

Statistical methods of dealing with this effect include randomised
experimental design and joint estimation of growth rates, e.g. using a
hierarchical Bayesian model.

We took a different approach and formulated a *mechanistic model* of
nutrient diffusion and microbial growth.

The previous standard was to fit a logistic growth curve with two
parameters - a growth rate and carrying capacity - to each colony; we
found more consistent growth estimates - indicated by lower
coefficient of variation for each strain - using roughly half the
parameters - a growth rate for each colony, a nutrient density and a
diffusion rate.

The mechanistic model could easily be extended to jointly estimate the
growth rates of replicates - reducing the number of parameters further
- or potentially be combined with statistical approaches to joint
estimation.

Research related to the project is documented in the following paper:
Boocock D and Lawless C (2017)
Modelling Competition for Nutrients between Microbial Populations Growing on a Solid Agar Surface
doi: https://doi.org/10.1101/086835

Features
--------

- Construct reaction-diffusion models using a 2D rectangular array
  of compartments
- Define reactions within compartments
- Define diffusion reactions between neighbouring compartments
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

It is possible to defining new reactions and species to model other
systems. cans will generate SBML models for an arbitrary array size
from a set of reactions common to each compartment. Models can be
simulated and results can be plotted. Given a set of initial
parameters, cans will also fit models to species timecourses. The
original application of cans, to model microbial growth in
Quantitative Fitness Analysis (QFA) experiments, illustrates the
intended use and capabilities.

An Example: Modelling QFA and fitting data
------------------------------------------

The image below, from a typical QFA experiment, shows a rectangular
array of cell cultures growing on the surface of a solid agar. Cell
density timecourses are measured for each spot. These are fit with a
growth model and inferred parameters are used to quantify cell
fitness.

.. figure:: http://farm6.staticflickr.com/5310/5658435523_c2e43729f1_b.jpg
   :width: 600px
   :alt: Photograph of an array of cell cultures on a QFA agar

   Figure 1: Photograph of cell cultures growing in a 3x5 zone on a
   QFA agar

To grow, cells consume nutrients which diffuse through the agar. The
locations of cells are fixed; there is some outward growth, but
cultures should not merge and cell density is measured rather than
culture area. Nutrients, on the other hand, are free to diffuse
through the agar between culture locations, creating a possible
competition effect between fast and slow growing neighbours. Below is
a schematic of the model: each culture and its surrounding area is
given a compartment; arrows represent nutrient diffusion between
compartments.

.. figure:: https://cloud.githubusercontent.com/assets/14029228/20231386/56343f2e-a859-11e6-9bdb-6eb92a36ba5d.png
   :width: 400px
   :alt: Schematic of a network growth-diffusion model for QFA

   Figure 2: Schematic of a network growth-diffusion model for QFA

We model nutrient fuelled cell division within a compartment by the
reaction equation

.. image:: https://cloud.githubusercontent.com/assets/14029228/20245183/d278a8d2-a993-11e6-9473-cab94455f9f7.jpg
   :alt: Equation N + C goes to 2C

..
   .. math::
       C + N \rightarrow 2C,

where C is a cell and N is an amount of nutrients required for a
division. Assuming `mass-action kinetics`_ and assuming that the
number of cells is continuous, we model the cell dynamics as a simple
first order reaction in a well-stirred vessel:

.. _mass-action kinetics: https://en.wikipedia.org/wiki/Law_of_mass_action


.. image:: https://cloud.githubusercontent.com/assets/14029228/20245228/c3ceb0c8-a994-11e6-9263-cd5b24f06bd3.jpg
   :alt: Rate equations for C and N

..
   .. math::
      \frac{dC}{dt} = bNC,\ \ \ \ \ \ \ \ \ \ \frac{dN}{dt} = -bNC,


where N and C are concentrations and b is a rate constant for the
reaction. We may model the diffusion of nutrients out of a culture i
by the reaction equation(s)

.. image:: https://cloud.githubusercontent.com/assets/14029228/20245243/0c2afb2e-a995-11e6-8e87-c6e4cfce3114.jpg
   :alt: Equation for nutrient diffusion

..
   .. math::
     N_{i} \rightarrow N_{j} \ \ \ \ \ \forall\ j \in \delta_{i},

where delta_i are the nearest neighbours (dark blue spots). We again
assume mass action kinetics for these reactions. Considering the sum
of diffusion reactions in and out of a culture, we modify the rate
equation for N to arrive at a model of competition:

.. image:: https://cloud.githubusercontent.com/assets/14029228/20245254/3ac81818-a995-11e6-8aa2-15feefca046d.jpg
   :alt: Rate equations for competition model

..
   .. math::
      \frac{dC_{i}}{dt} = b_{i}N_{i}C_{i},\ \ \ \ \ \ \ \ \ \ \frac{dN_{i}}{dt} = - b_{i}N_{i}C_{i} - k\sum_{j \epsilon \delta_i}(N_{i} - N_{j}).

Here k is a nutrient diffusion constant which is constant over the
plate.

Defining a Model
________________

The QFA model can be defined using the following syntax:

::

   globals = k, C(0), N(0)
   C + N -> 2C; b*[C]*[N]
   N -> _N; k*[N]

The two reactions can be repeated for each compartment in an array to
model networks of arbitrary size. The definition is explained as
follows:

- globals is a list of parameters that are the same for all
  compartments in the array. For this model, this is k, and the
  initial amount of cells and nutrients. The notation X(0) is reserved
  to specify the initial amount of species X.
- Notice that b is not contained is globals so each compartment is
  given a separate parameter.
- The underscore in the second reaction "_N" signifies that the
  species has left the original reaction volume.
- The rate of each reaction is given by an expression after the
  semicolon where square brackets represent concentration. Rate
  eqautions can be changed to model different dynamics (e.g. Monod,
  Michaelis-Menten).


Simulation and Parameter Inference
__________________________________

Below are example simulations of the QFA competition model (above)
using inferred parameters. Each subplot in the array shows species
timecourses for the respective compartment on a plate. Plots were
produced using cans.

.. figure:: https://cloud.githubusercontent.com/assets/14029228/20231510/58eacd04-a85a-11e6-92bf-487db9c04f91.png
   :width: 800px
   :alt: 12x20 simulation of a fit to a QFA plate

   Figure 3: Simulation from inferred parameters for a 12x20 zone of a QFA
   plate. Crosses are cell density observations, blue lines are
   inferred cells, yellow lines are inferred nutrients (unobserved).


.. figure:: https://cloud.githubusercontent.com/assets/14029228/20234291/04e28ae6-a871-11e6-8590-41a20f073626.png
   :width: 600px
   :alt: 3x3 simulation of a fit to a QFA plate using two models

   Figure 4: A larger plot of the boxed zone in Figure 3, showing fits
   of two models: the competition model (solid yellow and blue) and
   the logistic model (solid red). The logistic model is equivalent to
   the competition model with k=0, i.e. with no diffusion. Also
   plotted is a simulation of the competition model from initial
   parameters (dashed yellow and blue). Objective function values from
   least squares fits are displayed for both models. Note that
   logistic model parameters were inferred for individual cultures
   using the `qfaR`_ package in order to use its heuristic checks.

.. _qfaR: http://qfa.r-forge.r-project.org/


..
   TODO ----
   _________

   * [ ] Refactor and remove redundancies
   * [ ] Create parser
   * [ ] Add examples to the wiki showing how to create a model, solve
      it, and plot the simulation.
   * [ ] Other examples, e.g. inference, can go in scripts
