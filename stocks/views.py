from django.shortcuts import render, reverse
from django.views import generic
from .models import StockQuote
from chartjs.views.lines import BaseLineChartView
from .stock_class import StockProfile, get_historical_price, get_historical_cash_flow


price_data = [[], []]
fcf_data = [[], []]
symbol = ""


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'stocks/index.html'
    context_object_name = 'latest_stocks_list'

    def get_queryset(self):
        """Return the last five searched tickers"""
        return StockQuote.objects.order_by('-access_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'stocks/detail.html'
    context_object_name = 'stock_details'

    def get_object(self):
        return None

    def get_queryset(self):
        return None


def search_price(request):
    global price_data, symbol

    data = request.GET.copy()
    symbol = data.get('txt_ticker')

    price_data = get_historical_price(symbol, 30)
    try:
        profile = StockProfile(symbol)
        context = {'profile': profile}
    except(KeyError, ValueError) as e:
        return render(request, 'stocks/index.html', {
            'error_message': "Symbol doesn't exist",
        })
    else:
        return render(request, 'stocks/detail.html', context)


def search_cashflow(request):
    global fcf_data

    fcf_data = get_historical_cash_flow(symbol)
    return render(request, 'stocks/cash_flow.html')


class PriceChartView(BaseLineChartView):
    template_name = 'stocks/detail.html'

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return price_data[1]

    def get_providers(self):
        """Return names of datasets."""
        return ["Cost (usd)"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [price_data[0]]


class FCFPSChartView(BaseLineChartView):
    template_name = 'cash_flow/cash_flow.html'

    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return fcf_data[1]

    def get_providers(self):
        """Return names of datasets."""
        return ["Free Cash Per Share"]

    def get_data(self):
        """Return 3 datasets to plot."""
        return [fcf_data[0]]
