import re
import math
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

class DiceExpression:
    """
    A class representing a dice expression.
    """

    numRegex = "(100|[1-9][0-9]|[1-9])"
    modRegex = "(\+|\-|\*|\/|\/\^)"
    rerollRegex = "(ro|ro\<|ro\>|rr|rr\<|rr\>)"
    diceRegex = "^(?P<nDice>" + numRegex + ")d(?P<diceSize>" + numRegex + ")" + \
                "((?P<reroll>" + rerollRegex +")(?P<rerollValue>" +  numRegex + "))?" + \
                "((?P<min>mi)(?P<minValue>" +  numRegex + "))?" + \
                "((?P<keep>(kh|kl))(?P<keepValue>" +  numRegex + "))?" + \
                "((?P<explode>(\\!))((?P<explodeValue>" +  numRegex + ")?))?" + \
                "((?P<mod>" + modRegex + ")(?P<modValue>" + numRegex + "))?$"
    pattern = re.compile(diceRegex)

    def __init__(self, expression, maxReroll=5):
        """
        Creates a dice expression.
        """
        if not type(expression) is str:
            raise TypeError("Invalid 'expression' type.")
        if not type(maxReroll) is int:
            raise TypeError("Invalid 'maxReroll' type.")
        if maxReroll > 10:
            raise ValueError("Invalid max reroll. The maximum is 10")
        if self.pattern.match(expression) == None:
            raise ValueError("Invalid dice expression.")

        self.expression = expression
        self.maxReroll = maxReroll
        self.args = list(re.finditer(self.diceRegex, self.expression))[0].groupdict()

        self.cleanArgs()

        if self.args['minValue'] != None and self.args['minValue'] > self.args['diceSize']:
            raise ValueError("Invalid dice expression. Minimum value larger than dice size.")
        if self.args['explodeValue'] != None and self.args['explodeValue'] > self.args['diceSize']:
            raise ValueError("Invalid dice expression. Explode value larger than dice size.")

    def cleanArgs(self):
        """
        Cleans and processes the dice expression arguments.
        """
        self.args['nDice'] = int(self.args['nDice'])
        self.args['diceSize'] = int(self.args['diceSize'])
        if self.args['modValue'] != None:
            self.args['modValue'] = int(self.args['modValue'])
        if self.args['keepValue'] != None:
            self.args['keepValue'] = int(self.args['keepValue'])
        if self.args['rerollValue'] != None:
            self.args['rerollValue'] = int(self.args['rerollValue'])
        if self.args['minValue'] != None:
            self.args['minValue'] = int(self.args['minValue'])
        if self.args['explode'] != None:
            self.args['explode'] = True
            self.args['explodeValue'] = int(self.ifNone(self.args['explodeValue'], self.args['diceSize']))


    def roll(self):
        """
        Rolls this dice expression, returning the result.
        """
        dice = [Dice(self.args["diceSize"]) for i in range(self.args["nDice"])]
        rolledDice = self.recursiveRolls(dice)
        self.processMinimum(rolledDice)
        self.processKeeps(rolledDice)
        self.dice = rolledDice
        self.total = self.calculateTotal(rolledDice)
        return self.total

    def recursiveRolls(self, dice):
        """
        Rolls the list of given dice, taking into consideration re-rolls and exploding dice.

        Returns an independent list of dice.
        """
        [d.roll() for d in dice]
        result = self.processRerolls(dice)
        explodedDice = self.processExplode(result)
        if len(explodedDice) == 0:
            return result
        else:
            rolledExploded = self.recursiveRolls(explodedDice)
            result.extend(rolledExploded)
            return result

    def processRerolls(self, dice):
        """
        Re-rolls the dice in a given list of dice that need to be re-rolled.

        Returns an independent list of dice.
        """
        copiedDice = [d.copy() for d in dice]
        if self.args['reroll'] != None:
            if 'ro' in self.args['reroll']:
                sign = "==" if self.args['reroll'] == 'ro' else "<" if self.args['reroll'] == 'ro<' else ">"
                [d.roll() for d in copiedDice if eval(str(d.result()) + sign + str(self.args['rerollValue']))]
            else:
                sign = "==" if self.args['reroll'] == 'rr' else "<" if self.args['reroll'] == 'rr<' else ">"
                for d in copiedDice:
                    expression = str(d.result()) + sign + str(self.args['rerollValue'])
                    i = 0
                    while eval(expression) and i < self.maxReroll:
                        d.roll()
                        expression = str(d.result()) + sign + str(self.args['rerollValue'])
                        i += 1
        return copiedDice

    def processExplode(self, dice):
        """
        Returns a list of dice exploded from a given dice list.
        """
        if self.args['explode']:
            return [Dice(self.args["diceSize"], exploded=True) for d in dice if d.result() == self.args["explodeValue"]]
        return []

    def processMinimum(self, dice):
        """
        Adds the minimum value to the dice in a given list that do not meet the minimum value.
        """
        if self.args['min'] != None:
            [d.addRoll(self.args['minValue']) for d in dice if d.result() < self.args['minValue']]


    def processKeeps(self, dice):
        """
        Determines which dice of a given list are to kept and used in the result.
        """
        if self.args['keep'] != None:
            keepHighest = self.args['keep'] == 'kh'
            sortedDice = sorted(dice, key=Dice.result, reverse=keepHighest)
            for i in range(min(len(dice), self.args['keepValue'])):
                sortedDice[i].keepDice()
        else:
            for d in dice:
                d.keepDice()

    def calculateTotal(self, dice):
        """
        Calculates the total result of given list of dice, taking into considering any modifiers and
        which dice are to be kept.
        """
        rollsSum = sum([d.result() for d in dice if d.keep])
        mod = self.ifNone(self.args['mod'], '+')
        modValue = self.ifNone(self.args['modValue'], 0)
        roundUp = False
        if self.args['mod'] == '/^':
            mod = "/"
            roundUp = True

        result = eval(str(rollsSum) + mod + str(modValue))
        return math.floor(result) if not roundUp else math.ceil(result)

    def ifNone(self, arg, default):
        """
        Returns 'default' if 'arg' is None. Otherwise, returns 'arg'.
        """
        return default if arg == None else arg

    def toJSON(self):
        """
        Returns the JSON string for this dice expression.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)