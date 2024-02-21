import random

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from project.models import Project
from question.models import Question, Option
from .models import Instance, InstanceAttempt, QuestionInstance, InstanceAttemptAnswer
from .forms import CreateInstanceForm
import random


class CreateInstanceView(CreateView):
    model = Instance
    form_class = CreateInstanceForm

    # success_url = reverse_lazy('login')

    def form_valid(self, form):
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(id=project_id)

        instance = form.instance
        instance.instance_project = project
        word_file = form.cleaned_data.get('word_file')

        if word_file:
            print('Arquivo Word encontrado: ', word_file)
            # print('Instance: ', instance.id)
            instance.save()
            form.process_word_file()
            messages.success(self.request, _('Instance created successfully'))
            return HttpResponseRedirect(self.get_success_url())
        else:
            print('Arquivo Word não encontrado. Operação cancelada.')
            messages.error(self.request, _('Word file not found. Operation cancelled'))
            return self.form_invalid(form)

    def get_success_url(self):
        pj = self.kwargs.get('project_id')
        return reverse_lazy('pj_detail', args=(pj,))


class SurveyStartView(TemplateView):
    template_name = 'survey_start.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance_id = kwargs['instance_id']
        instance = Instance.objects.get(id=instance_id)
        context['instance'] = instance
        attempt_exists = InstanceAttempt.objects.filter(user_id=self.request.user.participant,
                                                        instance_id=instance).first()
        if attempt_exists:
            context['attempt'] = attempt_exists
        return context

    def post(self, request, *args, **kwargs):
        # Crie uma nova instância de tentativa de pesquisa ao iniciar
        # print('kwargs: ', kwargs)
        instance = Instance.objects.get(id=kwargs['instance_id'])
        instance_attempt = InstanceAttempt.objects.create(user_id=request.user.participant, instance_id=instance)
        return redirect(reverse_lazy('survey_question', kwargs={'attempt_id': instance_attempt.id, 'q': 0}))


class SurveyQuestionView(TemplateView):
    template_name = 'survey_question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempt_id = kwargs['attempt_id']
        instance_attempt = InstanceAttempt.objects.get(id=attempt_id)
        question_instances = QuestionInstance.objects.filter(instance_pj=instance_attempt.instance_id)
        current_question_index = kwargs['q']

        # print(question_instances)
        # print(kwargs)

        if current_question_index < question_instances.count():
            is_correct = False
            likert_scale = 1
            question_id = question_instances[current_question_index].question_pj.id
            iaas = InstanceAttemptAnswer.objects.filter(question_id=question_id, instance_attempt_id=instance_attempt)
            options = []
            for i in iaas:
                options.append(i.option_id)
                # print(f'R: {i.option_id.text} - {i.option_id.correct}')
                if i.option_id.correct:
                    is_correct = True
                    likert_scale = i.likert_scale

            question_options = list(question_instances[current_question_index].question_pj.options.all())
            random.shuffle(question_options)

            context['respondidas'] = options
            context['attempt_id'] = attempt_id
            context['is_correct'] = is_correct
            context['likert_scale'] = likert_scale
            context['question_instance'] = question_instances[current_question_index]
            context['question_options'] = question_options
            context['current_question_index'] = current_question_index
            context['next_question_index'] = current_question_index + 1
            context['total_questions'] = question_instances.count()
        return context

    def post(self, request, *args, **kwargs):
        attempt_id = kwargs['attempt_id']
        instance_attempt = InstanceAttempt.objects.get(id=attempt_id)
        question_id = request.POST.get('question_id')
        option_id = request.POST.get('option_id')
        likert_scale = request.POST.get('likert_scale')
        finish_survey = request.POST.get('finish_survey')
        question = Question.objects.get(id=question_id)

        current_question_index = int(request.POST.get('current_question_index', 0))
        question_instances = QuestionInstance.objects.filter(instance_pj=instance_attempt.instance_id)
        next_question_index = current_question_index + 1

        instance_attempt_answer_obj = InstanceAttemptAnswer.objects.filter(question_id=question_id,
                                                                           instance_attempt_id=instance_attempt).last()

        if likert_scale:
            # print('Atualizar questão com likert scale')
            print('Likert Value: ', likert_scale)

            instance_attempt_answer = InstanceAttemptAnswer.objects.get(id=instance_attempt_answer_obj.pk)
            instance_attempt_answer.likert_scale = likert_scale

            instance_attempt_answer.save()

            messages.success(self.request, _('Thank you for rating our question correct'))

            if next_question_index >= question_instances.count():
                messages.success(self.request, 'Parabéns! Você concluiu a pesquisa, pressione o botão Finalizar, '
                                               'para que sua pesquisa seja válida.')

            return redirect(
                reverse_lazy('survey_question',
                             kwargs={'attempt_id': instance_attempt.id, 'q': current_question_index}))
        elif finish_survey:
            print('Finished survey: ', finish_survey)
            instance_attempt_obj = InstanceAttempt.objects.get(id=finish_survey)
            print('Attempt: ', instance_attempt_obj)
            instance_attempt_obj.status_attempt = 1

            instance_attempt_obj.save()

            return redirect(reverse_lazy('survey_finished'))
        else:
            option = Option.objects.get(id=option_id)
            attempt_number = 1
            if instance_attempt_answer_obj:
                attempt_number = int(instance_attempt_answer_obj.attempt_number)+1
            if question_id and option_id:
                instance_attempt_answer_created = InstanceAttemptAnswer.objects.create(
                    question_id=question,
                    option_id=option,
                    instance_attempt_id=instance_attempt,
                    likert_scale=likert_scale,
                    attempt_number=attempt_number
                )

                if instance_attempt_answer_created:
                    messages.success(self.request, instance_attempt_answer_created.option_id.feedback)
            else:
                print('Escolha uma das opções')

            if next_question_index < question_instances.count():
                return redirect(
                    reverse_lazy('survey_question',
                                 kwargs={'attempt_id': instance_attempt.id, 'q': current_question_index}))
            else:
                return redirect(
                    reverse_lazy('survey_question',
                                 kwargs={'attempt_id': instance_attempt.id, 'q': current_question_index}))


class SurveyFinishedView(TemplateView):
    template_name = 'survey_finished.html'
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     instance_id = kwargs['instance_id']
    #     instance = Instance.objects.get(id=instance_id)
    #     context['instance'] = instance
    #     attempt_exists = InstanceAttempt.objects.filter(user_id=self.request.user.participant,
    #     instance_id=instance).first()
    #     if attempt_exists:
    #         context['attempt'] = attempt_exists
    #     return context
