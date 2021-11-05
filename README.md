# Bouncing balls

### A small Python project to simulate circles bouncing with each other.

#### Requirements : 

*   Python 3.7 and its built-in modules
*   `pygame` for graphics and `matplotlib` for movement visualization
*   Speakers I guess?



#### Explanations

This project aims to simulate simple physics using circles that bounce with each other.

It creates N instances of a `Ball` class that store:

-   The `x` and `y` coordinates of the object's center position;
-   The `dx` and `dy` displacement vector;
-   The radius of the ball;
-   The color (for prettiness).



Each iteration of the main loop (every `1/FRAMERATE` seconds) moves each ball's according to its displacement vector.



##### In case of collision

##### …with a wall:

*   It changes `x` to its negative value for a vertical wall, `y` for a horizontal wall.

##### …with another object:

*   With *C1* the first ball and its center *O1*, *C2* the second ball and its center *O2*, *D* the distance between the centers and *A* and *B* the extremities of the circles on the line *(O1, O2)*, we can find the interpenetration vector's coordinates since we have:
    *   the length of *[AB]* and
    *   the vector *D*



![equation](https://latex.codecogs.com/png.latex?%5Clarge%20%7B%5Ccolor%7BRed%7D%20v%20%3D%20%28%5Cfrac%7BD_x%20%5Ctimes%20AB%7D%7B%7C%5Coverrightarrow%7BD%7D%7C%7D%2C%20%5Cfrac%7BD_y%20%5Ctimes%20AB%7D%7B%7C%5Coverrightarrow%7BD%7D%7C%7D%29%7D)



Now we have *v* the interpenetration vector directed from O2 to O1, we can just add it to C1's displacement vector to find the corrected new displacement vector.

##### C1 has bounced!

As illustrated below:

![illustration 1](./illu1.png)

We redo the process after switching *C1* and *C2* so that the other ball bounces too.

We can also simulate a mass difference between *C1* and *C2* (let's say proportional to their radius). We do not add *v* entirely, but rather

![equation](https://latex.codecogs.com/png.latex?%5Clarge%20%5C%5C%20%7B%5Ccolor%7BRed%7D%20x%20%5Cleftarrow%20x%20&plus;%20%5Cfrac%7Bv_x%20%5Ctimes%20%7Br_2%7D%7D%7Br_1%7D%20%7D%5C%5C%20%7B%5Ccolor%7BRed%7D%20y%20%5Cleftarrow%20y%20&plus;%20%5Cfrac%7Bv_y%20%5Ctimes%20%7Br_2%7D%7D%7Br_1%7D%7D)

If *r1* ≥ *r2* then *v* is proportionally decreased. Otherwise, *v* is  increased. To counter that, we normalize the total movement of the simulation so it doesn't scale-up infinitely.

