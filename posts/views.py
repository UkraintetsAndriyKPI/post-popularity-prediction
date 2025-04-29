import re
import json
from datetime import datetime
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from posts.models import Post, Prediction
from posts.forms import PostAttempt
from posts.jobs.jobs import CATEGORIES, client, reddit


@login_required
def post_attempt(request):
    form = PostAttempt(request.POST or None)

    context = {
        'page_name': f"Attempt page | {request.user.username}",
        'form': form,
    }


    if request.method == 'POST':
        if form.is_valid():
            post_url = form.cleaned_data['url']
            print(f"URL from form: {post_url}")

            try:
                submission = reddit.submission(url=str(form.cleaned_data['url']).strip())
            except:
                messages.error(request, "Can not find the post. Maybe post didn't exist. Or try again later.")
                return render(request, 'main/post_attempt.html', context)

            post_creation_timestamp = datetime.utcfromtimestamp(submission.created_utc)
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
                            f"Title: {submission.title}\n"
                            f"Content: {submission.selftext}"
                        )
                    }
                ],
                temperature=0.7,
            )

            response_text = response.choices[0].message.content
            cleaned = re.sub(r"```json|```", "", response_text).strip()
            reply_result = json.loads(cleaned)

            post = Post.objects.create(user_id=User.objects.get(id=request.user.id),
                        platform='reddit',
                        url=f"https://reddit.com{submission.permalink}",
                        title=submission.title,
                        content=submission.selftext,

                        post_creation_timestamp=post_creation_timestamp,
                        likes=submission.score,
                        comments=submission.num_comments,
                        prediction=Prediction(
                            predicted_likes = reply_result['likes'],
                            predicted_comments = reply_result['comments'],
                            predicted_shares = reply_result['shares'],
                            predicted_mood = reply_result['mood'],
                        ))

            messages.success(request, "Prediction successfully created.")
            return redirect('prediction_detail', post.id)

    return render(request, 'main/post_attempt.html', context)



def prediction_detail(request, pk):
    post_prediction = get_object_or_404(Post, id=pk)
    return render(request,'main/post_prediction_detail.html',
                  {'post_prediction': post_prediction})
