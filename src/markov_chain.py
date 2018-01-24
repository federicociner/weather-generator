import numpy as np
import random


class MarkovChain(object):

    def __init__(self, states, transitions, transition_probs):
        """Initialise Markov Chain object with states, transition states, and
        matrix of transition probabilities.

        Args:
            states (list(str)): List of possible states.
            transitions (list(str)): List of possible transitions.
            transition_probs (numpy.Array): Transition matrix containing
            transition probabilities.

        """
        self.states = states
        self.transitions = transitions
        self.transition_probs = transition_probs

    def forecast_weather(self, prev_state):
        """Implements Markov Chain model to forecast the weather condition
        for a given day.

        Args:
            prev_state (str): State for the previous observation period.
        Returns:
            forecast (str): Forecasted weather condition for a given
            observation period.

        """
        print("Previous state is: ", prev_state)
