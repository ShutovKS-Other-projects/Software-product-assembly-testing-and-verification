class SSDProduct:
    ALLOWED_INTERFACES = ['SATA', 'NVMe', 'SAS']

    def __init__(self, data: dict):
        # Проверка обязательных полей и типов
        if 'brand' not in data or not isinstance(data['brand'], str):
            raise ValueError("Неверное значение для 'brand'")
        self.brand = data['brand']

        if 'capacity' not in data or not isinstance(data['capacity'], (int, float)):
            raise ValueError("Неверное значение для 'capacity'")
        self.capacity = data['capacity']

        if 'nvme' not in data or not isinstance(data['nvme'], bool):
            raise ValueError("Неверное значение для 'nvme'")
        self.nvme = data['nvme']

        if 'read_speed' not in data or not isinstance(data['read_speed'], (int, float)):
            raise ValueError("Неверное значение для 'read_speed'")
        self.read_speed = data['read_speed']

        # write_speed – необязательное поле
        if 'write_speed' in data:
            if not isinstance(data['write_speed'], (int, float)):
                raise ValueError("Неверное значение для 'write_speed'")
            self.write_speed = data['write_speed']
        else:
            self.write_speed = None

        if 'interface' not in data or not isinstance(data['interface'], str) or data[
            'interface'] not in self.ALLOWED_INTERFACES:
            raise ValueError("Неверное значение для 'interface'")
        self.interface = data['interface']

    @property
    def performance_index(self):
        """Индекс производительности = (read_speed + write_speed) / capacity.
        Если write_speed отсутствует, используется только read_speed."""
        total_speed = self.read_speed + (self.write_speed if self.write_speed is not None else 0)
        return total_speed / self.capacity

    def __repr__(self):
        return (f"SSDProduct(brand={self.brand}, capacity={self.capacity}, nvme={self.nvme}, "
                f"read_speed={self.read_speed}, write_speed={self.write_speed}, interface={self.interface})")


# Демонстрация работы класса
if __name__ == '__main__':
    api_answer_ssd = {
        "brand": "Samsung",
        "capacity": 1024,
        "nvme": True,
        "read_speed": 3500,
        "write_speed": 3000,
        "interface": "NVMe"
    }
    try:
        product = SSDProduct(api_answer_ssd)
        print("Продукт создан успешно:", product)
        print("Индекс производительности:", product.performance_index)
    except ValueError as e:
        print("Ошибка:", e)
