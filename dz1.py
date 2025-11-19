import numpy as np


# Завдання 1


nums = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
])
#
# print("Число 14:", nums[3, 1])
# print("Третій рядок:", nums[2])
# print("Перший стовпчик:", nums[:, 0])
# print("Верхня половина:\n", nums[:2, :])
#
# nums2 = nums.copy()
# nums2[1:3, :] = 100
# print("Замінені рядки 2-3 на 100:\n", nums2)
#
# nums3 = nums.copy()
# nums3[1] = nums3[-1]
# print("Другий рядок як останній:\n", nums3)

# Завдання 2

# nums4 = nums.copy()
#
# mask = (nums4 % 2 == 0)
# print("Парні числа:", nums4[mask])
#
# nums4[mask] = 100
# print("Парні числа замінено на 100:\n", nums4)

# Завдання 3

a = np.array([128, 200, 10], dtype=np.uint8)
b = np.array([250, 10, 34], dtype=np.uint8)

result = (0.2 * a + 0.8 * b).astype(np.uint8)

print("Результат 20% першого + 80% другого:", result)
print("Тип даних:", result.dtype)
