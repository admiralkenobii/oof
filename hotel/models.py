from django.conf import settings
from django.db import models


# номера
class Room(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Доступен"
        OCCUPIED = "occupied", "Занят"

    number = models.CharField(
        max_length=12,
        unique=True,
        verbose_name="Номер комнаты",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    capacity = models.PositiveSmallIntegerField(
        verbose_name="Количество мест",
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость за ночь",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.AVAILABLE,
        verbose_name="Статус",
    )

    def __str__(self):
        return f"Номер {self.number}"


# бронирования
class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Подтверждено"
        CANCELLED = "cancelled", "Отменено"

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="Гость",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        related_name="bookings",
        verbose_name="Номер",
    )
    check_in_date = models.DateField(
        verbose_name="Дата заезда",
    )
    check_out_date = models.DateField(
        verbose_name="Дата выезда",
    )
    guests_count = models.PositiveSmallIntegerField(
        verbose_name="Количество гостей",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.CONFIRMED,
        verbose_name="Статус",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )

    def __str__(self):
        return f"Бронирование №{self.id}: номера {self.room.number}"


# услуги отеля
class HotelService(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название услуги",
    )
    description = models.TextField(
        verbose_name="Описание",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
    )

    def __str__(self):
        return self.name


# заказы услуг
class ServiceOrder(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="service_orders",
        verbose_name="Бронирование",
    )
    service = models.ForeignKey(
        HotelService,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Услуга",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создано",
    )

    def __str__(self):
        return (f"Услуга {self.service.name} для бронирования №{self.booking.id}. "
                f"Дата: {self.created_at}")