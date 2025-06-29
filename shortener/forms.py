from django import forms
import re


class ShortURLForm(forms.Form):
    original_url = forms.URLField(
        label='原網址',
        required=True,
        widget=forms.URLInput(attrs={
            'class': 'w-96 py-3 px-4 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3c2f80] bg-white text-[#1d1d4a]',
            'id': 'id_original_url',
            'placeholder': '請輸入要縮短的網址...'
        })
    )
    
    password = forms.CharField(
        label='密碼（非必填）',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-60 py-3 px-4 pr-10 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3c2f80] bg-white text-[#1d1d4a]',
            'pattern': r'\d{8}',
            'inputmode': 'numeric',
            'maxlength': '8',
            'placeholder': '密碼需為 8 位數字',
            'id': 'id_password',
            'type': 'password',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'  # 前端即時過濾非數字
        })
    )
    
    def clean_password(self):
        """自定義密碼驗證"""
        password = self.cleaned_data.get('password')
        
        # 如果密碼為空，直接返回（因為是非必填）
        if not password:
            return password
        
        # 移除所有非數字字符（額外保護）
        password = re.sub(r'[^0-9]', '', password)
        
        # 檢查是否只包含數字
        if not re.match(r'^\d+$', password):
            raise forms.ValidationError('密碼只能包含數字')
        
        # 檢查是否為 8 位數
        if len(password) != 8:
            raise forms.ValidationError('密碼必須是 8 位數字')
        
        return password
    
    def clean_original_url(self):
        """自定義 URL 驗證（可選）"""
        original_url = self.cleaned_data.get('original_url')
        
        if original_url:
            # 確保 URL 包含協議
            if not original_url.startswith(('http://', 'https://')):
                original_url = 'https://' + original_url
        
        return original_url