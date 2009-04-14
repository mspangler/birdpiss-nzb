from django import template
from django.utils.translation import ungettext, ugettext as _
import datetime

register = template.Library()

@register.filter
def date_diff(d):

    now = datetime.datetime.now()
    today = datetime.datetime(now.year, now.month, now.day)
    delta = now - d
    delta_midnight = today - d
    days = delta.days
    hours = round(delta.seconds / 3600., 0)
    minutes = round(delta.seconds / 60., 0)
    chunks = (
        (365.0, lambda n: ungettext('year', 'years', n)),
        (30.0, lambda n: ungettext('month', 'months', n)),
        (7.0, lambda n : ungettext('week', 'weeks', n)),
        (1.0, lambda n : ungettext('day', 'days', n)),
    )
    
    if days == 0:
        if hours == 0:
            if minutes > 0:
                return ungettext('1 minute', \
                    '%(minutes)d minutes', minutes) % \
                    {'minutes': minutes}
            else:
                return _("1 minute")
        else:
            return ungettext('1 hour', '%(hours)d hours', hours) \
            % {'hours':hours}

    if delta_midnight.days == 0:
        #return _("yesterday at %s") % d.strftime("%H:%M")
        return _("1 day")

    count = 0
    for i, (chunk, name) in enumerate(chunks):
        if days >= chunk:
            count = round((delta_midnight.days + 1)/chunk, 0)
            break

    return _('%(number)d %(type)s') % \
        {'number': count, 'type': name(count)}
