from django import template

register = template.Library()

@register.filter(name='get_status_badge_class')
def get_status_badge_class(status):
    if status == 'COMPLETED':
        return 'bg-success'
    elif status == 'IN_PROGRESS':
        return 'bg-primary'
    elif status == 'BLOCKED':
        return 'bg-danger'
    # Mặc định là 'TODO'
    return 'bg-secondary'