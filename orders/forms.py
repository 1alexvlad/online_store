from django import forms 
import re
from datetime import datetime


class CreateOrderForm(forms.Form):
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
            ],
        )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
            ],
        )

    card_number = forms.CharField(required=False, label='Номер карты')
    card_expiry = forms.CharField(required=False, label='Срок действия (MM/YY)')
    card_cvv = forms.CharField(required=False, label='CVC')

    
    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")
        if len(data) != 10:
            raise forms.ValidationError("Неверный формат номера")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        payment_on_get = cleaned_data.get('payment_on_get')
        
        if payment_on_get == '0':
            card_number = cleaned_data.get('card_number')
            card_expiry = cleaned_data.get('card_expiry')
            card_cvv = cleaned_data.get('card_cvv')
            
            if not card_number:
                self.add_error('card_number', 'Обязательное поле')
            elif not card_number.isdigit() or len(card_number) != 16:
                self.add_error('card_number', 'Неверный номер карты')
            
            if not card_expiry:
                self.add_error('card_expiry', 'Обязательное поле')
            else:
                try:
                    month, year = card_expiry.split('/')
                    exp_date = datetime.strptime(f'20{year}-{month}-01', '%Y-%m-%d')
                    if exp_date < datetime.now():
                        self.add_error('card_expiry', 'Срок действия карты истек')
                except:
                    self.add_error('card_expiry', 'Неверный формат (MM/YY)')
            
            if not card_cvv:
                self.add_error('card_cvv', 'Обязательное поле')
            elif not card_cvv.isdigit() or len(card_cvv) not in [3, 4]:
                self.add_error('card_cvv', 'Неверный CVV код')
        
        return cleaned_data
