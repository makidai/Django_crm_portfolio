from django.db import models
from django.contrib.auth.models import User

#顧客情報
class Customer(models.Model):
    user = models.OneToOneField(User, verbose_name='ユーザー', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('名前',max_length=200, null=True)
    phone = models.CharField('携帯番号',max_length=200, null=True)
    email = models.CharField('メールアドレス',max_length=200, null=True)
    profile_pic = models.ImageField('プロフィール写真',default="profile.png", null=True, blank=True)
    date_created = models.DateTimeField('作成日',auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name

#商品タグ
class Tag(models.Model):
    name = models.CharField('タグ名',max_length=200, null=True)

    def __str__(self):
        return self.name

#商品
class Product(models.Model):
    CATEGORY = (
        ('Indoor','インドア'),
        ('Out Door','アウトドア'),
    )
    name = models.CharField('商品名',max_length=200, null=True)
    price = models.DecimalField('価格',max_digits=10,decimal_places=0)
    category = models.CharField('カテゴリー',max_length=200, null=True, choices=CATEGORY)
    description = models.CharField('商品説明',max_length=200, null=True, blank=True)
    date_created = models.DateTimeField('作成日',auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

#注文情報
class Order(models.Model):
    STATUS = (
        ('Pending','保留中'),
        ('Out for delivery','配達中'),
        ('Delivered','配達済み'),
    )
    customer = models.ForeignKey(Customer, verbose_name='顧客', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, verbose_name='商品' ,null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField('注文日',auto_now_add=True, null=True)
    status = models.CharField('配達状況',max_length=200, null=True, choices=STATUS)
    note = models.CharField('メモ',max_length=1000, null=True)

    def __str__(self):
        return self.product.name
