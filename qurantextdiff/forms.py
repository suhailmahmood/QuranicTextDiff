from haystack.forms import SearchForm


class QuranDiacriticSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
