from django.shortcuts import render, redirect, reverse
from .models import Filme, Usuario
from .forms import CriarContaForm, FormHomePage
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
# def homepage(request):
#     return render(request, 'homepage.html')


class Homepage(FormView):
    template_name = 'homepage.html'
    form_class = FormHomePage

    def get_success_url(self):
        email = self.request.POST.get('email')
        usuario = Usuario.objects.filter(email=email)
        if usuario:
            return reverse('filme:login')
        else:
            return reverse('filme:criarconta')

    def get(self, request, *args, **Kwargs):
        if request.user.is_authenticated:#usuario == logado:
            return redirect('filme:homefilme')#redirecionar para a pagina home filme

        else:
            return super().get(request, *args, **Kwargs)



# def homefilmes(request):
#     context = {}
#     lista_filmes = Filme.objects.all()
#     context['lista_filmes'] = lista_filmes
#     return render(request, 'homepage_filme.html', context)

class Homefilmes(LoginRequiredMixin, ListView):
    template_name = 'homepage_filme.html'
    model = Filme
    #Vai retorna um object_list


class Detalhesfilme(LoginRequiredMixin, DetailView):
    template_name = 'detalhesfilme.html'
    model = Filme
    #retorna object

    def get(self, request, *args, **Kwargs):
        filme = self.get_object()
        filme.visualizacao += 1
        filme.save()

        usuario = request.user
        usuario.filme_vistos.add(filme)

        return super().get(request, *args, **Kwargs)



    def get_context_data(self, **kwargs):
        context = super(Detalhesfilme, self).get_context_data(**kwargs)
        filmes_relacionados = Filme.objects.filter(categoria=self.get_object().categoria)[0:5]
        #ele vai pegar todos os meus objetos(filmes/series) e pegar so a categoria
        context['filmes_relacionados'] = filmes_relacionados
        return context


class Pesquisafilme(LoginRequiredMixin,  ListView):
    template_name = 'pesquisa.html'
    model = Filme
    #object_list

    def get_queryset(self):
        termo_pesquisa = self.request.GET.get('query')
        if termo_pesquisa:
            object_list = Filme.objects.filter(titulo__icontains=termo_pesquisa)
            return object_list
        else:
            return None

class Paginaperfil(LoginRequiredMixin, UpdateView):
    template_name = 'editarperfil.html'
    model = Usuario
    fields = ['first_name', 'last_name', 'email']
    def get_success_url(self):
        return reverse('filme:homefilme')

class Criarconta(FormView):
    template_name = 'criarconta.html'
    form_class = CriarContaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('filme:login')

