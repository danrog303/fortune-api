import os
import lorem
from django.core.management import BaseCommand
from fortune_models.models import FortunePool, FortuneEntry, FortuneImage
from fortune_api.settings import BASE_DIR
from django.core.files.base import ContentFile


class Command(BaseCommand):
    help = 'Prepopulates fortune_api database with some dummy data.'

    pool_data = {
        "name": "albert-einstein-quotes",
        "description": "Quotes of Albert Einstein.",
        "entry_expiration_seconds": 5,
        "public": True
    }

    einstein_images = ["einstein_1.jpg", "einstein_2.jpg", "einstein_3.jpg", "einstein_4.jpg"]
    einstein_images_dir = os.path.join(BASE_DIR, "fortune_prepopulate/assets")

    def pool_exists(self):
        return FortunePool.objects.filter(name__exact=self.pool_data["name"]).count() > 0

    def create_entries(self):
        pool = FortunePool.objects.filter(name__exact=self.pool_data["name"]).first()
        images = [
            FortuneImage.objects.filter(name__exact=img.split(".")[0]).first()
            for img in self.einstein_images
        ]

        FortuneEntry.objects.create(pool=pool, image=images[0], text=lorem.paragraph(), trigger="trigger_morning")
        FortuneEntry.objects.create(pool=pool, image=images[1], text=lorem.paragraph(), trigger="trigger_morning")
        FortuneEntry.objects.create(pool=pool, image=images[2], text=lorem.paragraph(), trigger="trigger_noon")
        FortuneEntry.objects.create(pool=pool, image=images[3], text=lorem.paragraph(), trigger="trigger_noon")
        FortuneEntry.objects.create(pool=pool, image=images[0], text=lorem.paragraph(), trigger="trigger_evening")
        FortuneEntry.objects.create(pool=pool, image=images[1], text=lorem.paragraph(), trigger="trigger_evening")
        FortuneEntry.objects.create(pool=pool, image=images[2], text=lorem.paragraph(), trigger="trigger_night")
        FortuneEntry.objects.create(pool=pool, image=images[3], text=lorem.paragraph(), trigger="trigger_night")

    def create_pool(self):
        FortunePool.objects.create(**self.pool_data)

    def upload_images(self):
        for image_name in self.einstein_images:
            image_path = os.path.join(self.einstein_images_dir, image_name)
            fi_obj = FortuneImage.objects.create(name=image_name.split('.')[0])
            fi_obj.img.save(
                image_name,
                content=ContentFile(open(image_path, "rb").read()),
                save=True
            )

    def handle(self, *args, **options):
        if self.pool_exists():
            self.stdout.write(self.style.ERROR(f"Database prepopulation failed."))
            self.stdout.write(self.style.ERROR(f"Pool '{self.pool_data['name']}' already exists."))
            exit(1)

        self.create_pool()
        self.upload_images()
        self.create_entries()

        self.stdout.write(self.style.SUCCESS(f"Database propopulation succeeded."))
        self.stdout.write(self.style.SUCCESS(f"Visit /api/pool/{self.pool_data['name']}/ endpoint to see changes."))

