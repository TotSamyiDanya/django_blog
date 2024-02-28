from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Логин',
                'autocomplete': 'off'
            }
        )
    )
    password = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Пароль',
                'type': 'password',
                'autocomplete': 'off'
            }
        )
    )
    avatar = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control custom-input button-blog',
                'type': 'file'
            }
        )
    )


class LoginForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Логин',
                'autocomplete': 'off'
            }
        )
    )
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Пароль',
                'type': 'password',
                'autocomplete': 'off'
            }
        )
    )


class PostForm(forms.Form):
    title = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Заголовок...',
                'autocomplete': 'off',
                'rows': '3'
            }
        )
    )
    subtitle = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Подзаголовок...',
                'autocomplete': 'off',
                'rows': '3'
            }
        )
    )
    topic = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Тема...',
                'autocomplete': 'off'
            }
        )
    )
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control custom-input input-blog',
                'placeholder': 'Текст...',
                'autocomplete': 'off',
                'rows': '30'
            }
        )
    )
    cover = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'class': 'form-control custom-input button-blog',
                'type': 'file',
                'accept': 'image/*',
                'id': 'imageInput'
            }
        )
    )
