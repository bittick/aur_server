from rest_framework.pagination import PageNumberPagination, _get_page_links
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.response import Response


class CarAdPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    @staticmethod
    def _get_displayed_page_numbers(current, final):
        assert current >= 1
        assert final >= current

        if final <= 8:
            return list(range(1, final + 1))

        # Check for gap between 1 and the rest of the sequence
        if current >= 6:
            included = {1, None, current - 2, current - 1, current, current + 1, current + 2, current + 3, current + 4,
                        final}
        else:
            included = {i for i in range(1, 9)}
            included.update([current + i for i in range(-2, 5) if 0 < current + i <= final])
            included.add(final)

        # Now sort the page numbers and drop anything outside the limits.
        included = [
            idx for idx in sorted(included)
            if 0 < idx <= final
        ]

        # Finally insert any `...` breaks
        if current > 3:
            included.insert(1, None)
        if current < final - 4:
            included.insert(len(included) - 1, None)
        return included

    def get_html_context(self):
        base_url = self.request.build_absolute_uri()

        def page_number_to_url(page_number):
            if page_number == 1:
                return remove_query_param(base_url, self.page_query_param)
            else:
                return replace_query_param(base_url, self.page_query_param, page_number)

        current = self.page.number
        final = self.page.paginator.num_pages
        page_numbers = self._get_displayed_page_numbers(current, final)
        page_links = _get_page_links(page_numbers, current, page_number_to_url)
        return {
            'previous_url': self.get_previous_link(),
            'next_url': self.get_next_link(),
            'page_links': page_links
        }

    def get_paginated_response(self, data):
        return Response({
            'page_count': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'pages_data': self.get_html_context(),
            'results': data

        })
