from django.db import models
# from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from .manager import CompanyManager, CoordinatorManager, ParticipantManager, UserManager
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
import uuid


class Country(models.Model):
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=25)

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['title']

    def __str__(self):
        return self.title


class User(AbstractUser):

    objects = UserManager()

    def validate_agree(self):
        if not self:
            raise ValidationError(
                _('This field is required'),
                params={'value': self},
            )

    class Types(models.TextChoices):
        COMPANY = "COMPANY", "Company"
        COORDINATOR = "COORDINATOR", "Coordinator"
        PARTICIPANT = "PARTICIPANT", "Participant"
        STAFF = "STAFF", "Staff"

    language = models.CharField(max_length=10, choices=[
        ('en', _('English')),
        ('pt-br', _('Portuguese (Brazil)')),
    ], default='pt-br')

    id = models.UUIDField(primary_key=True,  default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=25, blank=True, null=True, default='Dynamic insert')
    type = models.CharField(_('Type'), max_length=50, choices=Types.choices, default=Types.PARTICIPANT)
    name = models.CharField(_('Name'), max_length=255)
    email = models.EmailField(_('Email'), unique=True)
    password = models.CharField(max_length=255)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    i_agree = models.BooleanField(default=False, validators=[validate_agree])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Coordinator(User):
    objects = CoordinatorManager()

    GENDERS = [
        (None, '-- I don\'t want to inform --'),
        ('Cis man', 'Cis man'),
        ('Cis woman', 'Cis woman'),
        ('Non-binary', 'Non-binary'),
        ('Queer', 'Queer'),
        ('Trans man', 'Trans man'),
        ('Trans woman', 'Trans woman'),
    ]
    SEXUAL_ORIENTATIONS = [
        (None, '-- I don\'t want to inform --'),
        ('Assexual', 'Assexual'),
        ('Bissexual', 'Bissexual'),
        ('Gay', 'Gay'),
        ('Heterosexual/straight', 'Heterosexual/straight'),
        ('Lesbian', 'Lesbian'),
        ('Pansexual', 'Pansexual'),
    ]
    DESABILITIES = [
        (None, '-- I don\'t want to inform --'),
        ('I identify myself as a person with visual disability', 'I identify myself as a person with visual disability'),
        ('I identify myself as a person with low vision', 'I identify myself as a person with low vision'),
        ('I identify myself as blind', 'I identify myself as blind'),
        ('I identify myself as a person with hearing disability', 'I identify myself as a person with hearing disability'),
        ('I identify myself as deaf', 'I identify myself as deaf'),
        ('I identify myself as a person with intelectual disability', 'I identify myself as a person with intelectual disability'),
        ('I identify myself as a person with mental disability', 'I identify myself as a person with mental disability'),
        ('I identify myself as a person with physical disability', 'I identify myself as a person with physical disability'),
        ('I identify myself as a person with no disability', 'I identify myself as a person with no disability'),
    ]

    picture = models.ImageField(_('photo'), upload_to='coordinator', )
    picture_description = models.CharField(_('Picture description'), max_length=255)
    phone = models.CharField(_('Phone number'), max_length=20, blank=True, null=True)
    social_name = models.CharField(_('Social Name'), max_length=125, blank=True, null=True)
    gender_identity = models.CharField(_('Gender identity'), max_length=80, choices=GENDERS, null=True, blank=True)
    other_gender = models.CharField(_('Other gender'), max_length=125, blank=True, null=True)
    sexual_orientation = models.CharField(_('Sexual orientation'), max_length=50, choices=SEXUAL_ORIENTATIONS, null=True, blank=True)
    other_orientation = models.CharField(_('Other orientation'), max_length=80, blank=True, null=True)
    desability = models.CharField(_('Desability'), max_length=100, choices=DESABILITIES, null=True, blank=True)
    other_desability = models.CharField(_('Other desability'), max_length=145, blank=True, null=True)
    title_pronoun = models.CharField(_('Title and Pronoun'), max_length=45, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Coordinator')
        verbose_name_plural = _('Coordinators')

    def save(self, *args, **kwargs):
        self.type = User.Types.COORDINATOR
        super(Coordinator, self).save(*args, **kwargs)


class Participant(User):
    objects = ParticipantManager()

    GENDERS = [
        (None, '-- I don\'t want to inform --'),
        ('Cis man', 'Cis man'),
        ('Cis woman', 'Cis woman'),
        ('Non-binary', 'Non-binary'),
        ('Queer', 'Queer'),
        ('Trans man', 'Trans man'),
        ('Trans woman', 'Trans woman'),
    ]
    SEXUAL_ORIENTATIONS = [
        (None, '-- I don\'t want to inform --'),
        ('Assexual', 'Assexual'),
        ('Bissexual', 'Bissexual'),
        ('Gay', 'Gay'),
        ('Heterosexual/straight', 'Heterosexual/straight'),
        ('Lesbian', 'Lesbian'),
        ('Pansexual', 'Pansexual'),
    ]
    DESABILITIES = [
        (None, '-- I don\'t want to inform --'),
        ('I identify myself as a person with visual disability', 'I identify myself as a person with visual disability'),
        ('I identify myself as a person with low vision', 'I identify myself as a person with low vision'),
        ('I identify myself as blind', 'I identify myself as blind'),
        ('I identify myself as a person with hearing disability', 'I identify myself as a person with hearing disability'),
        ('I identify myself as deaf', 'I identify myself as deaf'),
        ('I identify myself as a person with intelectual disability', 'I identify myself as a person with intelectual disability'),
        ('I identify myself as a person with mental disability', 'I identify myself as a person with mental disability'),
        ('I identify myself as a person with physical disability', 'I identify myself as a person with physical disability'),
        ('I identify myself as a person with no disability', 'I identify myself as a person with no disability'),
    ]

    pj = models.ForeignKey('project.Project', related_name='user_project', on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='participant', blank=True, null=True)
    picture_description = models.CharField(max_length=255, blank=True, null=True)
    social_name = models.CharField(max_length=125, blank=True, null=True)
    title_pronoun = models.CharField(max_length=45, blank=True, null=True)
    gender_identity = models.CharField(max_length=80, choices=GENDERS, null=True, blank=True)
    other_gender = models.CharField(max_length=125, blank=True, null=True)
    sexual_orientation = models.CharField(max_length=50, choices=SEXUAL_ORIENTATIONS, null=True, blank=True)
    other_orientation = models.CharField(max_length=80, blank=True, null=True)
    desability = models.CharField(max_length=100, choices=DESABILITIES, null=True, blank=True)
    other_desability = models.CharField(max_length=145, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Participant')
        verbose_name_plural = _('Participants')

    def save(self, *args, **kwargs):
        self.type = User.Types.PARTICIPANT
        super(Participant, self).save(*args, **kwargs)


class Manager(User):

    objects = CompanyManager()

    profile_manager = models.CharField(_('Manager Name'), max_length=255, default='')
    social_name = models.CharField(_('Social Name'), max_length=125, blank=True, null=True)
    title_pronoun = models.CharField(_('Title and Pronoun'), max_length=45, blank=True, null=True)
    is_resp = models.BooleanField(_('I am responsible for the information contained in this profile'),
                                  default=False, validators=[User.validate_agree])
    cnpj = models.CharField(_('CNPJ'), max_length=45)
    address = models.CharField(_('Address'), max_length=255, null=True, blank=True)
    phone_manager = models.CharField(_('Phone'), max_length=20, default='')
    email_manager = models.EmailField(_('Email'), max_length=255, default='')
    picture = models.ImageField(_('Company Logo'), upload_to='company',)
    banner = models.ImageField(_('Company Banner'), upload_to='company')
    picture_description = models.CharField(_('Logo description'), max_length=255)
    banner_description = models.CharField(_('Banner description'), max_length=255)
    phone = models.CharField(_('Company phone number'), max_length=20)

    company_description = RichTextField(_('Company description'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')

    def save(self, *args, **kwargs):
        self.type = User.Types.COMPANY
        super(Manager, self).save(*args, **kwargs)
