import numpy as np

class coordinate:
    """坐标类"""
    def __init__(self):
        self.base_x = np.array([[30], [0], [0], [1]])
        self.base_y = np.array([[0], [30], [0], [1]])
        self.base_z = np.array([[0], [0], [30], [1]])
        self.base_o = np.array([[0], [0], [0], [1]])
        self.coord_x = self.base_x
        self.coord_y = self.base_y
        self.coord_z = self.base_z
        self.coord_o = self.base_o





if __name__ == "__main__":
    pass