from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from .models import *
from .forms import AddReviewForm, UpdateReviewForm, ShoesForm, FilterForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Shoes, User


# Create your views here.


class CategoryProductsListView(View):
    def get(self, request):
        categories = CategoryProducts.objects.all()
        return render(request, 'products/category_products.html', {'categories': categories})


class ShoesListView(View):
    def get(self, request, category_id):
        category = get_object_or_404(CategoryProducts, pk=category_id)
        shoes = Shoes.objects.filter(category=category)
        return render(request, 'products/shoes.html', {'shoes': shoes})


class ShoesListView1(ListView):
    model = Shoes
    template_name = 'products/shoes_list.html'
    context_object_name = 'shoes'


class ShoesDetailView(View):
    def get(self, request, pk):
        shoe = get_object_or_404(Shoes, pk=pk)
        reviews = Review.objects.filter(shoe=shoe)
        # return render(request, 'products/shoe_detail.html', {'shoe': shoe, 'reviews': reviews})
        recommended_shoes = Shoes.objects.filter(
            category=shoe.category,
            type=shoe.type,
            size=shoe.size
        ).exclude(pk=pk)[:5]
        return render(request, 'products/shoe_detail.html', {
            'shoe': shoe,
            'reviews': reviews,
            'recommended_shoes': recommended_shoes
        })


class CreateShoeView(View):
    def get(self, request):
        form = ShoesForm()
        return render(request, 'createshoe.html', {'form': form})

    def post(self, request):
        form = ShoesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products:all_shoes')
        return render(request, 'createshoe.html', {'form': form})


class ShoesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shoes
    form_class = ShoesForm
    template_name = 'products/shoes_form.html'

    def test_func(self):
        shoe = self.get_object()
        return self.request.user == shoe.owner or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to update this shoe.")
        return redirect('shoes_detail', pk=self.get_object().pk)

    def get_success_url(self):
        messages.success(self.request, "Shoe updated successfully!")
        return reverse('shoes_detail', kwargs={'pk': self.object.pk})


class ShoesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Shoes
    template_name = 'products/shoes_confirm_delete.html'
    success_url = reverse_lazy('shoes_list')

    def test_func(self):
        shoe = self.get_object()
        return self.request.user == shoe.owner or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "You do not have permission to delete this shoe.")
        return redirect('shoes_detail', pk=self.get_object().pk)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Shoe deleted successfully!")
        return super().delete(request, *args, **kwargs)


class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        shoe = get_object_or_404(Shoes, pk=pk)
        add_review_form = AddReviewForm()
        return render(request, 'products/add_review.html', {'shoe': shoe, 'add_review_form': add_review_form})

    def post(self, request, pk):
        shoe = get_object_or_404(Shoes, pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = add_review_form.save(commit=False)
            review.shoe = shoe
            review.user = request.user
            review.save()
            messages.success(request, "Your review was added successfully!")
            return redirect('products:shoe_detail', pk=pk)
        else:
            messages.error(request, "Failed to add your review.")
            return render(request, 'products/add_review.html', {'shoe': shoe, 'add_review_form': add_review_form})


class ReviewDeleteView(View):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        shoe_pk = review.shoe.pk
        if review.user == request.user or request.user.is_staff:
            review.delete()
            messages.success(request, "Your review was deleted successfully!")
        else:
            messages.error(request, "You do not have permission to delete this review.")
        return redirect('products:shoe_detail', pk=shoe_pk)


class ReviewUpdateView(View):
    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to update this review.")
            return redirect('products:shoe_detail', pk=review.shoe.pk)
        update_form = UpdateReviewForm(instance=review)
        return render(request, 'products/update_review.html', {'form': update_form})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user and not request.user.is_staff:
            messages.error(request, "You do not have permission to update this review.")
            return redirect('products:shoe_detail', pk=review.shoe.pk)
        update_form = UpdateReviewForm(request.POST, instance=review)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, "Your review was updated successfully!")
            return redirect('products:shoe_detail', pk=review.shoe.pk)
        else:
            messages.error(request, "Failed to update your review.")
            return render(request, 'products/update_review.html', {'form': update_form})


class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        shoes_results = Shoes.objects.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(type__name__icontains=query) |
            Q(size__name__icontains=query)
        )
        users_results = User.objects.filter(username__icontains=query)
        return render(request, 'products/search_results.html', {
            'query': query,
            'shoes_results': shoes_results,
            'users_results': users_results,
        })


class FilterView(View):
    def get(self, request):
        filter_form = FilterForm(request.GET)
        if filter_form.is_valid():
            filtered_shoes = self.get_filtered_shoes(filter_form.cleaned_data)
            return render(request, 'products/filter_results.html', {'shoes': filtered_shoes})
        else:
            return render(request, 'products/filter.html', {'filter_form': filter_form})

    def get_filtered_shoes(self, filter_data):
        category = filter_data.get('category')
        size = filter_data.get('size')
        type = filter_data.get('type')
        color = filter_data.get('color')
        made_company = filter_data.get('made_company')
        made_country = filter_data.get('made_country')
        lather = filter_data.get('lather')
        season = filter_data.get('season')
        price_min = filter_data.get('price_min')
        price_max = filter_data.get('price_max')

        filtered_shoes = Shoes.objects.all()
        if category:
            filtered_shoes = filtered_shoes.filter(category=category)
        if size:
            filtered_shoes = filtered_shoes.filter(size=size)
        if type:
            filtered_shoes = filtered_shoes.filter(type=type)
        if color:
            filtered_shoes = filtered_shoes.filter(color=color)
        if made_company:
            filtered_shoes = filtered_shoes.filter(made_company=made_company)
        if made_country:
            filtered_shoes = filtered_shoes.filter(made_country=made_country)
        if lather:
            filtered_shoes = filtered_shoes.filter(lather=lather)
        if season:
            filtered_shoes = filtered_shoes.filter(season=season)
        if price_min:
            filtered_shoes = filtered_shoes.filter(price__gte=price_min)
        if price_max:
            filtered_shoes = filtered_shoes.filter(price__lte=price_max)

        return filtered_shoes
