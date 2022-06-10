#!/bin/python3
#runs detection on webcam and writes position to stdout for testing
import cv2
import constants

# class to smooth out position of detection across frames to avoid shakey aim
# basically just the moving average function
class smoother():
    def __init__(self, alpha : float):
        self.alpha = alpha
        self.accumulator = -1
    
    def smooth(self, value):
        if self.accumulator == -1:
            self.accumulator = value
        self.accumulator = (self.alpha * value) + ((1.0 - self.alpha) * self.accumulator)
        return self.accumulator
    
