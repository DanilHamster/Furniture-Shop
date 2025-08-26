from .forms import SearchItemForm


def global_search_form(request):
    return {"search_form": SearchItemForm(request.GET or None)}
