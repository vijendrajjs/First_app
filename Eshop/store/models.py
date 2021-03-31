from django.db import models
import datetime


# Create your models here
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=50, default='', null=True, blank=True)
    image = models.ImageField(upload_to='uploads/products/')


    def __str__(self):
        return self.name
    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in = ids)

    @staticmethod
    def get_products_by_quary(quary):

        return Product.objects.filter(name = quary)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class customer(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=15)


    def __str__(self):
        return self.first_name

    @staticmethod
    def get_customer_by_email(email):
        try:
            return customer.objects.get(email=email)
        except:
            return False



class Order(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50,default='')
    phone = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __int__(self):
        return self.id


    def place_order(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
       return Order.objects.filter(customer = customer_id).order_by('-date')


class OrderNumber(models.Model):
    order = models.ManyToManyField(Order)
    
    amount = models.IntegerField()
