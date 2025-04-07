from django import template

from carts.models import Cart


register = template.Library()

@register.simple_tag()
def user_carts(request):
    try:
        if request.user.is_authenticated:
            carts = Cart.objects.filter(user=request.user).select_related('product')
            return carts
        else:

            return Cart.objects.none()
    except Exception as e:

        return Cart.objects.none()
