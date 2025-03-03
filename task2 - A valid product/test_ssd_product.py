import unittest

from ssd_product import SSDProduct


class TestSSDProduct(unittest.TestCase):
    def test_valid_data(self):
        data = {
            "brand": "Kingston",
            "capacity": 512,
            "nvme": False,
            "read_speed": 550,
            "interface": "SATA"
        }
        product = SSDProduct(data)
        self.assertEqual(product.brand, "Kingston")
        self.assertEqual(product.capacity, 512)
        self.assertFalse(product.nvme)
        self.assertEqual(product.read_speed, 550)
        self.assertIsNone(product.write_speed)
        self.assertEqual(product.interface, "SATA")

    def test_invalid_brand(self):
        data = {
            "brand": 123,  # неверный тип
            "capacity": 512,
            "nvme": False,
            "read_speed": 550,
            "interface": "SATA"
        }
        with self.assertRaises(ValueError):
            SSDProduct(data)

    def test_invalid_interface(self):
        data = {
            "brand": "Intel",
            "capacity": 256,
            "nvme": True,
            "read_speed": 2000,
            "interface": "USB"  # недопустимое значение
        }
        with self.assertRaises(ValueError):
            SSDProduct(data)


if __name__ == '__main__':
    unittest.main()
