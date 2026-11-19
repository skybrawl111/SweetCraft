from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import datetime
import random

from bakery.models import (
    CustomUser, Category, CrustType, Filling, Decoration,
    BaseCake, ConfectionerShift, Order, OrderItem, OrderItemDecoration, Review
)

class Command(BaseCommand):
    help = 'Заполняет базу данных реалистичными демонстрационными данными для Занятия 5'

    def handle(self, *args, **options):
        import sys
        if sys.stdout.encoding.lower() != 'utf-8':
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except Exception:
                pass
        self.stdout.write("Starting demo data generation for Day 5...")

        # 1. Создание 10 категорий десертов
        categories_data = [
            ('Классические торты', 'classic-cakes', 'Традиционные проверенные временем торты для семейных торжеств'),
            ('Муссовые торты', 'mousse-cakes', 'Европейские легкие десерты с зеркальной глазурью и велюром'),
            ('Бенто-торты', 'bento-cakes', 'Мини-торты на 1-2 персоны в экологичных ланч-боксах'),
            ('Свадебные ярусные торты', 'wedding-cakes', 'Многоярусные торжественные композиции со скрытым каркасом'),
            ('Детские праздничные торты', 'kids-cakes', 'Яркие торты с безопасными красителями и сахарными фигурками'),
            ('Капкейки и маффины', 'cupcakes', 'Порционные бисквитные пирожные с кремовыми шапочками'),
            ('Макаронс и пирожные', 'macarons', 'Французские миндальные пирожные с ганашем'),
            ('Тарты и тарталетки', 'tarts', 'Песочные корзинки со свежими ягодами и заварным кремом'),
            ('ПП и веган десерты', 'diet-vegan', 'Низкокалорийные десерты без сахара, глютена и лактозы'),
            ('Чизкейки', 'cheesecakes', 'Нежные чизкейки горячего и холодного приготовления на крем-чизе'),
        ]
        cat_objs = []
        for name, slug, desc in categories_data:
            cat, _ = Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': desc, 'is_active': True}
            )
            cat_objs.append(cat)
        self.stdout.write(f"Categories created: {len(cat_objs)}")

        # 2. Создание пользователей с ролями
        admin, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Чошгун',
                'last_name': 'Адилов',
                'email': 'admin@sweetcraft.local',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '+7 (999) 111-22-33'
            }
        )
        admin.first_name = 'Чошгун'
        admin.last_name = 'Адилов'
        admin.set_password('admin123')
        admin.save()

        manager, _ = CustomUser.objects.get_or_create(
            username='manager',
            defaults={
                'first_name': 'Елена',
                'last_name': 'Менеджерова',
                'email': 'manager@sweetcraft.local',
                'role': 'manager',
                'is_staff': True,
                'phone': '+7 (999) 222-33-44'
            }
        )
        manager.set_password('manager123')
        manager.save()

        baker, _ = CustomUser.objects.get_or_create(
            username='baker',
            defaults={
                'first_name': 'Михаил',
                'last_name': 'Шеф-Кондитер',
                'email': 'baker@sweetcraft.local',
                'role': 'confectioner',
                'is_staff': True,
                'phone': '+7 (999) 333-44-55'
            }
        )
        baker.set_password('baker123')
        baker.save()

        customers = []
        customer_data = [
            ('anna', 'Анна', 'Смирнова', 'anna@mail.local', '+7 (903) 123-45-67'),
            ('dmitry', 'Дмитрий', 'Иванов', 'dmitry@mail.local', '+7 (916) 234-56-78'),
            ('olga', 'Ольга', 'Кузнецова', 'olga@mail.local', '+7 (925) 345-67-89'),
            ('sergey', 'Сергей', 'Попов', 'sergey@mail.local', '+7 (977) 456-78-90'),
            ('marina', 'Марина', 'Васильева', 'marina@mail.local', '+7 (985) 567-89-01'),
            ('artem', 'Артем', 'Новиков', 'artem@mail.local', '+7 (915) 678-90-12'),
            ('svetlana', 'Светлана', 'Морозова', 'sveta@mail.local', '+7 (926) 789-01-23'),
            ('igor', 'Игорь', 'Федоров', 'igor@mail.local', '+7 (909) 890-12-34'),
            ('tatiana', 'Татьяна', 'Павлова', 'tanya@mail.local', '+7 (968) 901-23-45'),
            ('viktor', 'Виктор', 'Семенов', 'viktor@mail.local', '+7 (999) 012-34-56'),
        ]
        for u, f, l, e, p in customer_data:
            cust, _ = CustomUser.objects.get_or_create(
                username=u,
                defaults={'first_name': f, 'last_name': l, 'email': e, 'role': 'customer', 'phone': p}
            )
            cust.set_password('client123')
            cust.save()
            customers.append(cust)
        self.stdout.write(f"Users created: admin, manager, baker, {len(customers)} customers.")

        # 3. Создание 10 видов коржей
        crusts_data = [
            ('Классический шифоновый ванильный', Decimal('400.00'), 'Воздушный и нежный бисквит с натуральной мадагаскарской ванилью'),
            ('Насыщенный шоколадный брауни', Decimal('550.00'), 'Плотный, влажный шоколадный бисквит на основе бельгийского тёмного какао'),
            ('Красный бархат (Red Velvet)', Decimal('500.00'), 'Легендарный сочный бархатный бисквит с тонким шоколадным послевкусием'),
            ('Морковно-пряный с корицей', Decimal('450.00'), 'Ароматный бисквит с добавлением свежей моркови, корицы и мускатного ореха'),
            ('Фисташковый деликатный', Decimal('650.00'), 'Изысканный бисквит с добавлением 100% натуральной фисташковой пасты'),
            ('Медовые коржи традиционные', Decimal('400.00'), 'Тонкие золотистые коржи на алтайском липовом мёде со сливочной пропиткой'),
            ('Слоёные хрустящие коржи (Наполеон)', Decimal('450.00'), 'Многослойные тончайшие рубленые коржи на сливочном масле 82.5%'),
            ('Миндальный дакуаз (без глютена)', Decimal('700.00'), 'Хрустящий снаружи и мягкий внутри меренговый корж на миндальной муке'),
            ('Кокосовый нежный бисквит', Decimal('480.00'), 'Влажный бисквит на кокосовом молоке с добавлением белой стружки'),
            ('Лавандовый бисквит с черникой', Decimal('520.00'), 'Оригинальный бисквит с экстрактом горной лаванды и ягодами черники'),
        ]
        crust_objs = []
        for name, cost, desc in crusts_data:
            c, _ = CrustType.objects.get_or_create(name=name, defaults={'extra_cost': cost, 'description': desc})
            crust_objs.append(c)

        # 4. Создание 10 видов начинок
        fillings_data = [
            ('Малина - мята (ягодное компоте)', 'Свежее малиновое конфи с листочками перечной мяты', Decimal('1200.00')),
            ('Сливочный маскарпоне с садовой клубникой', 'Нежнейший крем на основе итальянского сыра маскарпоне', Decimal('1350.00')),
            ('Солёная карамель с жареным арахисом', 'Домашняя тягучая карамель с щепоткой морской соли', Decimal('1100.00')),
            ('Манго - маракуйя (тропический мусс)', 'Яркий экзотический вкус спелого тайского манго и кислинка маракуйи', Decimal('1400.00')),
            ('Тёмный бельгийский шоколад с пьяной вишней', 'Плотный шоколадный ганаш с вишней, вымоченной в ликёре', Decimal('1300.00')),
            ('Черничный чизкейк', 'Сливочно-сырный крем с прослойкой из протёртой черники', Decimal('1250.00')),
            ('Фисташковый ганаш с малиной', 'Премиальный крем с фисташковой пастой и цельными ягодами малины', Decimal('1600.00')),
            ('Лимонный курд с нежной меренгой', 'Освежающий цитрусовый заварной крем с ярким лимонным соком', Decimal('1150.00')),
            ('Крем-чиз на белом шоколаде', 'Классический устойчивый крем с натуральными сливками и белым шоколадом', Decimal('1200.00')),
            ('Карамелизованная груша с сыром Дорблю', 'Гастрономическое сочетание пряной томлёной груши и благородного сыра', Decimal('1500.00')),
        ]
        filling_objs = []
        for name, desc, price in fillings_data:
            f, _ = Filling.objects.get_or_create(name=name, defaults={'description': desc, 'price_per_kg': price})
            filling_objs.append(f)

        # 5. Создание 10 элементов декора
        decor_data = [
            ('Венок из свежих ягод (клубника, голубика, малина)', Decimal('800.00'), 'Горка свежих отборных ягод с веточками розмарина'),
            ('Шоколадный велюр (напыление какао-масла)', Decimal('700.00'), 'Бархатистое матовое покрытие любого цвета на выбор'),
            ('Сахарная фотопечать съедобными чернилами', Decimal('500.00'), 'Печать любого изображения, фотографии или логотипа на вафельной бумаге'),
            ('Фигурки из мастики ручной лепки (до 3 шт.)', Decimal('1200.00'), 'Индивидуальные персонажи и композиции ручной работы мастера'),
            ('Шоколадные сферы и трюфели ручной работы', Decimal('650.00'), 'Шары из бельгийского шоколада с золотым напылением'),
            ('Леденцы из изомальта и безе на палочках', Decimal('450.00'), 'Прозрачные кристаллы и воздушные меренги для детского торта'),
            ('Макаронс французские ассорти (5 шт.)', Decimal('600.00'), 'Миндальные пирожные с нежными начинками на выбор'),
            ('Съедобное сусальное золото и кандурин', Decimal('550.00'), 'Изящные золотые брызги и сияние для юбилейного торта'),
            ('Зеркальная глянцевая глазурь', Decimal('500.00'), 'Идеально ровный зеркальный блеск поверхности торта'),
            ('Живые обработанные съедобные цветы', Decimal('750.00'), 'Бутоны роз, эустом и кустовых хризантем со специальной изоляцией стеблей'),
        ]
        decor_objs = []
        for name, cost, desc in decor_data:
            d, _ = Decoration.objects.get_or_create(name=name, defaults={'cost': cost, 'description': desc})
            decor_objs.append(d)

        self.stdout.write(f"Catalogs created: {len(crust_objs)} crusts, {len(filling_objs)} fillings, {len(decor_objs)} decors.")

        # 6. Создание 32 базовых десертов в каталоге (>= 30 записей)
        cakes_data = [
            # Классические торты (cat 0)
            ('Красный бархат классический', 'krasnyj-barhat', 'Знаменитый торт с сочными красными коржами и сливочным крем-чизом.', Decimal('2800.00'), Decimal('2.0'), crust_objs[2], cat_objs[0]),
            ('Шоколадный трюфель Премиум', 'shokoladnyj-tryufel', 'Глубокий шоколадный вкус для истинных ценителей бельгийского шоколада.', Decimal('3200.00'), Decimal('2.0'), crust_objs[1], cat_objs[0]),
            ('Морковный с пряной карамелью', 'morkovnyj-karamel', 'Домашний уютный вкус с нотками корицы, грецкого ореха и карамели.', Decimal('2500.00'), Decimal('2.0'), crust_objs[3], cat_objs[0]),
            ('Медовик Деревенский', 'medovik-derevenskij', 'Традиционный многослойный медовик с нежным заварным кремом.', Decimal('2400.00'), Decimal('2.2'), crust_objs[5], cat_objs[0]),
            ('Наполеон Хрустящий', 'napoleon-hrustyashchij', 'Тысяча тончайших слоёв рублёного теста и классический пломбирный крем.', Decimal('2600.00'), Decimal('2.2'), crust_objs[6], cat_objs[0]),
            
            # Муссовые торты (cat 1)
            ('Фисташка - Малина Мусс', 'fistashka-malina-mousse', 'Элитный десерт с натуральной фисташкой и яркой малиновой кислинкой.', Decimal('3600.00'), Decimal('1.8'), crust_objs[4], cat_objs[1]),
            ('Тропический Манго-Маракуйя', 'tropicheskij-mango', 'Лёгкий летний торт с освежающим фруктовым муссом и ванильным бисквитом.', Decimal('3100.00'), Decimal('1.8'), crust_objs[0], cat_objs[1]),
            ('Три шоколада Премиум', 'tri-shokolada', 'Градация нежных муссов из белого, молочного и темного шоколада.', Decimal('3400.00'), Decimal('1.9'), crust_objs[1], cat_objs[1]),
            ('Лавандовый Сон Мусс', 'lavandovyj-son', 'Изысканный десерт с ароматом прованской лаванды и черничным кули.', Decimal('3300.00'), Decimal('1.8'), crust_objs[9], cat_objs[1]),
            
            # Бенто-торты (cat 2)
            ('Бенто Шоколадный экспресс', 'bento-shokoladnyj', 'Мини-торт на 400 грамм с надписью и свечкой в наборе.', Decimal('1200.00'), Decimal('0.5'), crust_objs[1], cat_objs[2]),
            ('Бенто Ягодный пломбир', 'bento-yagodnyj', 'Воздушный ванильный бисквит с клубничным кули и крем-чизом.', Decimal('1200.00'), Decimal('0.5'), crust_objs[0], cat_objs[2]),
            ('Бенто Карамельный арахис', 'bento-karamel-arahis', 'Сникерс-стиль с домашней соленой карамелью и арахисом.', Decimal('1250.00'), Decimal('0.5'), crust_objs[1], cat_objs[2]),
            ('Бенто Красный бархат Мини', 'bento-red-velvet', 'Порционный красный бархат с сердечком и пожеланием.', Decimal('1250.00'), Decimal('0.5'), crust_objs[2], cat_objs[2]),
            
            # Свадебные ярусные торты (cat 3)
            ('Свадебная Симфония (3 яруса)', 'svadebnaya-simfoniya-3tier', 'Грандиозный трехъярусный торт со скрытым каркасом и белым велюром.', Decimal('12500.00'), Decimal('6.5'), crust_objs[0], cat_objs[3]),
            ('Элегия Любви (2 яруса)', 'elegiya-lyubvi-2tier', 'Двухъярусный торт в пастельных тонах с живыми цветами.', Decimal('8500.00'), Decimal('4.2'), crust_objs[2], cat_objs[3]),
            ('Золотой Век Свадебный', 'zolotoj-vek-wedding', 'Роскошное оформление сусальным золотом и жемчужным кандурином.', Decimal('14000.00'), Decimal('7.0'), crust_objs[4], cat_objs[3]),
            
            # Детские торты (cat 4)
            ('Космическое Путешествие', 'kosmicheskoe-puteshestvie', 'Торт с леденцами из изомальта и сахарной ракетой.', Decimal('3700.00'), Decimal('2.5'), crust_objs[1], cat_objs[4]),
            ('Сказочный Единорог', 'skazochnyj-edinorog', 'Нежный розово-голубой торт с рогом из бельгийского шоколада.', Decimal('3900.00'), Decimal('2.5'), crust_objs[0], cat_objs[4]),
            ('Сафари в Джунглях', 'safari-dzhungli', 'Фигурки милых зверят ручной лепки из сахарной мастики.', Decimal('4200.00'), Decimal('2.8'), crust_objs[3], cat_objs[4]),
            
            # Капкейки (cat 5)
            ('Набор капкейков Ягодный микс (6 шт)', 'cupcakes-berry-mix-6', 'Ассорти ванильных и шоколадных капкейков со свежими ягодами.', Decimal('1500.00'), Decimal('0.6'), crust_objs[0], cat_objs[5]),
            ('Набор капкейков Шоколадный вулкан (12 шт)', 'cupcakes-choc-vulcan-12', 'Шоколадные кексы с жидким центром и шапочкой ганаша.', Decimal('2800.00'), Decimal('1.2'), crust_objs[1], cat_objs[5]),
            ('Набор капкейков Красный бархат (6 шт)', 'cupcakes-red-velvet-6', 'Сочные кексы с малиновой начинкой и крем-чизом.', Decimal('1600.00'), Decimal('0.6'), crust_objs[2], cat_objs[5]),

            # Макаронс (cat 6)
            ('Коробка макаронс Гранд Ассорти (16 шт)', 'macarons-grand-16', '16 французских пирожных с 8 разными вкусами.', Decimal('2400.00'), Decimal('0.4'), crust_objs[7], cat_objs[6]),
            ('Набор макаронс Фисташка-Малина (8 шт)', 'macarons-pistachio-8', 'Нежные миндальные половинки с фисташковым ганашем.', Decimal('1300.00'), Decimal('0.2'), crust_objs[7], cat_objs[6]),
            
            # Тарты (cat 7)
            ('Тарт с лесной земляникой и кремом дипломат', 'tart-strawberry-diplomat', 'Хрустящее песочное сабле со свежими ягодами.', Decimal('2200.00'), Decimal('1.2'), crust_objs[0], cat_objs[7]),
            ('Лимонный Тарто-торт с меренгой', 'limonnyj-tart', 'Яркий десерт с лимонным курдом и обожжённой меренгой.', Decimal('2700.00'), Decimal('1.8'), crust_objs[0], cat_objs[7]),
            
            # ПП и веган (cat 8)
            ('Миндальный Дакуаз с ягодами (Без глютена)', 'mindalnyj-dakuaz', 'Безглютеновый воздушный торт на миндальной муке с клубникой.', Decimal('3800.00'), Decimal('1.8'), crust_objs[7], cat_objs[8]),
            ('Авокадо-Лайм Raw Cake (Веган)', 'avocado-lime-raw', 'Сыроедческий торт на основе кешью-крема, авокадо и кокосового масла.', Decimal('3900.00'), Decimal('1.6'), crust_objs[8], cat_objs[8]),
            ('Кокосовый Рай без сахара', 'kokosovyj-raj-sugarfree', 'Десерт на стевии и кокосовых сливках с чиа-джемом.', Decimal('3500.00'), Decimal('1.7'), crust_objs[8], cat_objs[8]),
            
            # Чизкейки (cat 9)
            ('Чизкейк Нью-Йорк Классический', 'cheesecake-new-york', 'Плотный запеченный чизкейк из сыра филадельфия на песочной основе.', Decimal('2600.00'), Decimal('1.8'), crust_objs[0], cat_objs[9]),
            ('Черничный Чизкейк Торт', 'chernichnyj-chizkejk', 'Сочетание запечённого чизкейка и ароматной лесной черники.', Decimal('2900.00'), Decimal('2.0'), crust_objs[0], cat_objs[9]),
            ('Карамельный чизкейк с пеканом', 'cheesecake-caramel-pecan', 'Сливочно-сырный торт с карамельной глазурью и орехами пекан.', Decimal('3100.00'), Decimal('1.9'), crust_objs[1], cat_objs[9]),
        ]
        base_cakes = []
        for title, slug, desc, price, weight, cr, cat in cakes_data:
            bc, _ = BaseCake.objects.get_or_create(
                slug=slug,
                defaults={
                    'title': title,
                    'description': desc,
                    'base_price': price,
                    'default_weight': weight,
                    'crust_type': cr,
                    'category': cat,
                    'is_available': True
                }
            )
            bc.available_fillings.set(random.sample(filling_objs, random.randint(2, 4)))
            base_cakes.append(bc)
        self.stdout.write(f"Catalog created: {len(base_cakes)} base cakes across {len(cat_objs)} categories.")

        # 7. Создание 17 производственных смен (включая лимиты 35 кг будни / 45 кг выходные)
        today = timezone.localdate()
        shift_objs = []
        for offset in range(-3, 14):
            dt = today + datetime.timedelta(days=offset)
            is_weekend = dt.weekday() in (5, 6)
            cap = Decimal('45.00') if is_weekend else Decimal('35.00')
            shift, _ = ConfectionerShift.objects.get_or_create(
                shift_date=dt,
                defaults={
                    'confectioner': baker,
                    'max_capacity_weight': cap,
                    'notes': 'Усиленная выходная смена' if is_weekend else 'Стандартная рабочая смена цеха'
                }
            )
            shift_objs.append(shift)
        self.stdout.write(f"Shifts created: {len(shift_objs)} daily shifts.")

        # 8. Создание 35 заказов покупателей
        statuses = ['NEW', 'ACCEPTED', 'IN_PROGRESS', 'READY', 'COMPLETED']
        order_count = 0
        for i in range(35):
            cust = customers[i % len(customers)]
            shift = random.choice(shift_objs)
            status = 'COMPLETED' if shift.shift_date < today else random.choice(statuses)

            order = Order.objects.create(
                customer=cust,
                delivery_date=shift.shift_date,
                status=status,
                contact_phone=cust.phone or '+7 (999) 000-00-00',
                delivery_address=f"г. Москва, ул. Кондитерская, д. {i+1}, кв. {random.randint(1, 120)}",
                comment=f"Заказ #{i+1} к праздничному событию. Доставить аккуратно."
            )

            # Создание позиции заказа
            bc = random.choice(base_cakes)
            cr = bc.crust_type or random.choice(crust_objs)
            fl = random.choice(filling_objs)
            w = Decimal(str(random.choice([1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0])))
            tiers = 1 if w < Decimal('3.0') else (2 if w < Decimal('5.0') else 3)

            item = OrderItem.objects.create(
                order=order,
                base_cake=bc,
                crust_type=cr,
                filling=fl,
                weight=w,
                tiers=tiers,
                text_on_cake=f"С праздником! #{i+1}" if i % 2 == 0 else ""
            )

            # Добавление элементов декора через явную связующую модель OrderItemDecoration
            selected_decors = random.sample(decor_objs, random.randint(1, 3))
            for dec in selected_decors:
                OrderItemDecoration.objects.create(
                    order_item=item,
                    decoration=dec,
                    quantity=random.randint(1, 2),
                    custom_notes="Разместить по центру изделия"
                )

            # Расчет цены по формуле Варианта 1
            price = item.calculate_price()
            item.item_price = price
            item.save(update_fields=['item_price'])

            order.total_price = price
            order.save(update_fields=['total_price'])
            order_count += 1

        self.stdout.write(f"Orders created: {order_count} orders with order items and decorations.")

        # 9. Создание 15 отзывов на торты
        review_texts = [
            "Торт превзошёл все ожидания! Коржи очень нежные, крем воздушный и в меру сладкий. Все гости были в восторге!",
            "Заказывали на день рождения дочки. Оформление просто ювелирное, ягоды свежайшие, спасибо кондитерам!",
            "Отличная кондитерская! Удобный конструктор на сайте, рассчитали всё сразу без сюрпризов при получении.",
            "Начинка манго-маракуйя — это шедевр! Очень сочно, кислинка идеально балансирует бисквит.",
            "Очень переживали за доставку, но привезли минута в минуту, торт в идеальном состоянии.",
            "Шоколадный трюфель — рай для сладкоежек. Плотный, насыщенный, настоящий бельгийский шоколад.",
            "Заказываем уже третий раз, качество всегда на высоте. Идеальный сервис и пунктуальность.",
            "Вкусный классический торт, чувствуются натуральные ингредиенты, никакого маргарина.",
            "Очень красивый торт с велюром и ягодами. На фотографиях с праздника смотрелся великолепно!",
            "Спасибо за помощь в выборе начинки! Менеджер помог определиться с весом на компанию."
        ]
        rev_count = 0
        for i in range(15):
            bc = random.choice(base_cakes)
            c = random.choice(customers)
            r, created = Review.objects.get_or_create(
                base_cake=bc,
                customer=c,
                defaults={
                    'rating': random.choice([4, 5, 5, 5, 4]),
                    'text': random.choice(review_texts)
                }
            )
            if created:
                rev_count += 1

        self.stdout.write(f"Reviews created: {rev_count}")
        self.stdout.write("SUCCESS: Demo data generation for Day 5 completed successfully!")
