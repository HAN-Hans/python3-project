def foo(x):
    print(f"{x}")


class A(object):
    # __slots__定义的属性仅对当前类起作用,对继承的子类是不起作用的
    # 除非在子类中也定义__slots__,这样,子类允许定义的属性就是自身的__slots__加上父类的__slots__
    __slots__ = ('name', 'var_of_instance')  # 限制实例属性
    var_of_class = 1  # 类属性

    def __init__(self, name):
        self.name = name
        self.var_of_instance = 0

    def foo(self, x):
        print(f"{self} -> {x}")

    @classmethod
    def class_foo(cls, x):
        print(f"{cls} ->{x}")

    @staticmethod
    def static_foo(x):
        print(f"{x}")


foo(10)
a = A("han")
print(f"{a} -> {a.var_of_class} -> {a.var_of_instance}")
print(f"{a.__class__} -> {A.var_of_class} -> {a.__class__.var_of_class}")
# 实例方法需要绑定对应的实例,可通过实例调用,或者函数中传入实例
a.foo(123)  # 123
# A.foo(123)  # TypeError: foo() missing 1 required positional argument: 'x'
A.foo(a, 456)  # 456
A.foo(A, 789)  # 789
# 类方法是绑定到类的
A.class_foo(123)  # 123
a.class_foo(456)  # 456
# 静态方法就和普通方法一样,只不过是放在类中,方便使用
A.static_foo(456)  # 123
a.static_foo(456)  # 456
# 可以给类动态添加属性,但是无法对实例添加slots之外属性,会报错
A.pk = 10
print(A.pk)  # 10
# a.bk = 10  # AttributeError: 'A' object has no attribute 'bk'