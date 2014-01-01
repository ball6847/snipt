from registration.backends.simple.views import RegistrationView
from .forms import SniptRegistrationForm

class SniptRegistrationView(RegistrationView):
    """
    Custom registration view that uses our custom form.
    
    """
    form_class = SniptRegistrationForm
