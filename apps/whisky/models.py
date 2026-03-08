from django.db import models


class CaskType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Whisky(models.Model):

    COUNTRY_CHOICES = [
        ("scotland", "Scotland"),
        ("usa", "USA"),
        ("ireland", "Ireland"),
        ("japan", "Japan"),
        ("canada", "Canada"),
        ("taiwan", "Taiwan"),
        ("india", "India"),
        ("other", "Other"),
    ]

    TYPE_CHOICES = [
        ("single_malt", "Single Malt"),
        ("blended", "Blended"),
        ("blended_malt", "Blended Malt"),
        ("single_grain", "Single Grain"),
        ("bourbon", "Bourbon"),
        ("rye", "Rye"),
        ("tennessee", "Tennessee"),
        ("single_pot_still", "Single Pot Still"),
        ("other", "Other"),
    ]

    REGION_CHOICES = [
        ("islay", "Islay"),
        ("speyside", "Speyside"),
        ("highlands", "Highlands"),
        ("lowlands", "Lowlands"),
        ("campbeltown", "Campbeltown"),
        ("islands", "Islands"),
        ("kentucky", "Kentucky"),
        ("tennessee", "Tennessee"),
        ("other", "Other"),
    ]

    PEAT_LEVEL_CHOICES = [
        ("none", "None"),
        ("light", "Light"),
        ("medium", "Medium"),
        ("heavy", "Heavy"),
    ]

    PRICE_TIER_CHOICES = [
    ("budget", "Budget (~₩50,000)"),
    ("mid", "Mid-range (₩50,000~₩100,000)"),
    ("premium", "Premium (₩100,000~₩200,000)"),
    ("luxury", "Luxury (₩200,000~)"),
]

    # 기본 정보
    name = models.CharField(max_length=200)
    distillery = models.CharField(max_length=200)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES)
    whisky_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True)
    age = models.PositiveBigIntegerField(null=True, blank=True)
    abv = models.FloatField()
    cask_types = models.ManyToManyField(CaskType, blank=True)
    peat_level = models.CharField(max_length=10, choices=PEAT_LEVEL_CHOICES, default="none")


    # 도슨트 콘텐츠
    description = models.TextField()
    history = models.TextField(blank=True)
    bartender_tip = models.TextField(blank=True)
    pairing = models.JSONField(default=list, blank=True)
    serving_guide = models.JSONField(default=dict, blank=True)
    flavor_profile = models.JSONField(default=dict, blank=True)
    price_tier = models.CharField(max_length=20, choices=PRICE_TIER_CHOICES, blank=True)

    # 메타
    image = models.ImageField(upload_to='whiskies/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.distillery})"