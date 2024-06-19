from ckeditor.fields import CKEditorWidget
from colorfield.widgets import ColorWidget
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

from account_module.models import User
from article_module.models import Article, ArticleCategory, ArticleTag
from contact_module.models import ContactUs
from order_module.models import Order, Address, Wholesale
from product_module.models import Product, ProductCategory, ProductTag, ProductGrind, ProductColor, ProductGallery, \
    Coupon
from site_module.models import SiteSetting, SiteBanner, SocialMedia, TopProduct, SiteSettingCategory, FooterLinkBox, \
    FooterLink
from wallet_module.models import Wallet, Transaction, WalletSetting


class AdminProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'title', 'image', 'price', 'availability_count', 'short_description', 'description', 'is_active', 'status',
            'category', 'tag', 'grind')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control mb-1',
                'id': 'id_amount_tomans'
            }),
            'availability_count': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': CKEditorWidget(),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        self.fields['tag'].widget = forms.CheckboxSelectMultiple()
        self.fields['grind'].widget = forms.CheckboxSelectMultiple()
        self.fields['category'].queryset = ProductCategory.objects.filter(is_active=True)
        self.fields['tag'].queryset = ProductTag.objects.filter(is_active=True)
        self.fields['grind'].queryset = ProductGrind.objects.filter(is_active=True)


class AdminCategoryModelForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = ('title', 'url_title', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'url_title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }


class AdminTagModelForm(forms.ModelForm):
    class Meta:
        model = ProductTag
        fields = ('title', 'url_title', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'url_title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }


class AdminColorModelForm(forms.ModelForm):
    class Meta:
        model = ProductColor
        fields = ('title', 'count', 'color', 'status', 'is_active', 'product')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'count': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'color': ColorWidget(),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation2'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()


class AdminGrindModelForm(forms.ModelForm):
    class Meta:
        model = ProductGrind
        fields = ('title', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }


class AdminGalleryModelForm(forms.ModelForm):
    class Meta:
        model = ProductGallery
        fields = ('is_active', 'product', 'image')
        widgets = {
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()


class AdminContactModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'create_date': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'response': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'is_read_by_admin': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'is_emailed': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation2'
            }),
        }


class AdminَArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title', 'slug', 'image', 'visit_count', 'short_description', 'description', 'is_active', 'category', 'tag')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput'
            }),
            'visit_count': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'description': CKEditorWidget(),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        self.fields['tag'].widget = forms.CheckboxSelectMultiple()
        self.fields['category'].queryset = ArticleCategory.objects.filter(is_active=True)
        self.fields['tag'].queryset = ArticleTag.objects.filter(is_active=True)


class AdminArticleTagModelForm(forms.ModelForm):
    class Meta:
        model = ArticleTag
        fields = ('title', 'url_title', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'url_title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }


class AdminArticleCategoryModelForm(forms.ModelForm):
    class Meta:
        model = ArticleCategory
        fields = ('title', 'url_title', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'url_title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }


class AdminSiteSettingModelForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = '__all__'
        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'site_name_title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'newletter_text': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'copyright': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'site_icon_circle': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput1'
            }),
            'site_icon': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput2'
            }),
            'about_us_image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput3'
            }),
            'products_count': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'shipping_amount': forms.NumberInput(attrs={
                'class': 'form-control mb-1',
                'id': 'id_amount_tomans'
            }),
            'customer_count': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'site_description': CKEditorWidget(),
            'why_pure_text': CKEditorWidget(),
            'is_main_setting': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
        }


class AdminSiteBannerModelForm(forms.ModelForm):
    class Meta:
        model = SiteBanner
        fields = ('title', 'position', 'image', 'url', 'is_active')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'position': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput2'
            }),
        }


class AdminSiteSocialModelForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = '__all__'
        widgets = {
            'telegram': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'instagram': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'youtube': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class AdminSiteTopProductModelForm(forms.ModelForm):
    class Meta:
        model = TopProduct
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            })
        }


class AdminSiteCategoryModelForm(forms.ModelForm):
    class Meta:
        model = SiteSettingCategory
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'short_description': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'product_category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'example-fileinput2'
            }),
        }


class AdminSiteFooterBoxModelForm(forms.ModelForm):
    class Meta:
        model = FooterLinkBox
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


class AdminSiteFooterLinkModelForm(forms.ModelForm):
    class Meta:
        model = FooterLink
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'url': forms.URLInput(attrs={
                'class': 'form-control'
            }),
            'footer_link_box': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class AdminOrderModelForm(forms.ModelForm):
    is_paid = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            # 'disabled': 'disabled',
            'class': 'form-control custom-control-input',
            'id': 'customControlValidation1',
        })
    )

    class Meta:
        model = Order
        fields = ('is_paid', 'payment_date', 'status')
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'payment_date': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }


class AdminWholesaleModelForm(forms.ModelForm):
    class Meta:
        model = Wholesale
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'landline_phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),
            'full_address': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'product': CKEditorWidget(),
            'statement': forms.NumberInput(attrs={
                'class': 'form-control mb-1',
                'id': 'inputTomans1',
            }),
            'total_amount_paid': forms.NumberInput(attrs={
                'class': 'form-control mb-1',
                'id': 'inputTomans2',
            }),
            'total_amount_payable': forms.NumberInput(attrs={
                'class': 'form-control mb-1',
                'id': 'inputTomans3',
            }),
            'order_date': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_status': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1',
            }),
        }


class AdminUserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date_joined': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'otp': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
            'last_login': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'password': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'groups': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'user_permissions': forms.SelectMultiple(attrs={
                'class': 'form-control'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1',
            }),
            'is_staff': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation2',
            }),
            'is_superuser': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation3',
            }),
        }


class AddUserAdminForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            RegexValidator(
                regex=r'^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,4}$',  # Email regex
                message='لطفا ایمیل را با فرمت صحیح وارد کنید.',
                code='invalid_email'
            )
        ],
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )

    def clean_phone_number(self):
        patterns = r'^09\d{9}$'
        phone_number = self.cleaned_data.get('phone_number')
        if re.match(patterns, phone_number):
            return phone_number
        raise ValidationError('لطفا شماره موبایل را با فرمت صحیح وارد کنید')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')


class LoginUserAdminForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'نام کاربری'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )


class AdminAddressModelForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
            }),
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'exact_address': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'plaque': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }


class ChangePasswordUserAdminForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'کلمه عبور فعلی'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'کلمه عبور جدید'
        }),
        validators=[
            RegexValidator(
                regex=r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{8,}$',
                message="کلمه عبور را با توجه به ملاحظات تکمیل کنید",
            ),
            validators.MaxLengthValidator(50)
        ],
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'تکرار کلمه عبور جدید'
        }),
        validators=[
            validators.MaxLengthValidator(50)
        ]
    )

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password == confirm_new_password:
            return confirm_new_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارد')


class AdminWalletModelForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
            }),
            'balance': forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'id': 'id_amount_tomans'
            })
        }


class AdminTransactionWalletModelForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'id': 'id_amount_tomans'
            }),
            'timestamp': forms.TextInput(attrs={
                'class': 'form-control',
            })
        }


class AdminWalletSettingModelForm(forms.ModelForm):
    class Meta:
        model = WalletSetting
        fields = '__all__'
        widgets = {
            'percentage_to_add': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'min_purchase': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'id_amount_tomans'
            })
        }


class AdminCouponModelForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
            }),
            'used_by': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customControlValidation1',
            })
        }

    def __init__(self, *args, **kwargs):
        super(AdminCouponModelForm, self).__init__(*args, **kwargs)
        self.fields['valid_to'] = JalaliDateField(widget=AdminJalaliDateWidget)
        self.fields['valid_from'] = JalaliDateField(widget=AdminJalaliDateWidget)
