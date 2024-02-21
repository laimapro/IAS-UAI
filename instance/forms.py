from django import forms

from question.models import Category, Question, Option
from .models import Instance, QuestionInstance
from docx import Document


class CreateInstanceForm(forms.ModelForm):
    title = forms.CharField()
    description = forms.Textarea()
    word_file = forms.FileField()

    class Meta:
        model = Instance
        fields = ['title', 'description', 'word_file']

    def process_word_file(self):
        word_file = self.cleaned_data['word_file']
        # print('INSTANCE ID: ', self.instance.id)
        document = Document(word_file)

        current_category = None
        current_question = None
        new_option = None

        for paragraph in document.paragraphs:
            if paragraph.text.startswith('Category:'):
                # Nova pergunta encontrada
                category_text = paragraph.text.replace('Category:', '').strip()
                categories = Category.objects.filter(title=category_text)
                if categories.exists():
                    current_category = categories.first()
                else:
                    current_category = Category.objects.create(title=category_text)
            elif paragraph.text.startswith('Question:'):
                # Nova pergunta encontrada
                question_text = paragraph.text.replace('Question:', '').strip()
                questions = Question.objects.filter(title=question_text)
                if questions.exists():
                    current_question = questions.first()
                else:
                    current_question = Question.objects.create(category=current_category, title=question_text)
                question_instance = QuestionInstance.objects.create(question_pj=current_question, instance_pj=self.instance)
            elif paragraph.text.startswith('Option:'):
                correct = False
                option_text = paragraph.text.replace('Option:', '').strip()
                feedback = 'None'
                # print("Opção:", option_text)
                if '[c]' in option_text.lower():
                    option_text = option_text.replace('[c]', '').strip()
                    correct = True
                    # print("Opção correta:", correct)
                opt = Option.objects.filter(text=option_text, question=current_question)
                if not opt.exists():
                    new_option = Option.objects.create(question=current_question, text=option_text, feedback=feedback,
                                                       correct=correct)
                else:
                    new_option = opt.first()
                    new_option.feedback = feedback
                    new_option.correct = correct
                    new_option.save()

            elif paragraph.text.startswith('Feedback:'):
                feedback = paragraph.text.replace('Feedback:', '').strip()
                if new_option is not None:
                    new_option.feedback = feedback
                    new_option.save()
