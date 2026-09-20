import dis



def greet(name):
      pass
      return 'Привет, ' + name + '!'


print(greet('Вася'))


dis.dis(greet)






#
# mylist = ["hello" for x in range(5)]
# myset = {x for x in range(5)}
# mydict = {x: x**x for x in range(5)}
# mygen = (x for x in range(5))
#
#
#
#
# print(mylist)
# print(myset)
# print(mydict)
# print(mygen)
#
# print(next(mygen))







# def maximumProfit(arr):
#
#     arr.append(0)
#
#     gained = 0
#     bought = None
#
#
#     for i in range(len(arr)-1):
#         if arr[i] >= arr[i+1] and bought is None:
#             continue
#
#         if arr[i] < arr[i+1] and bought is None:
#             bought = arr[i]
#             gained -= bought
#             continue
#
#         if bought is not None and arr[i] - bought  > arr[i+1] - bought:
#             gained += arr[i]
#             bought = None
#             continue
#
#         if bought is not None and arr[i] - bought  <= arr[i+1] - bought:
#             continue
#
#
#     return gained
#
#
#
# arr = [100, 180, 260, 310, 40, 535, 695]
#
#
# print(maximumProfit(arr))















# from collections import Counter
#
#
#
#
# def get_boyer_moor_major(arr: list, threshold: float = 0.5):
#     n = len(arr)
#     el1 = -1
#     c1 = 0
#
#     for el in arr:
#
#         if el == el1:
#             c1 += 1
#         elif c1 == 0:
#             el1 = el
#             c1 = 1
#         else:
#             c1 -= 1
#             continue
#
#     c1 = 0
#     for el in arr:
#         if el == el1:
#             c1 += 1
#
#     return el1, c1 / n > threshold
#
#
#
# arr = [2, 8, 8, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
#        5, 5, 5, 5, 5, 5, 1, 1, 8, 8, 8, 5, 6, 2, 2, 2, 2,
#        2, 6, 6, 6, 6]
#
# print(get_boyer_moor_major(arr))







# from docxtpl import DocxTemplate
#
#
# context = {}
# context['my'] = 'Название компании.'
# context['your'] = 'ещё надо..............'
#
#
# doc = DocxTemplate("template.docx")
# doc.render(context)
# doc.save("output.docx")
# from os.path import split

#
# import base64
# import io
#
# data_b64 = ""
#
# with open("template.docx", "rb") as f:
#     data = f.read()
#     print(type(data))
#     data_b64 = base64.b64encode(data).decode()
#     print(data_b64)
#
# with open("output.txt", "w") as f:
#     f.write(data_b64)
#
#
# with open("output.txt", "r") as f:
#     txt_data = f.read()
#     print(txt_data)
#     bin_data = base64.b64decode(txt_data)
#     print(type(bin_data))
#     b = io.BytesIO(bin_data)
#
#     context = {}
#     context['my'] = 'Название компании.'
#     context['your'] = 'ещё надо..............'
#
#
#     doc = DocxTemplate(b)
#     doc.render(context)
#     doc.save("ready.docx")


# with open("new.docx", "bw") as bf:
#     w= bf.write(bin_data)
#     print(w)
#

# mystr = "taras shakharov"
# new = "_".join([substr.capitalize() for substr in mystr.split()])
#
# import datetime
#
# print(datetime.datetime.now().strftime("%Y-%m-%d__%H-%M-%S"))

# a = lambda: [print(123), print(555)]
# print(a())

# class MyClass:
#     def __init__(self):
#         self.a = 1
#         self.b = True
#
#     def __repr__(self):
#         representation = f"class type of object: {self.__class__.__name__}\n"
#         for key, value in self.__dict__.items():
#             representation += f"{key}: {value}\n"
#
#         return representation
#
#
# obj1 = MyClass()
#
# print(obj1)


# DEBUG = dbg()
#
# print(DEBUG.val)
# print(DEBUG.toggle())
# print(DEBUG.val)
# print(DEBUG.toggle())
# print(DEBUG.val)
#


#
# class Ident:
#     def __init__(self):
#         self.level = 0
#
#     def __enter__(self):
#         self.level += 1
#         return self
#
#     def __exit__(self, exc_type, exc_value, traceback):
#         self.level -= 1
#
#     def print(self, msg):
#         print("\t" * self.level + msg)
#
#
# with Ident() as ident:
#     ident.print("hello")
#     with ident:
#         ident.print("world")
#         ident.print("!!")
#         with ident:
#             ident.print("Yhooooo!!!!")


# import time
# import functools
# # class based contextmanager
# class TmeCheck:
#     def __init__(self):
#         self.start_time = None
#         self.end_time = None
#
#     def __enter__(self):
#         self.start_time = time.time()
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.end_time = time.time()
#         print(f"function took {self.end_time - self.start_time} seconds")
#         self.start_time = None
#         self.end_time = None
#         return
#
#
# # decorator based contextmanager
# def time_check(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         res = func(*args, **kwargs)
#         res_time = time.time() - start
#         print(f"{func.__name__} took {res_time} seconds")
#         return res
#     return wrapper
#
#
#
# #@time_check
# def my_func():
#     print("hello is long......")
#     time.sleep(2)
#     print("hello is done.....")
#
#
#
# with TmeCheck():
#     my_func()
# # my_func()


# class MyClass:
#     def __init__(self):
#         self.__name = "taras"
#
#     def get_name(self):
#         return self.__name
#
#
# o = MyClass()
# print(o.get_name())
# print(o._MyClass__name)


# def getsec(arr):
#
#     return list(reversed(arr))
#
#
#
# arr = list(map(int, "3 5 0 0 4".split()))
#
# print(getsec(arr))

#
# def reqf(n):
#     if n <= 1:
#         print(1)
#         return n
#     print(n)
#
#     reqf(n-1)
#
#
# reqf(3)
