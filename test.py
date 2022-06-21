from tosys import State, System, InputSignal
"""
模拟电容充电的过程  
"""

R = 15  # Ohm
L = 0.1  # H
C = 0.1  # F
ui = 1    # v

"""
u0' = ui - u0/R/C  
"""


square = InputSignal.squre(9)

sys = System(0, 20, .001, input=lambda t: square(t))
sys.addState(State("u0", 0, lambda t, state: (sys.input(t)-state['u0'])/R/C))

sys.RK4()
sys.draw()