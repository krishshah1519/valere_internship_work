import unittest
from Day1 import calculator

class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calculator.add(9,6),15)
        self.assertEqual(calculator.add(-9,-11),-20)
        self.assertEqual(calculator.add(5,-9),-4)
        self.assertEqual(calculator.add(-9,5),-4)

    def test_subtract(self):
        self.assertEqual(calculator.subtract(122,104),18)
        self.assertEqual(calculator.subtract(-122,-1),-121)
        self.assertEqual(calculator.subtract(-122,20),-142)
        self.assertEqual(calculator.subtract(22,-10),32)

    def test_multiply(self):
        self.assertEqual(calculator.multiply(12,0),0)
        self.assertEqual(calculator.multiply(12,-100),-1200)
        self.assertEqual(calculator.multiply(-12,15),-180)
        self.assertEqual(calculator.multiply(-12,-16),192)

    def test_divide(self):
        self.assertEqual(calculator.divide(10,10),1)
        self.assertEqual(calculator.divide(-100,10),-10)
        self.assertEqual(calculator.divide(100,-10),-10)
        self.assertEqual(calculator.divide(100,0),None)
        self.assertEqual(calculator.divide(0,10),0)

if __name__ == '__main__':
    unittest.main()
