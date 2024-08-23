from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Login(models.Model):
    emailaddress = models.EmailField(max_length=90)
    password = models.CharField(max_length=90)



class Register(models.Model):
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    username = models.CharField(max_length=90)
    password = models.CharField(max_length=20)
    confirm_password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    



class Customer(models.Model):
    

    COUNTRY_CHOICES = [
        ('AF', 'Afghanistan'),
        ('AL', 'Albania'),
        ('DZ', 'Algeria'),
        ('AS', 'American Samoa'),
        ('AD', 'Andorra'),
        ('AO', 'Angola'),
        ('AI', 'Anguilla'),
        ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'),
        ('AR', 'Argentina'),
        ('AM', 'Armenia'),
        ('AW', 'Aruba'),
        ('AU', 'Australia'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BS', 'Bahamas'),
        ('BH', 'Bahrain'),
        ('BD', 'Bangladesh'),
        ('BB', 'Barbados'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'),
        ('BZ', 'Belize'),
        ('BJ', 'Benin'),
        ('BM', 'Bermuda'),
        ('BT', 'Bhutan'),
        ('BO', 'Bolivia'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BW', 'Botswana'),
        ('BR', 'Brazil'),
        ('IO', 'British Indian Ocean Territory'),
        ('BN', 'Brunei Darussalam'),
        ('BG', 'Bulgaria'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('KH', 'Cambodia'),
        ('CM', 'Cameroon'),
        ('CA', 'Canada'),
        ('CV', 'Cape Verde'),
        ('KY', 'Cayman Islands'),
        ('CF', 'Central African Republic'),
        ('TD', 'Chad'),
        ('CL', 'Chile'),
        ('CN', 'China'),
        ('CX', 'Christmas Island'),
        ('CC', 'Cocos (Keeling) Islands'),
        ('CO', 'Colombia'),
        ('KM', 'Comoros'),
        ('CG', 'Congo'),
        ('CD', 'Congo, The Democratic Republic of The'),
        ('CK', 'Cook Islands'),
        ('CR', 'Costa Rica'),
        ('CI', 'Cote D\'ivoire'),
        ('HR', 'Croatia'),
        ('CU', 'Cuba'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czech Republic'),
        ('DK', 'Denmark'),
        ('DJ', 'Djibouti'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic'),
        ('EC', 'Ecuador'),
        ('EG', 'Egypt'),
        ('SV', 'El Salvador'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('EE', 'Estonia'),
        ('ET', 'Ethiopia'),
        ('FK', 'Falkland Islands (Malvinas)'),
        ('FO', 'Faroe Islands'),
        ('FJ', 'Fiji'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('GF', 'French Guiana'),
        ('PF', 'French Polynesia'),
        ('TF', 'French Southern Territories'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia'),
        ('GE', 'Georgia'),
        ('DE', 'Germany'),
        ('GH', 'Ghana'),
        ('GI', 'Gibraltar'),
        ('GR', 'Greece'),
        ('GL', 'Greenland'),
        ('GD', 'Grenada'),
        ('GP', 'Guadeloupe'),
        ('GU', 'Guam'),
        ('GT', 'Guatemala'),
        ('GG', 'Guernsey'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea-bissau'),
        ('GY', 'Guyana'),
        ('HT', 'Haiti'),
        ('HM', 'Heard Island and Mcdonald Islands'),
        ('VA', 'Holy See (Vatican City State)'),
        ('HN', 'Honduras'),
        ('HK', 'Hong Kong'),
        ('HU', 'Hungary'),
        ('IS', 'Iceland'),
        ('IN', 'India'),
        ('ID', 'Indonesia'),
        ('IR', 'Iran, Islamic Republic of'),
        ('IQ', 'Iraq'),
        ('IE', 'Ireland'),
        ('IM', 'Isle of Man'),
        ('IL', 'Israel'),
        ('IT', 'Italy'),
        ('JM', 'Jamaica'),
        ('JP', 'Japan'),
        ('JE', 'Jersey'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KI', 'Kiribati'),
        ('KP', 'Korea, Democratic People\'s Republic of'),
        ('KR', 'Korea, Republic of'),
        ('KW', 'Kuwait'),
        ('KG', 'Kyrgyzstan'),
        ('LA', 'Lao People\'s Democratic Republic'),
        ('LV', 'Latvia'),
        ('LB', 'Lebanon'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libyan Arab Jamahiriya'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MO', 'Macao'),
        ('MK', 'Macedonia, The Former Yugoslav Republic of'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('MY', 'Malaysia'),
        ('MV', 'Maldives'),
        ('ML', 'Mali'),
        ('MT', 'Malta'),
        ('MH', 'Marshall Islands'),
        ('MQ', 'Martinique'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('YT', 'Mayotte'),
        ('MX', 'Mexico'),
        ('FM', 'Micronesia, Federated States of'),
        ('MD', 'Moldova, Republic of'),
        ('MC', 'Monaco'),
        ('MN', 'Mongolia'),
        ('ME', 'Montenegro'),
        ('MS', 'Montserrat'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('MM', 'Myanmar'),
        ('NA', 'Namibia'),
        ('NR', 'Nauru'),
        ('NP', 'Nepal'),
        ('NL', 'Netherlands'),
        ('AN', 'Netherlands Antilles'),
        ('NC', 'New Caledonia'),
        ('NZ', 'New Zealand'),
        ('NI', 'Nicaragua'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('NU', 'Niue'),
        ('NF', 'Norfolk Island'),
        ('MP', 'Northern Mariana Islands'),
        ('NO', 'Norway'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PW', 'Palau'),
        ('PS', 'Palestinian Territory, Occupied'),
        ('PA', 'Panama'),
        ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'),
        ('PE', 'Peru'),
        ('PH', 'Philippines'),
        ('PN', 'Pitcairn'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('PR', 'Puerto Rico'),
        ('QA', 'Qatar'),
        ('RE', 'Reunion'),
        ('RO', 'Romania'),
        ('RU', 'Russian Federation'),
        ('RW', 'Rwanda'),
        ('SH', 'Saint Helena'),
        ('KN', 'Saint Kitts and Nevis'),
        ('LC', 'Saint Lucia'),
        ('PM', 'Saint Pierre and Miquelon'),
        ('VC', 'Saint Vincent and The Grenadines'),
        ('WS', 'Samoa'),
        ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'),
        ('SA', 'Saudi Arabia'),
        ('SN', 'Senegal'),
        ('RS', 'Serbia'),
        ('SC', 'Seychelles'),
        ('SL', 'Sierra Leone'),
        ('SG', 'Singapore'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('SB', 'Solomon Islands'),
        ('SO', 'Somalia'),
        ('ZA', 'South Africa'),
        ('GS', 'South Georgia and The South Sandwich Islands'),
        ('ES', 'Spain'),
        ('LK', 'Sri Lanka'),
        ('SD', 'Sudan'),
        ('SR', 'Suriname'),
        ('SJ', 'Svalbard and Jan Mayen'),
        ('SZ', 'Swaziland'),
        ('SE', 'Sweden'),
        ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'),
        ('TW', 'Taiwan, Province of China'),
        ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania, United Republic of'),
        ('TH', 'Thailand'),
        ('TL', 'Timor-leste'),
        ('TG', 'Togo'),
        ('TK', 'Tokelau'),
        ('TO', 'Tonga'),
        ('TT', 'Trinidad and Tobago'),
        ('TN', 'Tunisia'),
        ('TR', 'Turkey'),
    ]
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profile_pic = models.ImageField(null=True,default='team-2.jpg', blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, null=True)
    address = models.TextField( null=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default=1, null=True)
    about = models.TextField( null=True, blank=True)
    job = models.CharField(max_length=700, null=True)
    company = models.CharField(max_length=800, null=True)
    phone = models.CharField(max_length=40, null=True)
    email = models.EmailField(max_length=90, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return str(self.user.username) if self.user else "No user" 
    

class EmailAlertPreferences(models.Model):
    
    email_change = models.BooleanField(default=False)
    password_change = models.BooleanField(default=False)
    weekly_newsletter = models.BooleanField(default=False)
    product_promotions = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.username}'s Email Preferences"
    


    
class Tag(models.Model):
    name = models.CharField(max_length=400, null=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Northern Travels', 'Northern Travels'),
        ('Southern Travels', 'Southern Travels'),
        ('Western Travels', 'Western Travels'),
        ('Eastern Travels', 'Easthern Travels'),
    )
    name = models.CharField(max_length=400, null=True)
    product_image = models.ImageField(null=True, blank=True, default='img-1')
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=400, null=True, choices=CATEGORY)
    description = models.TextField( null=True, blank=True)
    days = models.CharField(max_length=400, null=True, blank=True)
    passenger = models.CharField(max_length=400, null=True, blank=True)
    location = models.CharField(max_length=400, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    availability_date = models.DateField(null = True)
    stars = models.IntegerField( default=1)
    remaining_seats = models.IntegerField(default=10)
    
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.name} ({'Available' if self.remaining_seats > 0 else 'Unavailable'})"
    
    def get_discounted_price(self):
    # Ensure that discount and price have default values
     discount = self.discount or 0
     price = self.price or 0
    
    # If discount is greater than 0, apply it
     if discount > 0:
         return price - (price * (discount / 100))
    # If no discount, return the original price
     return price
    
    def is_sold_out(self):
        return self.remaining_seats <= 0
    
    def reduce_seats(self, booked_seats):
        if self.remaining_seats >= booked_seats:
            self.remaining_seats -= booked_seats
            self.save()
        if self.remaining_seats == 0:
            self.availability_date = None  # Mark as unavailable
            self.save()

class Order(models.Model):
    STATUS = [
        ('pending', 'pending'),
        ('Completed', 'Completed'),
        ('Satisfied', 'Satisfied')
    ]
    TRAVEL_CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First Class', 'First Class'),
    ]

    ACCOMMODATION_CHOICES = [
        ('None', 'None'),
        ('Hotel', 'Hotel'),
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
    ]
    
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    amount_of_ticket = models.PositiveIntegerField(default=1)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=20)
    destination = models.CharField(max_length=200)
    departure_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, auto_now_add=True)
    adults = models.BooleanField(default=False, null=True)
    children = models.BooleanField(default=False, null=True)
    infants = models.BooleanField(default=False, null=True)
    travel_class = models.CharField(max_length=20, choices=TRAVEL_CLASS_CHOICES)
    accommodation = models.CharField(max_length=20, choices=ACCOMMODATION_CHOICES, default=1)
    special_requirements = models.TextField(null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    extra_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # New field

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.destination} - {self.product.name} - {self.id} by {self.product}"

    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


class Flight(models.Model):
    CATEGORY = (
        ('Northern Travels', 'Northern Travels'),
        ('Southern Travels', 'Southern Travels'),
        ('Western Travels', 'Western Travels'),
        ('Eastern Travels', 'Eastern Travels'),
    )
    AIRLINES = (
        ('Air Peace', 'Air Peace'),
        ('Arik Air', 'Arik Air'),
        ('Azman Air', 'Azman Air'),
        ('Med-View Airline', 'Med-View Airline'),
        ('Aero Contractors', 'Aero Contractors'),
        ('United Nigeria Airlines', 'United Nigeria Airlines'),
        ('Green Africa Airways', 'Green Africa Airways'),
        ('Ibom Air', 'Ibom Air'),
        ('Max Air', 'Max Air'),
        ('Overland Airways', 'Overland Airways')
    )
    
    from_location = models.CharField(max_length=400, null=True)
    to_location = models.CharField(max_length=400, null=True)
    product_image = models.ImageField(null=True, blank=True, default='default.jpg')
    price = models.FloatField(null=True)
    discount = models.FloatField(null=True, blank=True)
    category = models.CharField(max_length=400, null=True, choices=CATEGORY)
    airline = models.CharField(max_length=400, null=True, choices=AIRLINES)
    estimated_time = models.CharField(max_length=400, null=True)
    departure_time = models.DateTimeField(null=True)
    availability_date = models.DateField(null=True)
    flight_number = models.CharField(max_length=20, unique=True, null=True)  # New unique identifier field

    def __str__(self):
        return f"{self.airline} flight from {self.from_location} to {self.to_location}"

    def get_discounted_price(self):
        discount = self.discount or 0
        price = self.price or 0

        if discount > 0:
            return price - (price * (discount / 100))
        
        return price

    def is_available(self):
        # Checks if the flight is still available based on the availability date
        return self.availability_date and self.availability_date >= timezone.now().date()
    

class FlightBooking(models.Model):
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    travel_class = models.CharField(max_length=50, choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First Class', 'First Class')])
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    num_infants = models.PositiveIntegerField(default=0)
    preferred_airline = models.CharField(max_length=100, choices=Flight.AIRLINES)
    seat_preference = models.CharField(max_length=10, choices=[('Aisle', 'Aisle'), ('Window', 'Window'), ('Middle', 'Middle')], null=True, blank=True)
    meal_preference = models.CharField(max_length=50, choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Vegan', 'Vegan')], null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('PayPal', 'PayPal')])
    card_number = models.CharField(max_length=20)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    billing_address = models.TextField()
    extra_baggage = models.BooleanField(default=False)
    travel_insurance = models.BooleanField(default=False)
    airport_transfers = models.BooleanField(default=False)
    special_assistance = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.full_name} for flight on {self.departure_date}"
    
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
    
class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user} likes {self.post}'
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.message}"


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question



from django.core.validators import RegexValidator

class RecoveryKeyRequest(models.Model):
    username = models.CharField(max_length=150, unique=True)
    social_media_account = models.CharField(max_length=200)
    last_used_password = models.CharField(max_length=128, blank=True, null=True)
    id_card_upload = models.ImageField(upload_to='id_cards/')
    contact_method = models.CharField(
        max_length=100,
        # validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")],
        help_text="Enter a valid email or phone number."
    )

    def __str__(self):
        return f"Recovery Key Request by {self.username}"
    



class DigitalKey(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='digital_keys/')
    description = models.TextField()

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    PAYMENT_CHOICES = [
        ('bank_card', 'Bank Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
        ('gift_card', 'Gift Card'),
        ('mobile_app', 'Mobile App Transfer'),
    ]
    
    name = models.CharField(max_length=50, choices=PAYMENT_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_name_display()
    

class GiftCardPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    receipt_image = models.ImageField(upload_to='receipts/', blank=True)
    card_front_image = models.ImageField(upload_to='card_fronts/', blank=True)
    card_back_image = models.ImageField(upload_to='card_backs/', blank=True)
    card_type = models.CharField(max_length=50)
    card_code = models.CharField(max_length=100)

class CryptoWallet(models.Model):
    CRYPTO_CHOICES = [
        ('bitcoin', 'Bitcoin'),
        ('usdt', 'USDT'),
        ('ethereum', 'Ethereum'),
    ]

    NETWORK_CHOICES = [
        ('bitcoin', 'Bitcoin Network'),
        ('erc20', 'ERC-20 (Ethereum Network)'),
        ('trc20', 'TRC-20 (Tron Network)'),
        # Add more network types as needed
    ]

    currency = models.CharField(max_length=20, choices=CRYPTO_CHOICES, unique=True)
    address = models.CharField(max_length=255, unique=True)
    network_type = models.CharField(max_length=20, choices=NETWORK_CHOICES, null=True)
    network_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.56)

    def __str__(self):
        return f"{self.get_currency_display()} - {self.address} ({self.get_network_type_display()})"



class PaymentMethodRedirect(models.Model):
    method_name = models.CharField(max_length=50)
    redirect_url = models.URLField(max_length=200)

class ProfileApp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profiles/')
    likes = models.PositiveIntegerField(default=0)
    completed_transactions = models.PositiveIntegerField(default=0)
    transaction_time_frame = models.CharField(max_length=100)
    active_status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

class SocialApp(models.Model):
    profile = models.ForeignKey(ProfileApp, on_delete=models.CASCADE, related_name='social_apps')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='social_apps/')
    link = models.URLField()

    def __str__(self):
        return f"{self.name} - {self.profile.user.username}"
    
class CryptoTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    currency = models.CharField(max_length=10)  # e.g., BTC, ETH, USDT
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    status = models.CharField(max_length=20)  # e.g., pending, completed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_id} - {self.status}"
    

from django.utils import timezone

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    created_at = models.DateTimeField(auto_now_add=True)

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    last_profit_update = models.DateTimeField(auto_now=True)

class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='holdings', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=8)

    def __str__(self):
        return f'{self.symbol}: {self.amount}'