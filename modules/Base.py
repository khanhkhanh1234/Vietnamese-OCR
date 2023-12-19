from abc import ABC, abstractmethod

class Base(ABC):
    def __init__(self, device="cpu", *agf, **karg):
        pass
    
    @abstractmethod
    def __call__(self, input, *args, **kwds):
        """
        input: Should be BGR image with shape (h, w, 3)
        """
        pass
    