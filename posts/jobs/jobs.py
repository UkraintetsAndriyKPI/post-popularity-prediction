import os
import json
import random
import re
import praw
from django.utils import timezone
from datetime import datetime
from openai import OpenAI

from posts.models import Post, Prediction
from django.contrib.auth.models import User

client = OpenAI(
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/',
    api_key=os.environ.get("GEMINI_API"),
)

CATEGORIES = [
    'news',
    'worldnews',
    'technology',
    'science',
    'gadgets',
    'politics',
    'space',
    'education',
    'business'
]

reddit = praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                     client_secret=os.getenv('CLIENT_SECRET'),
                     user_agent='post getting agent')

def get_reddit_post():
    subreddit_name = random.choice(CATEGORIES)
    print(f"📂 Subreddit: r/{subreddit_name}")


    posts = list(reddit.subreddit(subreddit_name).new(limit=10))

    if not posts:
        print("No posts found.")
        return

    post = random.choice(posts)

    print("📢 Post title:")
    print(post.title)

    if post.selftext:
        print("\n📝 Post text:")
        print(post.selftext)

    print("\n🔗 Link to post:")
    print(f"https://reddit.com{post.permalink}")


    post_creation_timestamp = datetime.utcfromtimestamp(post.created_utc)
    post_creation_timestamp = timezone.make_aware(post_creation_timestamp, timezone.get_current_timezone())


    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a social media post analyst who predicts the popularity of Reddit or Twitter posts. "
                    "You need to estimate the number of likes, comments, shares, and the overall mood (sentiment) of the post. "
                    "Output must be in JSON format with keys: 'likes', 'comments', 'shares', and 'mood'."
                )
            },
            {
                "role": "user",
                "content": (
                    "Here is a post:\n"
                    f"Title: {post.title}\n"
                    f"Content: {post.selftext}"
                )
            }
        ],
        temperature=0.7,
    )

    response_text = response.choices[0].message.content

    cleaned = re.sub(r"```json|```", "", response_text).strip()

    reply_result = json.loads(cleaned)
    print(reply_result)

    Post.objects.create(user_id=User.objects.get(username='admin'),
                        platform='reddit',
                        url=f"https://reddit.com{post.permalink}",
                        title=post.title,
                        content=post.selftext,

                        post_creation_timestamp=post_creation_timestamp,
                        likes=post.score,
                        comments=post.num_comments,
                        prediction=Prediction(
                            predicted_likes = reply_result['likes'],
                            predicted_comments = reply_result['comments'],
                            predicted_shares = reply_result['shares'],
                            predicted_mood = reply_result['mood'],
                        ))
