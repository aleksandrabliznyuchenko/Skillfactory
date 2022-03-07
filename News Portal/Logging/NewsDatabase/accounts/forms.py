from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from news.models import Account, Category


class CustomCategoryName(ModelMultipleChoiceField):
    def label_from_instance(self, category):
        return "%s" % category.name


class CategorySubscriptionForm(ModelForm):
    category = CustomCategoryName(queryset=Category.objects.all(),
                                  label='Категории',
                                  widget=CheckboxSelectMultiple)

    class Meta:
        model = Account
        fields = ['category']
