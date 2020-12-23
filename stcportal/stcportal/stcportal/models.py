from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, Permission
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom User Manager class that extends BaseUserManager class
    allowing to define more fields than default related to the User.
    """
    def create_user(self, email, first_name, last_name,
                    password=None, commit=True):
        """
        Creates and saves an IOC Support User with the given email,
        first name, last name and password.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not first_name:
            raise ValueError(_('Users must have a first name'))
        if not last_name:
            raise ValueError(_('Users must have a last name'))

        user = self.model(
            email=self.normalize_email(email), #lowercase
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves an IOC Admin with the given email, first name,
        last name and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            commit=False,
        )
        user.is_staff = True
        user.is_superuser = True
        # user.role = "IOC Admin"
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Custom User class that extends AbstractBaseUser class
    allowing to define more fields than default related to the User.
    """
    email = models.EmailField(
        verbose_name=_('email address'), max_length=255, unique=True
    )
    # password field supplied by AbstractBaseUser
    # last_login field supplied by AbstractBaseUser
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_active = models.BooleanField(
        _('Active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('IOC Admin'),
        default=False,
        help_text=_(
            'Designates whether role of this user is IOC Admin (else is IOC Support User).'
        ),
    )
    read_only = models.BooleanField(
        _('Read Only'),
        default=True,
        help_text=_(
            'Read Only Permission'
        ),
    )
    subscribers_management = models.BooleanField(
        _('Subscribers Management'),
        default=False,
        help_text=_(
            'Subscribers Management Permission'
        ),
    )
    reporting_and_monitoring = models.BooleanField(
        _('Reporting & Monitoring'),
        default=False,
        help_text=_(
            'Reporting & Monitoring Permission'
        ),
    )

    # is_superuser field provided by PermissionsMixin
    # groups field provided by PermissionsMixin
    # user_permissions field provided by PermissionsMixin

    date_joined = models.DateTimeField(
        _('date joined'), default=timezone.now
    )

    objects = UserManager()

    # USERNAME and PASSWORD always prompted, should not be REQUIRED
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '{} <{}>'.format(self.get_full_name(), self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the STCS Management Portal?"
        # Simplest possible answer: Yes, always
        return True


class AuthTable(models.Model):
    """
    Custom AuthTable model class that defines AuthTable table
    from External (MariaDB) database.
    """
    # id = models.CharField(max_length=40, primary_key=True)
    userlogin = models.CharField(unique = True, max_length=40)
    timebanking = models.CharField(max_length=40, blank=True, null=True)
    FreeTime = models.CharField(max_length=40, blank=True, null=True)
    endofsubscription = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    framedip = models.CharField(max_length=40, blank=True, null=True)
    loginlimit = models.CharField(max_length=40, blank=True, null=True)
    blnRoaming = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    olddomain = models.CharField(max_length=40, blank=True, null=True)
    newdomain = models.CharField(max_length=40, blank=True, null=True)
    calledstationid = models.CharField(max_length=40, blank=True, null=True)
    poolhint = models.CharField(max_length=40, blank=True, null=True)
    typeid = models.CharField(max_length=40, blank=True, null=True)
    speed = models.CharField(max_length=40, blank=True, null=True)
    package = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    usertelephone = models.CharField(max_length=40, blank=True, null=True)
    usernationality = models.CharField(max_length=40, blank=True, null=True)
    idnumber = models.CharField(max_length=40, blank=True, null=True)
    idtype = models.CharField(max_length=40, blank=True, null=True)
    mobile = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    accounttype = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'AuthTable'

class InactivePrepaid(models.Model):
    """
    Custom InactivePrepaid model class that defines AuthTable table
    from External (MariaDB) database.
    """
    # id = models.CharField(max_length=40, primary_key=True)
    code = models.CharField(max_length=40, blank=True, null=True)
    Type = models.CharField(db_column='type', max_length=40, blank=True, null=True)
    accounttype = models.CharField(max_length=40, blank=True, null=True)
    hours = models.CharField(max_length=40, blank=True, null=True)
    generationdate = models.CharField(max_length=40, blank=True, null=True)
    usagedate = models.CharField(max_length=40, blank=True, null=True)
    userlogin = models.CharField(max_length=40, blank=True, null=True)
    dealer = models.CharField(max_length=40, blank=True, null=True)
    selldate = models.CharField(max_length=40, blank=True, null=True)
    sellprice = models.CharField(max_length=40, blank=True, null=True)
    tracknumber = models.CharField(max_length=40, blank=True, null=True)
    markdel = models.CharField(max_length=40, blank=True, null=True)
    promoid = models.CharField(max_length=40, blank=True, null=True)
    promocollected = models.CharField(max_length=40, blank=True, null=True)
    cardpromodays = models.CharField(max_length=40, blank=True, null=True)
    overactive = models.CharField(max_length=40, blank=True, null=True)
    transferreddays = models.CharField(max_length=40, blank=True, null=True)
    typeid = models.CharField(max_length=40, blank=True, null=True)
    speed = models.CharField(max_length=40, blank=True, null=True)
    package = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'InactivePrepaid'

class Packages(models.Model):
    """
    Custom Packages model class that defines Packages table
    from External (MariaDB) database.
    """
    TypeID = models.CharField(max_length=40, primary_key=True)
    # TypeID = models.CharField(max_length=40, blank=True, null=True)
    Type = models.CharField(max_length=40, blank=True, null=True)
    HourlyRate = models.CharField(max_length=40, blank=True, null=True)
    Sub_NoSub = models.CharField(max_length=40, blank=True, null=True)
    SubscriptionFee = models.CharField(max_length=40, blank=True, null=True)
    FreeHours = models.CharField(max_length=40, blank=True, null=True)
    Description = models.CharField(max_length=40, blank=True, null=True)
    countlogin = models.CharField(max_length=40, blank=True, null=True)
    billperiod = models.CharField(max_length=40, blank=True, null=True)
    visible = models.CharField(max_length=40, blank=True, null=True)
    AutoRenewable = models.CharField(max_length=40, blank=True, null=True)
    timebanking = models.CharField(max_length=40, blank=True, null=True)
    Promotion = models.CharField(max_length=40, blank=True, null=True)
    Unlimited = models.CharField(max_length=40, blank=True, null=True)
    OnlinePay = models.CharField(max_length=40, blank=True, null=True)
    SMSCredits = models.CharField(max_length=40, blank=True, null=True)
    OnlineSubscriptionFee = models.CharField(max_length=40, blank=True, null=True)
    ReferrerDays = models.CharField(max_length=40, blank=True, null=True)
    ReferrerHours = models.CharField(max_length=40, blank=True, null=True)
    Dealers = models.CharField(max_length=40, blank=True, null=True)
    FreeCourses = models.CharField(max_length=40, blank=True, null=True)
    DiscountCourses = models.CharField(max_length=40, blank=True, null=True)
    Promotime = models.CharField(max_length=40, blank=True, null=True)
    Promodays = models.CharField(max_length=40, blank=True, null=True)
    HasEmail = models.CharField(max_length=40, blank=True, null=True)
    GroupId = models.CharField(max_length=40, blank=True, null=True)
    RoamingFreeHours = models.CharField(max_length=40, blank=True, null=True)
    Speed = models.CharField(max_length=40, blank=True, null=True)
    Price = models.CharField(max_length=40, blank=True, null=True)
    DayPrice = models.CharField(max_length=40, blank=True, null=True)
    UserType = models.CharField(max_length=40, blank=True, null=True)
    HostingPlanID = models.CharField(max_length=40, blank=True, null=True)
    GmailUsers = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'Packages'

class NullSpeedRegularUsers(models.Model):
    """
    Custom NullSpeedRegularUsers model class that defines
    NullSpeedregularUsers table from External (MariaDB) database.
    """
    # id = models.CharField(max_length=40, primary_key=True)
    userlogin = models.CharField(unique=True, max_length=40)
    timebanking = models.CharField(max_length=40, blank=True, null=True)
    FreeTime = models.CharField(max_length=40, blank=True, null=True)
    endofsubscription = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    framedip = models.CharField(max_length=40, blank=True, null=True)
    loginlimit = models.CharField(max_length=40, blank=True, null=True)
    blnRoaming = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    olddomain = models.CharField(max_length=40, blank=True, null=True)
    newdomain = models.CharField(max_length=40, blank=True, null=True)
    calledstationid = models.CharField(max_length=40, blank=True, null=True)
    poolhint = models.CharField(max_length=40, blank=True, null=True)
    typeid = models.CharField(max_length=40, blank=True, null=True)
    speed = models.CharField(max_length=40, blank=True, null=True)
    package = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    usertelephone = models.CharField(max_length=40, blank=True, null=True)
    usernationality = models.CharField(max_length=40, blank=True, null=True)
    idnumber = models.CharField(max_length=40, blank=True, null=True)
    idtype = models.CharField(max_length=40, blank=True, null=True)
    mobile = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'NullSpeedRegularUsers'

class NullSpeedUnusedCafeCards(models.Model):
    """
    Custom NullSpeedUnusedCafeCards model class that defines 
    NullSpeedUnusedCafeCards table from External (MariaDB) database.
    """
    # id = models.IntegerField(primary_key=True)
    userlogin = models.CharField(unique=True, max_length=40)
    timebanking = models.CharField(max_length=40, blank=True, null=True)
    FreeTime = models.CharField(max_length=40, blank=True, null=True)
    endofsubscription = models.CharField(max_length=40, blank=True, null=True)
    password = models.CharField(max_length=40, blank=True, null=True)
    framedip = models.CharField(max_length=40, blank=True, null=True)
    loginlimit = models.CharField(max_length=40, blank=True, null=True)
    blnRoaming = models.CharField(max_length=40, blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    olddomain = models.CharField(max_length=40, blank=True, null=True)
    newdomain = models.CharField(max_length=40, blank=True, null=True)
    calledstationid = models.CharField(max_length=40, blank=True, null=True)
    poolhint = models.CharField(max_length=40, blank=True, null=True)
    typeid = models.CharField(max_length=40, blank=True, null=True)
    speed = models.CharField(max_length=40, blank=True, null=True)
    package = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=40, blank=True, null=True)
    usertelephone = models.CharField(max_length=40, blank=True, null=True)
    usernationality = models.CharField(max_length=40, blank=True, null=True)
    idnumber = models.CharField(max_length=40, blank=True, null=True)
    idtype = models.CharField(max_length=40, blank=True, null=True)
    mobile = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'NullSpeedUnusedCafeCards'

# class CafeCards(models.Model):
#     """
#     Custom CafeCards model class that defines 
#     CafeCards table from External (MariaDB) database.
#     """
#     id = models.CharField(max_length=40, primary_key=True)
#     userlogin = models.CharField(max_length=40)
#     timebanking = models.CharField(max_length=40)
#     FreeTime = models.CharField(max_length=40)
#     endofsubscription = models.CharField(max_length=40)
#     password = models.CharField(max_length=40)
#     framedip = models.CharField(max_length=40)
#     loginlimit = models.CharField(max_length=40)
#     blnRoaming = models.CharField(max_length=40)
#     status = models.CharField(max_length=40)
#     olddomain = models.CharField(max_length=40)
#     newdomain = models.CharField(max_length=40)
#     calledstationdi = models.CharField(max_length=40)
#     poolhint = models.CharField(max_length=40)
#     typeid = models.CharField(max_length=40)
#     speed = models.CharField(max_length=40)
#     package = models.CharField(max_length=40)
#     username = models.CharField(max_length=40)
#     usertelephone = models.CharField(max_length=40)
#     usernationality = models.CharField(max_length=40)
#     idnumber = models.CharField(max_length=40)
#     idtype = models.CharField(max_length=40)
#     mobile = models.CharField(max_length=40)
#     email = models.CharField(max_length=40)

#     class Meta:
#         db_table = 'CafeCards'

from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import AuthTable, Packages, InactivePrepaid, NullSpeedRegularUsers, NullSpeedUnusedCafeCards


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

class NullSpeedUnusedCafeCardsForm(ModelForm):
    """
    NullSpeedUnusedCafe form (Add entry/Edit entry)
    """
    def __init__(self, *args, **kwargs):
        super(NullSpeedUnusedCafeCardsForm, self).__init__(*args, **kwargs)
        self.fields['userlogin'].required = True
        # self.fields['accounttype'].required = True
        self.fields['typeid'].required = True
        self.fields['speed'].required = True
        self.fields['package'].required = True
        # self.fields['endOfSubscription'].required = True
        # self.fields['status'].required = True

    class Meta:
        model = NullSpeedUnusedCafeCards
        fields = '__all__'
        exclude = ['id']

# class CafeCardsForm(ModelForm):
#     """
#     CafeCards form (Add entry/Edit entry)
#     """
#     class Meta:
#         model = CafeCards
#         fields = '__all__'
#         exclude = ['id']