from django import template

register = template.Library()

'''@register.filter('form_name')
def form_name(form):
    return "form-" + str(form.auto_id) + "-name"'''