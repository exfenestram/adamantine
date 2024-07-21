import math

class Deviator:
    def __init__(self, count, mean, m2, delta):
        self.count = count
        self.amean = mean
        self.m2 = m2
        self.delta = delta

    def __call__(self, value):
        count = self.count
        mean = self.amean
        m2 = self.m2
        
        count += 1
        delta = value - mean
        mean += delta / count
        delta2 = value - mean
        m2 += delta * delta2
        return Deviator(count, mean, m2, delta2)
    
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
    

def apply_sequence(dev, seq):
    def apply_dev(dev, value):
        return dev(value)
    
    return foldl(apply_dev, dev, seq)

def empty():
    return Deviator(0, 0, 0, 0)
