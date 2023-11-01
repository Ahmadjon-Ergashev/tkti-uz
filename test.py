import random

# for i in range(3):
#     print(str(random.randint(111111, 999999)))

from collections import namedtuple


NewsType = namedtuple("NewsType", ["name"])
news_type_1 = NewsType("latest")
news_type_2 = NewsType("most_read")

print(news_type_1.name)