from rest_framework.pagination import PageNumberPagination


class SmallsetPagination(PageNumberPagination):
    page_size =2