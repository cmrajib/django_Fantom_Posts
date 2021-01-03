from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from .forms import PostCreationForm, PostUpdateForm, CreateCommentForm
from .models import Post, Category, Tag


class IndexView(ListView):
    template_name = "posts/index.html"
    model = Post
    context_object_name = 'posts'
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['slider_posts'] = Post.objects.all().filter(slider_post=True)
        return context

class PostDetail (DetailView, FormMixin):
    template_name = "posts/detail.html"
    model = Post
    context_object_name = 'single'
    form_class = CreateCommentForm


#If detail page is viewed, database model field called hit will increase
#This hit field is used to display most popular POST.
    def get(self, request, *args, **kwargs):
        self.hit = Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super(PostDetail, self).get(request, *args, **kwargs)

# By get_context_data value is passing to the template
# previous and next is for pagination
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['previous'] = Post.objects.filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next'] = Post.objects.filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        context['form'] = self.get_form()
        return context


    def form_valid(self, form):
        form.instance.post = self.object
        form.save()
        return super(PostDetail, self).form_valid(form)

    def post(self, *args, **kwaargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('detail', kwargs={"pk":self.object.pk, "slug":self.object.slug})

class CategoryDetail(ListView):
    model = Post
    template_name = 'categories/category_detail.html'
    context_object_name =  'post'

    def get_queryset(self):
        self.category = get_object_or_404(Category,pk=self.kwargs ['pk'])
        return Post.objects.filter(category=self.category).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        return context

class TagDetail(ListView):
    model = Post
    template_name = 'tags/tag_detail.html'
    context_object_name =  'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag,slug=self.kwargs ['slug'])
        return Post.objects.filter(tag=self.tag).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(TagDetail, self).get_context_data(**kwargs)
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        context['tag'] = self.tag
        return context


@method_decorator(login_required(login_url='users/login'),name="dispatch")
class CreatePostView(CreateView):
    template_name = 'posts/create-post.html'
    form_class =  PostCreationForm
    model = Post

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk,'slug':self.object.slug})


#user and tag are many to many relation, First save user then save tag
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()

#It is checking if it is exists in the database or not
# If new item then save
        tags = self.request.POST.get("tag").split(",")  #tag1, tag2, tag3

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)
        return super(CreatePostView, self).form_valid((form))


@method_decorator(login_required(login_url='users/login'),name="dispatch")
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail', kwargs={'pk':self.object.pk,'slug':self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.tag.clear()

        # It is checking if it is exists in the database or not
        # If new item then save
        tags = self.request.POST.get("tag").split(",")  # tag1, tag2, tag3

        for tag in tags:
            current_tag = Tag.objects.filter(slug=slugify(tag))
            if current_tag.count() < 1:
                create_tag = Tag.objects.create(title=tag)
                form.instance.tag.add(create_tag)
            else:
                existed_tag = Tag.objects.get(slug=slugify(tag))
                form.instance.tag.add(existed_tag)
        return super(UpdatePostView, self).form_valid((form))


    def get(self,request,*args,**kwargs):
        self.object = self.get_object()


# A user cannot update other user's post
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView, self).get(request,*args,**kwargs)


class DeletePostView(DeleteView):
    model = Post
    success_url= '/'
    template_name = 'posts/delete.html'

# One user cannot delete other user's post
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)
    def get(self,request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(DeletePostView, self).get(request, *args, **kwargs)


class SearchView(ListView):
    model = Post
    template_name = 'posts/search.html'
    paginate_by =3
    context_object_name = 'posts'

# q is the name of the search input field in right_side.html
    def get_queryset(self):
        query = self.request.GET.get('q')

        if query:
            return Post.objects.filter(Q(title__icontains=query)|
                                        Q(content__icontains=query)|
                                        Q(tag__title__icontains=query)
                                        ).order_by('id').distinct()

        return Post.objects.all().order_by('id')

