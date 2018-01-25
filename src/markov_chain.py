import numpy as np


class MarkovChain(object):

    def __init__(self):
        """Initialise Markov Chain object with states, transition states, and
        matrix of transition probabilities.

        Attrs:
            states (list(str)): List of possible states.
            transitions (list(str)): List of possible transitions.
            transition_probs (numpy.Array): Transition matrix containing
            transition probabilities.

        """
        self.states = ['Sunny', 'Rain', 'Snow']
        self.transitions = [['SuSu', 'SuRn', 'SuSn'],
                            ['RnSu', 'RnRn', 'RnSn'],
                            ['SnSu', 'SnRn', 'SnSn']]
        self.transition_probs = [[0.7, 0.2, 0.1],
                                 [0.5, 0.4, 0.1],
                                 [0.7, 0.1, 0.2]]

    def snow_possible(self, temp, humidity):
        """Checks current temperature and humidity conditions to determine
        whether 'Snow' is a possible condition.

        Args:
            temp (float): Temperature for the current period.
            humidity (int): Relative humidity for the current period.
        Returns
            Boolean value indicating whether 'Snow' is possible or not
        """
        return (temp < 0.0) or (temp < 4.0 and humidity < 40)

    def forecast_weather(self, temp, humidity):
        """Implements Markov Chain model to forecast the weather condition
        for a given day based on a prior observation period.

        Args:
            temp (float): Temperature for the previous period.
            humidity (int): Relative humidity for the previous period.
        Returns:
            cond (str): Forecasted weather condition for a given
            observation period.

        """
        # set initial state based on temperature and humidity
        # if temperature and humidity conditions are right, then snow is a
        # possibility
        forecast = None
        can_snow = self.snow_possible(temp, humidity)

        if can_snow:
            forecast = np.random.choice(self.states)
        else:
            forecast = np.random.choice(
                filter(lambda x: x != 'Snow', self.states))

        # go through possible states and run Markov Chain model for each
        if forecast == 'Sunny':
            change = np.random.choice(
                self.transitions[0], replace=True, p=self.transition_probs[0])
            if change == "SuSu":
                pass
            elif change == "SuRn":
                forecast = "Rain"
            elif change == "SuSn" and can_snow:
                forecast = "Snow"
        elif forecast == 'Rain':
            change = np.random.choice(
                self.transitions[1], replace=True, p=self.transition_probs[1])
            if change == "RnSu":
                forecast = "Sunny"
            elif change == "RnRn":
                pass
            elif change == "RnSn" and can_snow:
                forecast = "Snow"
        elif forecast == 'Snow':
            change = np.random.choice(
                self.transitions[2], replace=True, p=self.transition_probs[2])
            if change == "SnSu":
                forecast = "Sunny"
            elif change == "SnRn":
                forecast = "Rain"
            elif change == "SnSn":
                pass

        return forecast
