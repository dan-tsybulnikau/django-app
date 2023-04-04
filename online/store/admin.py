from django.contrib import admin
from .models import Category, Game


class GameInline(admin.StackedInline):
    model = Game


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):

    list_display = ("title", "view_game_link")
    inlines = [
        GameInline,
    ]

    @admin.display(description="games")
    def view_game_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        from django.utils.http import urlencode

        count = obj.game_set.count()
        url = (
            reverse("admin:store_game_changelist")
            + "?"
            + urlencode({"category_id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Games</a>', url, count)


@admin.register(Game)
class AdminGame(admin.ModelAdmin):
    date_hierarchy = "release_date"
    list_editable = ("release_date",)
    sortable_by = ("name", "release_date")
    list_filter = ("category",)
    search_fields = ("category__title", "name")
    radio_fields = {"category":admin.HORIZONTAL}
    
    # readonly_fields = ('img_tag',)
    list_display = (
        "name",
        "release_date",
        "show_pretty_price",
        # "img_preview",
        "get_link",
    )
    actions = ("make_inactive", "export_as_json")

    @admin.display(description="custom price")
    def show_pretty_price(self, obj):
        return f"$ {obj.price}"

    @admin.display(description="game image")
    def img_preview(self, obj):
        from django.utils.html import mark_safe

        return mark_safe(
            f'<img src = "{obj.game_image.url}" width ="150px" height="200px"/>'
        )

    @admin.display(description="game link")
    def get_link(self, obj):
        from django.utils.html import mark_safe

        return mark_safe(
            f'<a href="https://ru.wikipedia.org/wiki/{obj.name}">Search</a>'
        )

    @admin.action(description="Перевести в неактивное состояние")
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Скачать")
    def export_as_json(self, request, queryset):
        from django.core import serializers
        from django.http import FileResponse
        import io
        from datetime import datetime
        response = FileResponse(
            io.BytesIO(serializers.serialize("json", queryset).encode("utf-8")),
            as_attachment=True,
            filename=f"log-{datetime.now()}.txt",
        )
        return response