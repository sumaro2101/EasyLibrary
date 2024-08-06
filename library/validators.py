from rest_framework.validators import ValidationError
from rest_framework.serializers import ModelSerializer

from django.db.models import Q

from typing import Any, List, Union, Dict, Tuple

from datetime import date

from library.models import Volume, Book


def get_value(field: str,
              attrs: Dict,
              serializer: ModelSerializer,
              ) -> Any:
    """Функция выполняющая получение значения
    исходя из того что - пользователь желает изменить поле 
    или пользователь просто не указал его
    """
    try:
        value = attrs[field]
    except KeyError:
        if serializer.instance:
            instance = serializer.instance
            field = instance._meta.get_field(field)
            value = field.value_from_object(instance)
        else:
            field = instance.model._meta.get_field(field)
            if field.has_default():
                value = field.default
            else:
                value = None

    return value


def tigger_to_check(attrs: Dict,
                    *fields: List,
                    ) -> bool:
    """Тригер если проверка нужна
    """
    need_check = False
    for field in fields:
        if field in attrs:
            need_check = True
    return need_check


class YearValidator:
    """Валидатор года
    """
    requires_context = True

    def __init__(self,
                 year: str,
                 published: str,
                 ) -> None:
        if not isinstance(year, str):
            raise TypeError(f'{year}, должен быть именем поля (str)')
        if not isinstance(published, str):
            raise TypeError(f'{published}, должен быть именем поля (str)')
        self.year = year
        self.published = published

    def _check_valid_year(self, year: int, published: bool) -> None:
        """Проверка валидного значения года исходя из публикации
        """
        match published:
            case True:
                if not 1456 < year < date.today().year:
                    raise ValidationError({'year':
                        'Значение год не может быть меньше "1456"\
                            или больше текущего года'})
            case False:
                if not 1456 < year:
                    raise ValidationError({'year':
                        'Значение год не может быть меньше "1456"'})

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(attrs, self.year, self.published)
        if need_check:
            year = get_value(self.year, attrs, serializer)
            published = get_value(self.published, attrs, serializer)
            self._check_valid_year(year, published)


class VolumeValidator:
    """Валидатор тома
    """
    requires_context = True

    def __init__(self,
                 volume: str,
                 num_of_volume: str,
                 ) -> None:
        if not isinstance(volume, str):
            raise TypeError(f'{volume}, должен быть именем поля (str)')
        if not isinstance(num_of_volume, str):
            raise TypeError(f'{num_of_volume}, должен быть именем поля (str)')
        self.volume = volume
        self.num_of_volume = num_of_volume

    def _check_values_volume(self,
                             volume: Union[Volume, None],
                             num_of_volume: Union[int, None],
                             ) -> None:
        """Проверка значений в томе и номере
        """
        if volume and not num_of_volume:
            raise ValidationError(
                {'num_of_volume': 'Неоходимо указать номер книги\
                    из тома, либо номер не может быть нулем',
                    }
            )
        if volume is None and num_of_volume:
            raise ValidationError(
                {'volume': 'Неоходимо указать к какому тому\
                    принадлежит книга если указан номер в томе',
                    }
            )

    def _check_dublicate_number_of_volume(self,
                                          volume: Union[Volume, None],
                                          num_of_volume: Union[int, None],
                                          ) -> None:
        """Проверка уникальности номера в томе
        """
        if volume:
            volume = Book.objects.filter(Q(volume=volume) &
                                         Q(num_of_volume=num_of_volume))
            if volume.exists():
                raise ValidationError(
                    {'num_of_volume': 'В данном томе уже присутсвует\
                        книга с таким номером',
                        }
                )

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(attrs, self.volume, self.num_of_volume)
        if need_check:
            volume = get_value(self.volume, attrs, serializer)
            num_of_volume = get_value(self.num_of_volume, attrs, serializer)
            self._check_values_volume(volume, num_of_volume)
            self._check_dublicate_number_of_volume(volume, num_of_volume)


class PublishedValidator:
    """Валидатор значений исходя из публикации книги
    """
    requires_context = True

    def __init__(self,
                 best_seller: str,
                 circulation: str,
                 is_published: str,
                 ) -> None:
        if not isinstance(best_seller, str):
            TypeError(f'{best_seller}, должен быть строкой')
        if not isinstance(circulation, str):
            TypeError(f'{circulation}, должен быть строкой')
        if not isinstance(is_published, str):
            TypeError(f'{is_published}, должен быть строкой')
        self.best_seller = best_seller
        self.circulation = circulation
        self.is_published = is_published

    def _check_status_depens_on_published(self,
                                          best_seller: bool,
                                          circulation: Union[int, None],
                                          is_published: bool) -> None:
        """Проверка значений в завимости от публикации
        """
        match is_published:
            case True:
                if not circulation:
                    raise ValidationError(
                        {'circulation':
                            'Опубликованная книга не может быть без тиража',
                            }
                    )
            case False:
                if circulation or best_seller:
                    raise ValidationError(
                        {'circulation, best_seller':
                            'Книга которая не была опубликована\
                                не может быть лидером продаж\
                                    или иметь тираж',
                                    }
                    )

    def __call__(self, attrs, serializer) -> Any:
        need_check = tigger_to_check(
            attrs,
            self.best_seller,
            self.circulation,
            self.is_published,
        )
        if need_check:
            bs = get_value(self.best_seller, attrs, serializer)
            circ = get_value(self.circulation, attrs, serializer)
            publish = get_value(self.is_published, attrs, serializer)
            self._check_status_depens_on_published(bs, circ, publish)
