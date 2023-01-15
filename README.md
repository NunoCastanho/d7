# d7
A comprehensive, simple-to-use, Python-based dice notation interpreter and roller.

```
>>> expression = DiceExpression("1d6+2")
>>> expression.roll()
5
```

Dice notation is a system used to represent different combinations of dice. It is often used in tabletop role-playing games (TTRPGs) where the number and size of the dice are represented in simple, math-like expressions.

For instance, the expression `1d6` means *"roll one six-sided die"* while `2d4+1` is *"roll two four-sided dice and add one to the result"*.

d7 goes beyond the traditional, simple rolls and interprets more complex rolling expressions normally used in various TTRPGs.

## Notation

Using the different notations below, on top of the traditional `XdY`, you can form both simple or complex dice rolling expressions. For example:
* `1d6+2` - roll one six-sided die, adding two to the result;
* `2d4rr1+1` - roll two, four-sided die, re-rolling the value one, adding one to the result;
* `3d6ro<2kh2` - roll three, six-sided dice, re-rolling the value two at most once, keeping the highest two rolls;
* `6d8rr1mi3kh3!+4` - roll six exploding, eight-sided dice, whose minimum value is three, re-rolling the value one, keeping the highest three, and adding four to the result.

There is a hierarchy between the different notations where the "least" changing ones are executed first. As such, d7 uses the following sequence when resolving dice expressions: `roll()` -> `rr|ro` -> `!` -> `mi` -> `kh|hl` -> `+|-|*|/|/^`

### <ins>Modifiers</ins>

In addition to the **+** (e.g. `1d6+1`) and **-** (e.g. `1d6-1`) notation which adds or subtracts, respectively, a value from the total sum of the rolls, you can also use the **\*** (e.g. `1d6*2`), **/** (e.g. `2d6/2`), and **/^** (e.g. `3d8/^2`) to multiply, divide (rounded down) or divide (rounded up), respectively.

The modifier is usually the last part of a dice expression.

### <ins>Re-rolling</ins>
You can use the **rr** or **ro** notation to re-roll dice, depending on a specified condition. The **rr** notation translates to "re-roll" while the **ro** means "re-roll once".

For instance, the expression `1d6rr2` translates to "roll one six-sided die, re-rolling the value two" while `1d6ro2` is "roll one six-sided die, re-rolling the value two at most once".

Each of these two notations can be paired with the "<" or ">", thus indicating if it should re-roll on lower or higher values (e.g. `1d6rr<3`).

### <ins>Minimum</ins>

Through the use of the **mi** notation, you can establish a minimum value for the roll of each dice. As such, each die whose result is lower than the defined value will be changed to that value.

For example, the expression `3d6mi2` means *"roll three size-sided dice for which the minimum roll value is 2"*.

### <ins>Keep</ins>

Using the **kh** or **kl** notations, you can keep the specified highest or lowest, respectively, dice roll values. For instance, the expression `4d6kh3` translates to *"roll four six-sided dice, keeping the highest three"*.

This notation can also be seen as dropping results instead of keeping them. For example, keeping the highest three in a roll of four dice is the same as dropping the lowest one. Similarly, keeping the lowest roll in a roll of four dice is the same as dropping the highest three.

### <ins>Explode</ins>

Rolling exploding dice is similar to rolling regular dice, with the added fact that whenever a specified value, usually the highest possible, is rolled, the die is rolled again.

Using the **!** notation, you can roll exploding dice. By omitting a value afterwards, d7 will use the highest possible die value as the exploding one.

For example, the expression `1d6!` means *"roll one six-sided die, exploding on 6"* and `1d6!3` is *"roll one six-sided die, exploding on 3"*.