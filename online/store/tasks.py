# from better_profanity import profanity
import time
from celery import shared_task
from django.core import serializers

# profanity.load_censor_words()

# @shared_task()
# def replace_text_with_censored(instance):
#     instance = list(serializers.deserialize('json', instance))[0].object
#     censored_text = profanity.censor(instance.text)
#     time.sleep(5)
#     instance.text = censored_text
#     instance.save()
    
@shared_task()
def sample_task():
    print("The beat is running...")
    

from django.core.mail import send_mail
from django.urls import reverse_lazy
from typing import List

@shared_task()
def send_news_email_task(games: List[dict], user:dict):
    message_text = f'Hello {user["username"]}! See all our updates from last week!\n'
    for game in games:
        msg_chunk = f"""
        {games['name']} added at {games['release_date']}, price - {games['price']}
        More details: {reverse_lazy("store:game-detail", args=game['slug'])}
        """
        message_text += msg_chunk
    send_mail(
        "Weekly news",
        message_text,
        "support@example.com",
        [user['email']],
        fail_silently=False,
    )

from .models import Game
from django.contrib.auth.models import User
import datetime

@shared_task()  
def weekly_notification():
    all_users = list(User.objects.filter(is_staff=False).values())
    # print(all_users)
    all_new_games = list(Game.objects.filter(pub_date__gte=datetime.datetime.today()-datetime.timedelta(days=7)).values())
    # print(all_new_games)
    for user in all_users:
        send_news_email_task.delay(all_new_games, user)

