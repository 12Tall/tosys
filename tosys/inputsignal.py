
from math import cos, sin


class InputSignal():
    """
    输入信号函数， 并不打算与System 有太多关系。只共用了dt 步长
    """

    def constant(val=1):
        """
        常数信号: f(t) = 1
        """
        return lambda t: val

    def sin(Amplitude=1, omega=1, Phi=0):
        """
        正弦信号: f(t) = A*sin(omega*t+phi)
        """
        return lambda t: Amplitude * sin(omega*t + Phi)

    def cos(Amplitude=1, omega=1, Phi=0):
        """
        余弦信号: f(t) = A*cos(omega*t+phi)
        """
        return lambda t: Amplitude * cos(omega*t + Phi)

    def dirac(dt=0.001):
        """
        狄拉克函数: f(t) = delta(t)，也叫单位冲激函数
        """
        val = 1/dt
        _flag = True

        def delta(t):
            nonlocal _flag
            if _flag and (t >= 0):
                _flag = False
                return val
            else:
                return 0
        return delta

    def heaviside():
        """
        赫维赛德函数: f(t) = delta(t)，也叫单位阶跃函数
        """
        _flag = True

        def h(t):
            nonlocal _flag
            if _flag and (t < 0):
                return 0
            else:
                _flag = False
                return 1
        return h

    def delay(t0=0):
        """
        延时函数: f(t) = g(t-t0)
        """
        def g(t):
            _t = t-t0
            if _t <= 0:
                return 0
            else:
                return _t
        return g

    def diff(dt=0.001):
        """
        微分函数: f(t) = g'(t)
        """
        t0 = 0

        def g(t):
            nonlocal t0
            res = t-t0
            t0 = t
            return res
        return g

    def int(dt=0.001):
        """
        积分函数: f(t) = H(t)
        """
        res = 0

        def H(t):
            nonlocal res
            res += t*dt
            return res
        return H

    def squre(width=1):
        """
        方波信号: 
        """

        def wave(t):
            if int(t/width)%2 ==0:  
                return 1
            else:
                return 0
        return wave
