from multiprocessing import cpu_count, Pool
from concurrent.futures import ProcessPoolExecutor
from time import time

def factorize_static(lists):
     result = []
     for number in lists:
         result.append([i for i in range(1, number + 1) if number % i == 0])
     return result

def factorize(number):
     return [j for j in range(1, number + 1) if number % j == 0]

if __name__ == '__main__':
     lists = [128, 255, 99999, 10651060]
     print('--------------------------------------------------')
     start = time()
     result1 = factorize_static(lists)
     end = time()
     for i in range(len(lists)):
         print(lists[i], ' -> ', result1[i])
     print(f'Static - time of running -> {end - start}')
     print('--------------------------------------------------')
     start = time()
     with Pool(cpu_count()) as p:
         result = p.map(factorize, lists)
     end = time()
     s = time()
     for i in range(len(lists)):
         print(lists[i], ' -> ', result1[i])
     print(f'Pool - time of running -> {end - start}')
     print('--------------------------------------------------')
     print('--------------------------------------------------')
     start = time()
     with ProcessPoolExecutor(max_workers=cpu_count()) as executor:
        executor.map(factorize, lists)
     end = time()
     s = time()
     for i in range(len(lists)):
         print(lists[i], ' -> ', result1[i])
     print(f'ProcessPoolExecutor - time of running -> {end - start}')
     print('--------------------------------------------------')