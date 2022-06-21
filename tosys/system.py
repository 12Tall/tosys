from cProfile import label
from collections import OrderedDict
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy
from tosys.state import State


class System():
    """
    系统，用于管理状态及状态方程
    """

    def __init__(self, start=0, end=0, dt=0, input=lambda t: 1):

        def call_input(t):
            res = self._input(t)
            self._input_data.append(res)
            return res

        self.name = "system"
        self.state = OrderedDict()  # 有序字典，可以按添加顺序进行遍历，非必须
        self.equation = OrderedDict()
        self.history_index = 0
        self.history = None
        self.start = start
        self.end = end
        self.dt = dt
        self._input = input
        self._input_data = []        
        self.input = call_input

    def addState(self, state: State):
        """
        添加状态： 要求不要引用未定义的状态变量， 时间t 除外
        """
        self.state[state.name] = state.init_value
        self.equation[state.name] = state.equation

    def init_history(self):
        t = self.end - self.start
        dt = self.dt
        self.history_index = 0
        self.history = numpy.empty(
            [round(t/dt), len(self.state)], dtype=float)

    def record(self):
        """
        存储计算结果：待优化
        """
        j = 0
        for key in self.state:
            self.history[self.history_index][j] = self.state[key]
            j += 1
        self.history_index += 1

    def draw(self):
        """
        绘制各状态变量随时间变化的曲线
        """
        dt = self.dt
        ts = numpy.arange(self.start, self.end, dt)  # 时间轴
        input = numpy.reshape(self._input_data,(-1,4))[:,0]
        print(input)
        plt.plot(ts, input, label='input')

        j = 0
        for key in self.state:
            plt.plot(ts, self.history[:, j], label=key)  # 状态量
            j += 1
            
        plt.legend()
        plt.grid()
        plt.show()

    def RK4(self):
        """
        使用四阶龙格-库塔进行仿真，效果尚可
        中间使用了很多字典暂存变量，可以继续优化
        """
                
        def reset_state(state):
            """
            通过缓存来减少deepcopy 的次数
            """
            for key in state:
                state[key] = self.state[key]

        self.init_history()

        start, end, dt = self.start, self.end, self.dt
        t = end-start

        next_state = deepcopy(self.state)
        temp_state = deepcopy(self.state)

        for t in numpy.arange(start, end, dt):
            reset_state(next_state)
            for state in self.state:
                reset_state(temp_state)
                k1 = dt*self.equation[state](t, temp_state)
                for key in temp_state:
                    temp_state[key] += 0.5*k1
                k2 = dt*self.equation[state](t+0.5*k1, temp_state)
                for key in temp_state:
                    temp_state[key] += 0.5*(k2-k1)
                k3 = dt*self.equation[state](t, temp_state)
                for key in temp_state:
                    temp_state[key] += (k3-k2)
                k4 = dt*self.equation[state](t, temp_state)
                next_state[state] = self.state[state] + (k1+2*k2+2*k3+k4)/6.
            self.state = next_state
            self.record()
