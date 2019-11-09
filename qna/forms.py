from django.forms import CharField, ModelForm, ValidationError, TextInput

from .models import Question, Answer


class TagsField(CharField):
    def to_python(self, value):
        tags = [el.strip() for el in value.split(",")]
        if len(tags) > 3:
            raise ValidationError("You can add a maximum of 3 tags.")
        return tags


class AskForm(ModelForm):
    tags = TagsField(max_length=200,
                     widget=TextInput(attrs={
                         "placeholder": "tag1, tag2, tag3"
                     }))

    class Meta:
        model = Question
        fields = ("title", "text")


class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ("text",)
        labels = {
            "text": ""
        }
