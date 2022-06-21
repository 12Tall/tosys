
import string


class State:
    """
    状态变量及其对应的方程，
    如：
    y' = t ==> State("y", 0, lambda t, state: t)
    或也可调用另外一个状态：
    z' = y ==> State("z", 0, lambda t, state: state["y"])
    """

    def __init__(self, name: string, init_value: float, equation) -> None:
        self.name = name
        self.init_value = init_value
        self.equation = equation

