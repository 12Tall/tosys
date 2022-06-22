# tosys
A toy rk4 ODE solver, inspired by State-space equation. 🍭  
基于状态空间方程和四阶龙格-库塔的微分方程数值解法。需要手动构造微分方程（组）。  

## InputSignal  
输入信号已包含：  
- [x] `constant`: 常数信号`f(t) = 1`
- [x] `sin`: 正弦信号`f(t) = A*sin(omega*t+phi)`
- [x] `dirac`: 单位冲激函数`f(t) = delta(t)`
- [x] `delay`: 延时函数`f(t) = g(t-t0)`
- [x] `diff`:  微分函数`f(t) = g'(t)`
- [x] `int`: 积分函数` f(t) = H(t)`
- [x] `squre`: 方波信号  
- [ ] `PID`: 未做验证  
- [ ] `PWM`: 未做详细验证  

需要注意的是，RK4 算法会多调用信号函数4 倍，如果信号函数内有积分或者累加运算，需要额外注意！

## Example  

### 示例一

```Python
from tosys import State, System, InputSignal
"""
模拟电容充放电的过程    
"""

R = 15  # Ohm
L = 0.1  # H
C = 0.1  # F
ui = 1    # v

square = InputSignal.squre(5)  # 输入方波信号
sys = System(0, 20, .001, input=lambda t: square(t))  # 建立系统

"""
状态方程的形式：
    u0' = ui - u0/R/C  
方程右边对应的代码：
    lambda t, state: (ui*sys.input(t)-state['u0'])/R/C)
"""
sys.addState(State("u0", 0, lambda t, state: (ui*sys.input(t)-state['u0'])/R/C))

sys.RK4()  # 求解
sys.draw() # 画图
```  

![](img/exp_01.png)  

### 示例二  
```python
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

heaviside = InputSignal.heaviside()  # 阶跃信号
delay = InputSignal.delay(2)  # 延时两秒
sys = System(0, 10, .001, input = lambda t: heaviside(delay(t)))
sys.addState(State("u0", 0, lambda t, state: state['u1']))
sys.addState(State("u1", 0, lambda t, state: sys.input(t)*3 - 3*state['u0'] - 4*state['u1']))

sys.RK4()
sys.draw()
```
![](img/exp_02.png)  

### 示例三  
```python
"""
在示例二的基础上测试PWM 输入信号
"""

# ...  

sint = InputSignal.sin(omega=1)  # 正弦信号
pwm = InputSignal.pwm(dt=0.001,period=0.25)  # PWM 波形，输入信号为占空比，下面将正弦信号作为输入
delay = InputSignal.delay(2)
sys = System(0, 20, .001, input=lambda t: pwm(sint(delay(t)) ))

# ...  
```
![](img/exp_03.png)  


因为代码中使用了大量的循环语句，所以效率不算太高。但是计算能力还算强大：可以求常见的微分方程（组）的解，也可用于计算控制系统各状态变量的时域变化情况。  

-----  
后面可能会再完善，目前要继续啃编译原理了。   
📅2022-06-21