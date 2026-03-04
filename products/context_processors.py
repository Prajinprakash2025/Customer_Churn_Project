from .models import Category

def categories_processor(request):
    """
    Returns categories to all templates.
    """
    categories = Category.objects.all()
    return {
        'categories': categories
    }
