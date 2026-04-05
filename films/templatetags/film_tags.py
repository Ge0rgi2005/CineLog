from django import template

register = template.Library()


@register.filter(name='rating_stars')
def rating_stars(value):
    try:
        rating = int(value)
        filled = '★' * (rating // 2)
        empty = '☆' * (5 - rating // 2)
        return filled + empty
    except (ValueError, TypeError):
        return ''


@register.filter(name='duration_display')
def duration_display(minutes):
    try:
        minutes = int(minutes)
        hours = minutes // 60
        remaining = minutes % 60
        if hours > 0:
            return f"{hours}h {remaining}m"
        return f"{remaining}m"
    except (ValueError, TypeError):
        return ''


@register.simple_tag
def get_genre_count(genre):
    return genre.movies.count()