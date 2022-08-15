from django import forms


class SuggestWidget(forms.SelectMultiple):
    template_name = 'accounts/widgets/suggest.html'

    class Media:
        js = ('accounts/js/suggest.js',)
        css = {
            'all': ('accounts/css/suggest.css',)
        }

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' suggest'
        else:
            self.attrs['class'] = 'suggest'
