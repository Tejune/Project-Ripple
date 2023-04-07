#------------------------------------------------------------------------------------------
#   Ripple / tweens
#   Handles the creation and management of tweening and easing effetcs
#------------------------------------------------------------------------------------------

import pygame
import numpy
import math

createdTweens = []

#---------------------------------------------------------------------------------------------------------
# Interpolation methods
#---------------------------------------------------------------------------------------------------------

def linear(a: float, b: float, t: float) -> float:
    """Linear interpolate on the scale given by a to b, using t as the point on that scale.
    Examples
    --------
        50 == lerp(0, 100, 0.5)
        4.2 == lerp(1, 5, 0.8)
    """
    return (1 - t) * a + t * b

def exponential_InOut(a: float, b: float, t: float) -> float:
    """Exponential interpolation. Fading both in and out."""

    # The variable new_t represents the absolute progress of the animation in 
    # the bounds of 0 (beginning of the animation) and 1 (end of animation).

    new_t = 0
    if t == 0:
        new_t = 0
    elif t == 1:
        new_t = 1
    elif t < 0.5:
        new_t = math.pow(2, 20 * t - 10) / 2
    else:
        new_t = (2 - math.pow(2, -20 * t + 10)) / 2

    return linear(a, b, new_t)

#---------------------------------------------------------------------------------------------------------
# Tween class
#---------------------------------------------------------------------------------------------------------

class Tween:
    """Object used for handling interpolations."""

    def __init__ (self, duration: float, startValue: float, endValue: float, easingStyle: any):
        self.t = 0
        self.isPlaying = False
        self.duration = duration
        self.startValue = startValue
        self.endValue = endValue
        self.easingStyle = easingStyle
        self.currentValue = self.easingStyle(self.startValue, self.endValue, self.t)

    def step (self, deltaTime: float or int):

        # Only step if the tween is playing
        if not self.isPlaying:
            return

        # Increase t value by step value
        stepValue = deltaTime / self.duration
        self.t = min(self.t + stepValue, 1)

        # Update easing value using updated t value
        self.currentValue = self.easingStyle(self.startValue, self.endValue, self.t)
        

    def play (self):
        self.isPlaying = True
    
    def pause (self):
        self.isPlaying = False
    
    def stop (self):
        self.isPlaying = False
        self.t = 0

#---------------------------------------------------------------------------------------------------------
# General methods
#---------------------------------------------------------------------------------------------------------

def createTween (duration: float, startValue: float, endValue: float, easingStyle: any):
    """Create a new tween. Time is in milliseconds.

    --------
        tween = tweens.createTween(1000, 0, 1, tweens.linear)
        tween = tweens.createTween(600, 255, 0, tweens.linear)
    """

    # Create tween and append it to the created_tweens list
    newTween = Tween(duration, startValue, endValue, easingStyle)
    createdTweens.append(newTween)

    return newTween

def stepAllTweens (deltaTime: float or int):
    """Steps all tweens using the provided delta time."""

    for tween in createdTweens:
        tween.step(deltaTime)
