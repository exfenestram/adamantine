import math
from adamantine import exec_models

class Deviator:
    def __init__(self, count, mean, m2, delta, amin, amax):
        self.count = count
        self.amean = mean
        self.m2 = m2
        self.delta = delta
        self.amin = amin
        self.amax = amax

    def __call__(self, value):
        count = self.count
        mean = self.amean
        m2 = self.m2
        
        count += 1
        delta = value - mean
        mean += delta / count
        delta2 = value - mean
        m2 += delta * delta2
        if self.amin is None or value < self.amin:
            amin = value
        else:
            amin = self.amin
        if self.amax is None or value > self.amax:
            amax = value
        else:
            amax = self.amax
            
        return Deviator(count, mean, m2, delta2, amin, amax)
    
    def variance(self):
        return self.m2 / self.count
    
    def stddev(self):
        return math.sqrt(self.variance())
    
    def mean(self):
        return self.amean
    
    
    def combine(self, other):
        count = self.count + other.count
        mean = (self.count * self.amean + other.count * other.amean) / count
        delta = other.amean - self.amean
        m2 = self.m2 + other.m2 + delta * delta * self.count * other.count / count
        return Deviator(count, mean, m2, delta)
    
    def min(self):
        return self.amin
    
    def max(self):
        return self.amax
    

def apply_sequence(dev, seq):
    def apply_dev(dev, value):
        return dev(value)
    
    return exec_models.foldl(apply_dev, dev, seq)

def empty_deviator():
    return Deviator(0, 0, 0, 0, None, None)


def zscore(dev, iterator):
    mean = dev.mean()
    stddev = dev.stddev()
    for value in iterator:
        yield (value - mean) / stddev
        
