"""
Fuzzy Logic (Traffic Lights Simulation)

Installation:
Assuming you have pip installed, enter the following commands in your terminal:
sudo pip install scikit-fuzzy – with regard to the mechanism implementing fuzzy logic,
sudo pip install matplotlib – with regard to the visualisation of the road junction.

Overview:
This model demonstrates the operation of traffic lights at a road junction based on input variables such as traffic
density (corresponding with time of day), car queuing (i.e. queue length at the junction), road visibility (affected by
factors like rain and fog), and the presence of emergency situations.
In the code, we define variables, membership functions, and rules for implementing fuzzy logic. This enables the
simulation of a traffic light control system, helping determine the optimal duration for the green light.

Authors:
By Maciej Zagórski and Łukasz Dawidowski

Sources:
https://scikit-fuzzy.github.io/scikit-fuzzy/ , https://github.com/scikit-fuzzy (scikit-fuzzy documentation)
https://matplotlib.org/stable/ , https://github.com/matplotlib (matplotlib documentation)
“Application of fuzzy logic to control traffic signals”
(https://pubs.aip.org/aip/acp/article-pdf/doi/10.1063/1.5112230/14186507/020045_1_online.pdf)
https://github.com/woo-chia-wei/traffic-fuzzy-control/tree/master (example of applying the fuzzy logic to the road
junction and the traffic simulation)

Usage:
* Modify the input values for “emergency”, “traffic_during_day”, “cars_queuing”, and “air_transparency” in the Animation
  class (by default, they are determined randomly; the parameter ranges can be adjusted in the TrafficLightControlSystem
  class).
* Run the code to calculate the optimal “light_duration” using the plotted membership functions and rules of implemented
   fuzzy logic.
* Visualize the results using the animation of the road junction and the real-life traffic simulation (click on the
  junction to run the animation).
"""

from Animation import Animation
import matplotlib.pyplot as plt

if __name__ == "__main__":
    a = Animation()
    a.tlcs.show_views()
    plt.show()
