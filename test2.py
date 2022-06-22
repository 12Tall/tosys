from tosys import State, System, InputSignal
"""
模拟二阶电路的零状态响应  
电路图与参数参见: https://blog.csdn.net/qq_38972634/article/details/116405600
"""

R = 1  # Ohm
L = 0.25  # H
C = 1.3333  # F
# ui = 1(t-2)    # v

""" 
uc0' = uc1  
uc1' = uc2 = 3*ui - 3*uc - 4*uc1  
"""

sint = InputSignal.sin(omega=1)  # 正弦信号
pwm = InputSignal.pwm(dt=0.001,period=0.25)  # PWM 波形，输入信号为占空比，下面将正弦信号作为输入
delay = InputSignal.delay(2)
sys = System(0, 20, .001, input=lambda t: pwm(sint(delay(t)) ))
sys.addState(State("u0", 0, lambda t, state: state['u1']))
sys.addState(State("u1", 0, lambda t, state: sys.input(t)
                   * 3 - 3*state['u0'] - 4*state['u1']))


sys.RK4()
sys.draw()
