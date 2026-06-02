from django.contrib import admin
from django.utils.html import format_html
from .models import User, Image, Prediction, PredictionHistory
# =========================
# 👤 USER ADMIN
# =========================
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'email', 'phone')
    search_fields = ('firstname', 'lastname', 'email')


# =========================
# 🖼️ IMAGE ADMIN (WITH PREVIEW)
# =========================
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'preview', 'uploaded_at')

    def preview(self, obj):
        if obj.image_file:
            return format_html('<img src="{}" width="100" height="100" />', obj.image_file.url)
        return "No Image"

    preview.short_description = "Image Preview"


# =========================
# 🤖 PREDICTION ADMIN
# =========================
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'disease_name', 'confidence_score', 'created_at')
    search_fields = ('disease_name',)


# =========================
# 📜 HISTORY ADMIN
# =========================
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prediction', 'viewed_at')


# =========================
# REGISTER MODELS
# =========================
admin.site.register(User, UserAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Prediction, PredictionAdmin)
admin.site.register(PredictionHistory, PredictionHistoryAdmin)

