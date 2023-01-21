import random
import json


class Dice:
    """
    A class representing a rolling dice.
    """

    def __init__(self, size, keep=False, exploded=False):
        """
        Creates a dice of a given size.
        """
        if not type(size) is int:
            raise TypeError("Invalid 'size' type.")
        if size < 2 or size > 100:
            raise ValueError("The size of a dice must be between 2 and 100.")
        self.size = size
        self.keep = keep
        self.exploded = exploded
        self.history = []

    def __str__(self):
        return "{Size: " + str(self.size) + ", Keep: " + str(self.keep) + ", Exploded: " + str(self.exploded) + ", Result: " + str(self.result()) + \
               ", History: " + str(self.history) + "}"

    def __repr__(self):
       return self.__str__()

    def roll(self):
        """
        Rolls the dice and records the rolled value.
        """
        value = random.randint(1, self.size)
        self.history.append(value)

    def addRoll(self, value):
        """
        Adds a given value to the history of rolled values for this dice.
        """
        if not type(value) is int:
            raise TypeError("Invalid 'value' type.")
        if value > self.size:
            raise ValueError("The added value cannot be larger than the size of the dice.")
        self.history.append(value)

    def result(self):
        """
        Returns the most recent value for this dice. None if the dice has no value.
        """
        return self.history[-1] if len(self.history) > 0 else None

    def keepDice(self):
        """
        Sets this dice to be kept in the final calculation.
        """
        self.keep = True

    def copy(self):
        """
        Returns an independent copy of this dice.
        """
        result = Dice(self.size)
        result.keep = self.keep
        result.history = [value for value in self.history]
        result.exploded = self.exploded
        return result

    def toJSON(self):
        """
        Returns the JSON string for this dice.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)