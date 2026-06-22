# 2026.3.2 클로드랑 같이 기획중 ^0^

# 1. User
class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    bio = models.CharField(max_length=150, blank=True)
    theme = models.CharField(max_length=10, default="dark")  # 앱 설정
    note_default_public = models.BooleanField(default=True)  # 앱 설정
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # 탈퇴 시각


# 2. CaskType
class CaskType(models.Model):
    name = models.CharField(max_length=100)        # "Sherry", "Bourbon", "Port"
    description = models.TextField(blank=True)


# 3. Whisky
class Whisky(models.Model):
    # 기본 정보
    name = models.CharField(max_length=200)
    distillery = models.CharField(max_length=200)
    style = models.CharField(max_length=50, choices=STYLE_CHOICES)
    region = models.CharField(max_length=50, choices=REGION_CHOICES, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    abv = models.FloatField()
    cask_types = models.ManyToManyField(CaskType, blank=True)
    peat_level = models.PositiveIntegerField(default=0)  # 0-100

    # 도슨트 콘텐츠
    description = models.TextField()
    history = models.TextField(blank=True)
    bartender_tip = models.TextField(blank=True)
    pairing = models.TextField(blank=True)
    serving_guide = models.JSONField(default=dict)
    flavor_profile = models.JSONField(default=dict)  # {"smoky": 80, "sweet": 30 ...}

    # 메타
    image = models.ImageField(upload_to='whiskies/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def country(self):
        scotch = ["scotch_single_malt", "scotch_blended", "scotch_blended_malt", "scotch_single_grain"]
        if self.style in scotch:
            return "Scotland"
        mapping = {
            "bourbon": "USA", "rye": "USA", "tennessee": "USA",
            "irish": "Ireland",
            "japanese_single_malt": "Japan", "japanese_blended": "Japan",
        }
        return mapping.get(self.style, "Other")


# 4. TastingNote
class TastingNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    whisky = models.ForeignKey(Whisky, on_delete=models.CASCADE)

    tags = models.JSONField(default=list)       # 유저 자유 입력, 태그당 20자 / 최대 10개
    note = models.TextField(blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # 0.5 단위, 5.0 만점

    is_public = models.BooleanField(default=True)
    tasted_at = models.DateField(default=date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-tasted_at"]


# 5. Collection (내 장식장 - 마셔본 것)
class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    whisky = models.ForeignKey(Whisky, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "whisky")


# 6. Wishlist (위시리스트)
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    whisky = models.ForeignKey(Whisky, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "whisky")


# 7. ChatSession / ChatMessage (AI 큐레이터)
class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ChatMessage(models.Model):
    ROLE_CHOICES = [("user", "User"), ("assistant", "Assistant")]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    recommended_whiskies = models.ManyToManyField(Whisky, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]