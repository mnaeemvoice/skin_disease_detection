from django.db import models  # ✅ یہ لائن ضروری ہے

class SkinDisease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class BeautyProduct(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    disease = models.ForeignKey(SkinDisease, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
