from tosys import State, System, InputSignal
"""
模拟二阶电路的零状态响应  
电路图与参数参见: https://blog.csdn.net/qq_38972634/article/details/116405600
"""

R = 1  # Ohm
L = 0.25  # H
C = 1.3333  # F
ui = 1    # v

""" 
uc0' = uc1  
uc1' = uc2 = 3*ui - 3*uc - 4*uc1  
"""


input = InputSignal.heaviside()  # 阶跃信号
sys = System(0, 10, .001, )
sys.addState(State("u0", 0, lambda t, state: state['u1']))
sys.addState(State("u1", 0, lambda t, state: sys.input(t)*3 - 3*state['u0'] - 4*state['u1']))


sys.RK4()
sys.draw()