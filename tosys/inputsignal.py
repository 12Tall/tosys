
from cmath import e
from math import cos, inf, sin


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
            if _flag and (t <= 0):
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
            if t > 0 and int(t/width) % 2 == 0:
                return 1
            else:
                return 0
        return wave

    def pwm(dt=0.001, period=1):
        """
        PWM信号: 因为4阶龙格-库塔的原因，所以pwm 的采样周期成了预期的四分之一
        """
        _duty, counter = 0, 0
        period = period*4

        def wave(duty=0.5):
            nonlocal _duty, counter

            output = 0
            if counter >= period:
                counter = 0
                _duty = duty*period
                # print(">>>>>", counter, period, _duty, duty, period*duty)

            if counter < _duty:
                output = 1
            else:
                output = 0
            counter += dt

            # print(counter, period, _duty, duty, period*duty)
            return output
        return wave

    def posPID(dt=0.001, Kp=1, Ki=0, Kd=0, limit=None):
        """
        位置式pid: 
        """
        P, I, D, L = Kp, Ki, Kd, limit
        int_err, lerr = 0, 0

        def pid(err):
            nonlocal int_err, lerr
            int_err += err
            output = P*err + I*int_err*dt + D*(err - lerr)
            lerr = err
            if limit != None and output > limit:
                return limit
            return output
        return pid

    def incPID(dt=0.001, Kp=1, Ki=0, Kd=0, limit=None):
        """
        增量式pid: 
        """
        P, I, D, L = Kp, Ki, Kd, limit
        lerr, llerr, output = 0, 0, 0

        def pid(err):
            nonlocal llerr, lerr, output
            doutput = P*(err - lerr) + I*err*dt + D*(err - 2*lerr + llerr)
            llerr = lerr
            lerr = err
            output += doutput
            if limit != None and output > limit:
                output = limit
            return output
        return pid
