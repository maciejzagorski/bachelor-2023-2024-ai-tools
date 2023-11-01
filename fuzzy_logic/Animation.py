import matplotlib.animation as animation
import RoadJunction as rj
import TrafficLightControlSystem as tlcs

DECREASE_CARS_RATE = 5
PARAMETERS_CHANGE_RATE = 250
EMERGENCY_THRESHOLD = 0.8


class Animator:
    """
    Animator class for controlling the animation of the road junction and the real-life traffic simulation.
    """

    def __init__(self, figure, function):
        self.animation = animation.FuncAnimation(figure, function, interval=75, cache_frame_data=False)
        self.paused = True
        figure.canvas.mpl_connect('button_press_event', self._toggle_pause)

    def _toggle_pause(self, *args, **kwargs):
        """
        Toggle the animation between paused and resumed states based on the mouse-click.
        """
        if self.paused:
            self.animation.resume()
        else:
            self.animation.pause()
        self.paused = not self.paused


class Animation:
    """
    Animation class for simulating and visualizing traffic at the road junction (the real-life traffic simulation).
    """

    def __init__(self):
        self.marker = 0
        self.tlcs = tlcs.TrafficLightControlSystem()
        self.parameters = tlcs.RandomParameters()
        self.increase_cars_rate = (self.tlcs.setup.assess_time(self.parameters.time_of_day) + 1) * 10

        self.plot = rj.RoadJunction()
        self._initialize_plot()

        self.switch_x_y = True

        self.animator = Animator(self.plot.fig, self._update)

    def _initialize_plot(self):
        """
        Initialize the plot for the traffic simulation (the road junction) based on the generated random parameters.
        """
        self.plot.fig.patch.set_alpha((100 - self.parameters.air_transparency) / 100)

        self.plot.x_plot[0].set_linewidth(self.parameters.cars_queuing_x)
        self.plot.y_plot[0].set_linewidth(self.parameters.cars_queuing_y)

    def _update(self, i):
        """
        Update the animation frame.
        """
        if i == 0:
            self.__initialize_simulation()

        if i == self.marker:
            self.__update_marker_and_switch()

        if i % self.increase_cars_rate == 0:
            self.__adjust_car_number(self.plot.x_plot[0], 1)
            self.__adjust_car_number(self.plot.y_plot[0], 1)

        if i % DECREASE_CARS_RATE == 0:
            plot_to_decrease = self.plot.x_plot[0] if self.switch_x_y else self.plot.y_plot[0]
            self.__adjust_car_number(plot_to_decrease, -1)

        if i % PARAMETERS_CHANGE_RATE == 0:
            self.__update_air_transparency()
            self.__update_emergency()

        self.__update_legend(i)

    def __initialize_simulation(self):
        """
        Initialize the simulation, including pausing the animation, switching lights, and updating the marker, i.e. the
        frame of the next lights switch.
        """
        self.animator.animation.pause()
        self.plot.switch_lights(self.switch_x_y)
        self.marker = round(
            self.tlcs.perform_simulation(self.parameters.time_of_day,
                                         self.parameters.cars_queuing_x,
                                         self.parameters.air_transparency,
                                         self.parameters.emergency)
            * 10, 0)
        print(self.marker)

    def __update_legend(self, i):
        """
        Update the legend in the plot with various simulation parameters and their current values.
        """
        legend_values = [i,
                         self.marker,
                         self.parameters.time_of_day,
                         self.plot.x_plot[0].get_linewidth(),
                         self.plot.y_plot[0].get_linewidth(),
                         self.parameters.air_transparency,
                         self.parameters.emergency]

        for idx, value in enumerate(legend_values):
            self.plot.update_legend_text(idx, value)

        if self.parameters.emergency > EMERGENCY_THRESHOLD:
            self.plot.legend.get_texts()[6].set_color('red')
        else:
            self.plot.legend.get_texts()[6].set_color('black')

    def __update_marker_and_switch(self):
        """
        Update the marker and switch lights (i.e. switch) between X and Y directions (the roads, i.e. the flows of cars
        on the roads).
        """
        new_linewidth = self.plot.y_plot[0].get_linewidth() if self.switch_x_y else self.plot.x_plot[0].get_linewidth()

        outcome = round(self.tlcs.perform_simulation(self.parameters.time_of_day,
                                                     new_linewidth,
                                                     self.parameters.air_transparency,
                                                     self.parameters.emergency)
                        * 10, 0)
        print(outcome)
        self.marker += outcome

        self.switch_x_y = not self.switch_x_y
        self.plot.switch_lights(self.switch_x_y)

        if self.parameters.emergency > EMERGENCY_THRESHOLD:
            self.parameters.change_emergency()

    def __adjust_car_number(self, plot, change):
        """
        Adjust the linewidth, i.e. the number of the cars on the given road.
        """
        new_width = plot.get_linewidth() + change
        plot.set_linewidth(max(new_width, 0))

    def __update_air_transparency(self):
        """
        Update the air transparency parameter and, based on it, adjust the figure's alpha.
        """
        self.parameters.change_air_transparency()
        self.plot.fig.patch.set_alpha((100 - self.parameters.air_transparency) / 100)

    def __update_emergency(self):
        """
        Update the emergency parameter.
        """
        self.parameters.change_emergency()
