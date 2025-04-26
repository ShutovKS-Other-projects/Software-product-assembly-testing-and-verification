from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import SSD, Cart, CartItem


class Command(BaseCommand):
    help = "Генерирует тестовые группы, пользователей и партии для демонстрации ролей и корзины"

    @transaction.atomic
    def handle(self, *args, **options):
        # Создание групп
        group_names = ["Администратор", "Товаровед", "Менеджер", "Гость"]
        groups = {}
        for name in group_names:
            group, _ = Group.objects.get_or_create(name=name)
            groups[name] = group
        self.stdout.write(self.style.SUCCESS("Группы созданы"))

        # Создание пользователей
        users = {}
        user_specs = [
            ("admin", "1234", "Администратор", True),
            ("manager1", "1234", "Менеджер", False),
            ("manager2", "1234", "Менеджер", False),
            ("clerk", "1234", "Товаровед", False),
            ("guest", "1234", "Гость", False),
        ]
        for username, password, group, is_super in user_specs:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
            user.groups.clear()
            user.groups.add(groups[group])
            user.is_staff = True
            user.is_superuser = is_super
            user.save()
            users[username] = user
        self.stdout.write(self.style.SUCCESS("Пользователи созданы и добавлены в группы"))

        # Создание тестовых партий и позиций для менеджеров
        ssds = list(SSD.objects.all())
        if not ssds:
            self.stdout.write(self.style.WARNING("Нет товаров SSD. Сначала выполните seed_catalog!"))
            return
        for i, manager_name in enumerate(["manager1", "manager2"]):
            manager = users[manager_name]
            cart = Cart.objects.create(owner=manager)
            # Добавим 2 товара в каждую партию
            for ssd in ssds[i * 2:i * 2 + 2]:
                CartItem.objects.create(cart=cart, product=ssd, quantity=5 + i, price_at_add=ssd.price)
        self.stdout.write(self.style.SUCCESS("Тестовые партии и позиции созданы для менеджеров"))

        # Назначение прав группам
        ssd_ct = ContentType.objects.get(app_label="catalog", model="ssd")
        cart_ct = ContentType.objects.get(app_label="catalog", model="cart")
        cartitem_ct = ContentType.objects.get(app_label="catalog", model="cartitem")

        # Права для моделей
        ssd_perms = Permission.objects.filter(content_type=ssd_ct)
        cart_perms = Permission.objects.filter(content_type=cart_ct)
        cartitem_perms = Permission.objects.filter(content_type=cartitem_ct)

        # Администратор: все права
        groups["Администратор"].permissions.set(list(ssd_perms) + list(cart_perms) + list(cartitem_perms))

        # Менеджер: все права на Cart и CartItem, только просмотр SSD
        manager_perms = list(Permission.objects.filter(content_type=ssd_ct, codename__startswith="view_")) + \
                        list(cart_perms) + list(cartitem_perms)
        groups["Менеджер"].permissions.set(manager_perms)

        # Товаровед: все права на SSD
        groups["Товаровед"].permissions.set(list(ssd_perms))

        # Гость: только просмотр SSD
        guest_perms = Permission.objects.filter(content_type=ssd_ct, codename__startswith="view_")
        groups["Гость"].permissions.set(list(guest_perms))

        self.stdout.write(self.style.SUCCESS("Права назначены группам"))

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно сгенерированы!"))
