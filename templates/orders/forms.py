from django import forms

class OrderCreateForm(forms.Form):
    DELIVERY_CHOICES = [("delivery", "Нужна доставка"), ("pickup", "Самовывоз")]
    PAYMENT_CHOICES  = [("card", "Оплата картой"), ("cod", "Наличными/картой при получении")]

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name  = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    email      = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    phone      = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "В формате: XXX-XXX-XX-XX"}))

    delivery_method = forms.ChoiceField(choices=DELIVERY_CHOICES, initial="delivery", widget=forms.RadioSelect(attrs={"class": "form-check-input"}))
    address = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 2}))
    city    = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

    payment_method  = forms.ChoiceField(choices=PAYMENT_CHOICES, initial="card", widget=forms.RadioSelect(attrs={"class": "form-check-input"}))

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("delivery_method") == "delivery" and not (cleaned.get("address") or "").strip():
            self.add_error("address", "Укажите адрес доставки.")
        return cleaned
