from django import template

register = template.Library()


@register.inclusion_tag("blog/partials/post_list.html", takes_context=True)
def filter_user_posts(context, status):

    # Convert the status to a boolean if it's a string
    if isinstance(status, str):
        if status.lower() == "true":
            status = True
        elif status.lower() == "false":
            status = False
        else:
            status = None

    user_posts = context["posts"].filter(published_status=status)

    return {
        "posts": user_posts,
        "request": context["request"],
    }
