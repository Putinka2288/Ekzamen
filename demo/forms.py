from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from demo.models import User


def validate_passwod(password):
    if len(password) < 6:
        raise ValidationError('Пароль меньше 6 ')


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
                               validators=[RegexValidator('^[a-zA-Z0-9-]+$',
                                                          message='Разрешена только латиница, цифры и тире')],
                               error_messages={
                                   'required': 'Обязательое поле',
                                   'unique': 'Логин занят'
                               })

    email = forms.EmailField(label='Почта',
                             error_messages={
                                 'required': 'Обязательное поле',
                                 'unique': 'Почта занята'
                             })

    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput,
                               validators=[validate_passwod],
                               error_messages={
                                   'required': 'Обязательное поле'
                               })

    password2 = forms.CharField(label='Пароль(повторно)',
                                widget=forms.PasswordInput,
                                validators=[validate_passwod],
                                error_messages={
                                    'required': 'Обязательное поле'
                                })

    name = forms.CharField(label='Имя',
                           validators=[
                               RegexValidator('^[а-яА-Я- ]+$', message='Разрешены только кирилица пробел и тире')],
                           error_messages={
                               'required': 'Обязательное поле'
                           })

    surname = forms.CharField(label='Фамилия',
                              validators=[
                                  RegexValidator('^[а-яА-Я- ]+$', message='Разрешены только кирилица пробел и тире')],
                              error_messages={
                                  'required': 'Обязательное поле'
                              })

    patronymic = forms.CharField(label='Отчество',
                                 required=False,
                                 validators=[
                                     RegexValidator('^[а-яА-Я- ]+$',
                                                    message='Разрешены только кирилица пробел и тире')]
                                 )

    rule = forms.BooleanField(label='Соглашение с правилами',
                              required=True,
                              error_messages={
                                  'required': 'Обязательное поле'
                              })

    def clean(self, commit=True):
        super().clean()
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise ValidationError({
                'password2': ValidationError('Пароли не равны', code='password_mismatch')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password2'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'name', 'surname', 'patronymic', 'rule')


class OrderForm(forms.ModelForm):
    def clean(self):
        status = self.cleaned_data.get('status')
        rejection_reason = self.cleaned_data.get('rejection_reason')
        if self.instance.status != 'new':
            raise ValidationError({'status': 'Можно менять только у новых заказов'})

        if status == 'canceled' and not rejection_reason:
            raise ValidationError({'rejection_reason': 'Укажите причину'})