from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import BatchProcessForm

from .models import Question, Option


class QuestionBatchView(FormView):
    model = Question
    template_name = 'question/question_form.html'
    form_class = BatchProcessForm
    success_url = reverse_lazy('question_batch')
    success_message = "Questions were saved successfully"

    def form_valid(self, form):
        # Chama o método form_valid padrão e, em seguida, processa o arquivo Word
        response = super().form_valid(form)
        form.process_word_file()

        return response
