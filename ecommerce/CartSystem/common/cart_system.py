from django.db.models import Q
from CartSystem import models as cart_models


def get_wishlist_by_user(request):
    """
        Quantity:   If empty, then unlimited
                    If 0, finished
                    If >0, show the quantity
    """
    wishlists = cart_models.WishList.objects.filter(user=request.user)
    wishlist_data = []
    for data in wishlists:
        quantity = "Unlimited"
        if data.product.quantity_left < 1:
            quantity = "Finished"
        elif data.product.quantity_left and data.product.quantity_left > 0:
            quantity = data.product.quantity_left

        wishlist_data.append({
            "id": data.id,
            "englishName": data.product.english_name,
            "nepaliName": data.product.nepali_name,
            "oldPrice": data.product.old_price,
            "price": data.product.price,
            "mainImage": request.build_absolute_uri(data.product.main_image.url),
            "quantityLeft": quantity
        })
    return wishlist_data


def get_user_cart(request):
    if request.user.is_authenticated:
        cart = cart_models.AddToCart.objects.filter(user=request.user)
        data = []
        total = 0
        if cart:
            for item in cart:
                if not item.product.soft_delete and item.product.status:
                    total_price = item.quantity * item.product.price
                    total += total_price
                    data.append({
                        "id": item.id,
                        "englishName": item.product.english_name,
                        "nepaliName": item.product.nepali_name,
                        "price": item.product.price,
                        "quantity": item.quantity,
                        "mainImage": request.build_absolute_uri(item.product.main_image.url),
                        "totalPrice": total_price
                    })
                else:
                    item.delete()
    return data, total


def check_cart(request, product):
    try:
        cart = cart_models.AddToCart.objects.get(
            Q(product=product) & Q(user=request.user))
        return True
    except (Exception, cart_models.AddToCart.DoesNotExist):
        return False


def check_whislist(request, product):
    try:
        cart = cart_models.WishList.objects.get(
            Q(product=product) & Q(user=request.user))
        return True
    except (Exception, cart_models.WishList.DoesNotExist):
        return False


def delete_from_wishlist(request, pk):
    try:
        wishlist = cart_models.WishList.objects.get(pk=pk)
        if request.user == wishlist.user:
            wishlist.delete()
            return True
    except (cart_models.WishList.DoesNotExist, Exception) as e:
        return False

    return False
