class A:
    def __init__(self):
        self.num_lst = [10]

    def update(self):
        self.num_lst.append(10)


class B:
    def __init__(self, num_lst, update):
        self.num_lst = num_lst
        self.update = update

    def append_num(self):
        self.update()


a = A()
b = B(a.num_lst, a.update)
b.append_num()
b.append_num()

print(a.num_lst)
print(b.num_lst)