from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import AuthTable, Packages, InactivePrepaid, NullSpeedRegularUsers, NullSpeedUnusedCafe, CafeCards


class LoginForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
        # if user.username.startswith('b'):
        #     raise ValidationError(
        #         _("Sorry, accounts starting with 'b' aren't welcome here."),
        #         code='no_b_users',
        #     )

class AuthTableForm(ModelForm):
    """
    AuthTable form (Add entry/Edit entry)
    """
    class Meta:
        model = AuthTable
        fields = '__all__'
        exclude = ['id']

class PackagesForm(ModelForm):
    """
    Packages form (Add entry/Edit entry)
    """
    class Meta:
        model = Packages
        fields = '__all__'
        exclude = ['id']
    
class InactivePrepaidForm(ModelForm):
    """
    InactivePrepaid form (Add entry/Edit entry)
    """
    class Meta:
        model = InactivePrepaid
        fields = '__all__'
        exclude = ['id']

class NullSpeedRegularUsersForm(ModelForm):
    """
    NullSpeedRegularUsers form (Add entry/Edit entry)
    """
    class Meta:
        model = NullSpeedRegularUsers
        fields = '__all__'
        exclude = ['id']

class NullSpeedUnusedCafeForm(ModelForm):
    """
    NullSpeedUnusedCafe form (Add entry/Edit entry)
    """
    class Meta:
        model = NullSpeedUnusedCafe
        fields = '__all__'
        exclude = ['id']

class CafeCardsForm(ModelForm):
    """
    CafeCards form (Add entry/Edit entry)
    """
    class Meta:
        model = CafeCards
        fields = '__all__'
        exclude = ['id']