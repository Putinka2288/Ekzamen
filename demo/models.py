from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.crypto import get_random_string


def get_name_file(instance, filename):
    return '/'.join([get_random_string(length=5) + '_' + filename])


class User(AbstractUser):
    name = models.CharField(max_length=254, verbose_name='Имя', blank=False)
    surname = models.CharField(max_length=254, verbose_name='Фамилия', blank=False)
    patronymic = models.CharField(max_length=254, verbose_name='Отчество', blank=True)
    username = models.CharField(max_length=254, verbose_name='Логин', unique=True, blank=False)
    email = models.CharField(max_length=254, verbose_name='Почта', unique=True, blank=False)
    password = models.CharField(max_length=254, verbose_name='Пароль', blank=False)
    role = models.CharField(max_length=254, verbose_name='Роль', choices=(('admin', 'Админ'),
                                                                          ('user', 'Юзер')), default='user')

    def __str__(self):
        return str(self.name) + " " + str(self.patronymic) + " " + str(self.surname)

    def full_name(self):
        return ' '.join([self.name, self.surname, self.patronymic])


class Product(models.Model):
    name = models.CharField(max_length=254, verbose_name='Продукт', blank=False)
    photo_file = models.ImageField(max_length=254, null=True, blank=True, upload_to=get_name_file,
                                   validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg',
                                                                                          'jpeg', 'webp'])])
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0.00, blank=False)
    count = models.IntegerField(verbose_name='Количество', blank=False)
    country = models.CharField(max_length=254, verbose_name='Страна', blank=False)
    year = models.IntegerField(verbose_name='Год производства', blank=False)
    model = models.CharField(verbose_name='Модель', max_length=254, blank=False)
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=254, verbose_name='Категория', blank=False)


class Order(models.Model):
    STATUS_CHOICES = [('new', 'Новый'), ('confirmed', "Подтверждённый"), ('canceled', 'Отменённый')]
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='ItemInOrder', related_name='orders')
    date = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True)
    rejection_reason = models.TextField(verbose_name='Причина отказа', blank=True)
    status = models.CharField(max_length=254, verbose_name='Статус', choices=STATUS_CHOICES, default='new')

    def status_verbose(self):
        return dict(self.STATUS_CHOICES)[self.status]

    def count_product(self):
        count = 0
        for count_order in self.iteminorder_set.all():
            count += count_order.count
        return count

    def __str__(self):
        return self.date.ctime() + "|" + self.user.full_name() + "|" + str(self.count_product())


class ItemInOrder(models.Model):
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0.00, blank=False)


class Basket(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Количество', blank=False)
