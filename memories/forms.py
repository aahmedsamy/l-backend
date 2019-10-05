from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class MemoryForm(forms.ModelForm):
    title = forms.CharField(widget=EmojiPickerTextInputAdmin)
    body = forms.CharField(widget=EmojiPickerTextareaAdmin)


class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=EmojiPickerTextareaAdmin)
