
import math
class GeometricObject:
    def __init__(self, color="green", filled=True):
        self.__color = color  # set color
        self.__filled = filled

    def getColor(self):
        return self.__color

    def setColor(self, color):
        self.__color = color

    def isFilled(self):
        if self.__filled == 1:
            status = True
        else:
            status = False
        return status

    def setFilled(self, filled):
        self.__filled = filled

    def __str__(self):
        return "color: " + self.__color + " and filled: " + str(self.__filled)


class Triangle(GeometricObject):
    def __init__(self, a=1.0, b=1.0, c=1.0) -> None:
        super().__init__()  # invoke superclass init method
        self.__a = a
        self.__b = b
        self.__c = c

    def setParameters(self, a, b, c) -> None:
        self.__a = a
        self.__b = b
        self.__c = c

    def getArea(self) -> float:
        # compute area using herons formula
        s = (self.__a + self.__b + self.__c) / 2
        x = math.sqrt(s * (s - self.__a)*(s - self.__b)*(s - self.__c))
        return x
        # return area

    def getPerimeter(self) -> float:
        # compute perimeter
        # return perimeter
        perimeter = self.__a + self.__b + self.__c
        return perimeter

    def getSemiPerimeter(self) -> float:
        #compute semiperimeter
        perimeter = self.__a + self.__b + self.__c
        semi = perimeter / 2
        return semi

    def __str__(self) -> str:
        # print string message
        # return string message
        return f"Triangle: side1 = {str(self.__a)}, side2 = {str(self.__b)}, side3 = {str(self.__c)}"



def main():

    a = float(input("Enter side1: "))
    b = float(input("Enter side2: "))
    c = float(input("Enter side3: "))
    color = input("Enter color: ")
    filled = int(input("Enter 1/0 for filled (1: true, 0: false): "))
    geom = GeometricObject(color, filled)
    triangle = Triangle(a, b, c)
    #setting our color and fill (private variables need this to be changed)
    triangle.setColor(color)
    triangle.setFilled(filled)
    #print("Triangle", triangle)
    print("The area is", triangle.getArea())
    print("The perimeter is", triangle.getPerimeter())
    print("Color is", triangle.getColor())
    print("Filled is", triangle.isFilled())
    print("Semi perimeter:", triangle.getSemiPerimeter())


main()
