import numpy as np

# ПРАКТИЧНЕ ЗАНЯТТЯ 1(120 КОД ПОЧАТОК)

# створення масиву
# array = np.array([1, 2, 3, 4, 5])
#
# print(array)
# print(array.shape) # Розмір масиву
# print(array.dtype, "\n") # тип даних в одній комірці масиву
#
#
# # створення масиву
# array = np.array([[1, 2, 3, 4, 5],
#                  [6, 7, 8, 9, 10]])
#
# print(array)
# print(array.shape) # Розмір масиву
# print(array.dtype) # тип даних в одній комірці масиву




# порівняння швидкості для масивів та списків
# import time
#
# N = 10_000_000
# nums_list = list(range(N))
# nums_array = np.array(range(N))
#
# start = time.time()
# res = sum(nums_list)
# end = time.time()
#
# print(f"Python list: {end - start:0.5f} sec")
#
# start = time.time()
# res = np.sum(nums_array)
# end = time.time()
#
# print(f"Numpy array: {end - start:0.5f} sec")
#



# Завжди використовувати функції numpy
# цикл for -- велике зло




# створення та розміри
#
# nums = np.arange(10, 20, 2) # масив з діапазоном від 10 до 19 з кроком 2
# print(nums)
#
# nums = np.zeros(shape=(3, 4)) # масив з нулями розміром 3х4
# print(nums)
#
#
# # змінити розмір масиву
# nums = np.arange(10, 20) # масив з діапазоном від 10 до 19
# new_nums = nums.reshape((2, 5)) # зміна розміру на 2х5
# print(new_nums)



# індексація
# nums = np.arange(10, 20)
#
# print(nums)
# # print(nums[2:5]) # елементи з 2 по 4
# # print(nums[-3:]) # останні 3 елементи
# # print(nums[:4])  # перші 4 елементи
# # print(nums[2:7:2]) # елементи з 2 по 6 з кроком 2
#
# nums[2] = 0
# #nums[2:7] = 0
# nums[2:7] *= -1
#
# print(nums)



# nums = np.array([[1, 2, 3, 4, 5],
#                  [6, 7, 8, 9, 10]])
#
# print(nums.shape) # рядки, стовпці
# # для двовимірних масивів йде 2 індекси -- рядок і стовпець
#
# print(nums[1, 2]) # елемент з 1 рядка і 2 стовпця
# print(nums[1]) # весь 1 рядок
# print(nums[1, 2:4])
# print(nums[0:2, 1:4])




# булеві маски
# nums = np.array([[1, 20, 3, 4, 5],
#                  [6, 7, 8, 9, 10]])
#
# mask = nums > 7
# print(mask)
#
# print(nums[mask]) # елементи більші за 7
# nums[mask] = 0
# print(nums)
#
# # дістати числа які не відповідають масці(умові)
# # and -- &
# # or -- |
# # not -- ~
# print(nums[~mask])
#
#
# # кількість чисел що більше 7
# print(np.sum(mask))



# ПРАКТИЧНЕ ЗАНЯТТЯ 1
# Завдання 1
# nums = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# print(nums.shape)
# print(nums.dtype, "\n") # тип даних в одній комірці масиву
#
# new_nums = nums.reshape((2, 5)) # зміна розміру на 2х5
# print(new_nums)
# print(new_nums.shape)
# print(new_nums.dtype, "\n") # тип даних в одній комірці масиву

# Завдання 2
# nums = np.array([[1, 2, 3, 4],
#                  [5, 6, 7, 8],
#                     [9, 10, 11, 12]])
#
# print(nums[1, 2])
# print("\n")
#
# print(nums[1, :])
# print("\n")
#
# print(nums[:, 3])
# print("\n")
#
# print(nums[0:3, 2:4])
# print("\n")
#
# print(nums[1:3, 1:3])
# print("\n")
#
# nums[1:3, 1:3] = -1
# print(nums)
# print("\n")
#
# nums[:, 0] = nums[:, 1]
# print(nums)

# Завдання 3
# nums = np.array([[1, 2, 3, 4],
#                  [5, 6, 7, 8],
#                     [9, 10, 11, 12]])
#
# mask = nums > 6
# print(np.sum(mask))
# print("\n")
#
# print(nums[mask])
# print("\n")
#
# nums[mask] += 10
# print(nums[mask])
# print("\n")
#
# nums[~mask] *= -1
# print(nums[~mask])
# print("\n")


# Завдання 4
# nums = np.array([[-10, 24, 35],
#                  [250, -6, 7],
#                     [12, 180, 11],
#                  [-2, -45, -26]])
#
#
# mask = nums < 0
# print(nums[mask])
# print("\n")
#
# nums[mask] = 0
# print(nums[mask])
# print("\n")
#
# mask = nums > 100
# nums[mask] = 100
# print(nums[mask])
# print("\n")
#
# print(nums)


# Завдання 5
nums = np.array([100, 120, 200, 250, 10])
nums += 50
print(nums)

# nums = np.array([100, 120, 200, 250, 10], dtype = np.uint8)
# nums += 50
# print(nums)

new_nums = nums.astype(np.uint64)
nums += 50
print(nums)

mask = new_nums > 255
new_nums[mask] = 255

new_nums = new_nums.astype(np.uint8)
print(new_nums)