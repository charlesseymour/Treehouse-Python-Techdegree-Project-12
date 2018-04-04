from django import template

register = template.Library()

@register.filter
def return_item(l, i):
    try:
        return l[i]
    except:
        return None
        
@register.filter
def get_id(position_id):
    try:
        position_id = position_id.replace('id_positions-', '')
        position_id = int(position_id.replace('-title', ''))
    except:
        None