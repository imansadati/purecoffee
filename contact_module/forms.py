from django import forms

from contact_module.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    use_required_attribute = False

    class Meta:
        model = ContactUs
        fields = ["full_name", "email", "title", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "نام خود را وارد کنید"}),
            "email": forms.EmailInput(attrs={"placeholder": "ایمیل را وارد کنید"}),
            "title": forms.TextInput(attrs={"placeholder": "موضوع را وارد کنید"}),
            "message": forms.Textarea(attrs={"placeholder": "پیام را وارد کنید"}),
        }

        error_messages = {
            "full_name": {
                "required": "وارد کردن نام و نام خانوادگی اجباری میباشد. لطفا وارد کنید"
            },
            "email": {"required": "وارد کردن ایمیل اجباری میباشد. لطفا وارد کنید"},
            "title": {"required": "وارد کردن موضوع اجباری میباشد. لطفا وارد کنید"},
            "message": {"required": "وارد کردن پیام اجباری میباشد. لطفا وارد کنید"},
        }
