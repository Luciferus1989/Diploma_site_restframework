from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Avg, Sum, ExpressionWrapper, F, DecimalField
from myauth.models import CustomUser


def product_preview_directory_path(instance: "Item", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def item_image_directory_path(instance: 'ItemImage', filename: str) -> str:
    return 'products/product_{pk}/images/{filename}'.format(pk=instance.item.pk, filename=filename,)


def category_preview_directory_path(instance: "Category", filename: str) -> str:
    return "category/category_{pk}/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"#{self.name}"


class Category(models.Model):
    title = models.CharField(max_length=50)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    image = models.ImageField(upload_to=category_preview_directory_path, blank=False)

    def __str__(self):
        return self.title


class Item(models.Model):
    class Meta:
        ordering = ['name', 'price']

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Item price')
    count = models.IntegerField(default=0)
    discount = models.SmallIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    free_delivery = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, blank=True)


    @property
    def description_short(self) -> str:
        if len(self.description) < 50:
            return self.description
        else:
            return self.description[:50] + '...'

    def __str__(self) -> str:
        return self.name

    def get_feedbacks_count(self):
        return self.feedbacks.count()

    def get_average_rating(self):
        return self.feedbacks.aggregate(avg_rating=Avg('rate'))['avg_rating'] or 0.0

    def calculate_overall_rating(self):
        total_feedbacks = self.feedbacks.count()
        total_rating = self.feedbacks.aggregate(sum_rating=Sum('rate'))['sum_rating'] or 0

        if total_feedbacks > 0:
            average_rating = total_rating / total_feedbacks
            return f"{average_rating:.1f} / 5" if average_rating % 1 != 0 else f"{int(average_rating)} / 5"
        else:
            return 0.0

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        item = form.instance
        tags = item.tags.all()
        for tag_name in form.cleaned_data['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if tag not in tags:
                item.tags.add(tag)


class Specification(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}: {self.value}"

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    src = models.ImageField(upload_to=item_image_directory_path)
    description = models.CharField(max_length=100, null=False, blank=True)

    def __str__(self):
        return f"Image for {self.item.name}"


class Order(models.Model):
    status_choice = [
        ('active', 'active'),
        ('pending', 'pending'),
        ('in process', 'in process'),
        ('archived', 'Archived'),
    ]
    customer = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, through='Basket')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=status_choice, default='active')
    payment_type = models.CharField(max_length=20)
    delivery_type = models.CharField(max_length=20,
                                     choices=[("ordinary", "ordinary"), ("express", "express")], default='standard')
    city = models.CharField(max_length=255)
    address = models.TextField()

    def calculate_total_amount(self):
        total_amount = self.items.aggregate(total=Sum(F('price') * F('basket__quantity'), output_field=models.DecimalField()))['total']
        self.total_amount = total_amount
        return total_amount or Decimal('0.00')


class DeliverySettings(models.Model):
    delivery_type = models.CharField(max_length=20,
                                     choices=[("ordinary", "Обычная"), ("express", "Экспресс-доставка")])
    express_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    free_delivery_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    standard_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=200)

    def __str__(self):
        return str(self.delivery_type)


class Basket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class FeedBack(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='feedbacks')
    author = models.CharField(max_length=50)
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=300)
    rate = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"Feedback for {self.item.name} by {self.author}"



