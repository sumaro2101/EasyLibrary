from rest_framework.pagination import PageNumberPagination


class BasePaginate(PageNumberPagination):
    """Постраничный базовый вывод (10 объектов)
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 25


class PaginageVolumes(PageNumberPagination):
    """Постраничный вывод томов
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class PaginagePublishers(PageNumberPagination):
    """Постраничный вывод издателей
    """
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 30


class PaginageGenres(PageNumberPagination):
    """Постраничный вывод Жанров
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 40


class PaginateExtensions(PageNumberPagination):
    """Постраничный вывод заявок
    """
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 10
