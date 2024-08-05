from rest_framework.validators import ValidationError

from typing import Any, List, Union, Dict, Tuple

from datetime import date


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
        year = attrs.get(self.year)
        published = attrs.get(self.published)
        if year is None:
            year = serializer.instance.year_published
        if published is None:
            published = serializer.instance.is_published
        self._check_valid_year(year, published)


class VolumeValidator:
    """Валидатор тома
    """
    def __init__(self,
                 fields: List[str],
                 ) -> None:
        if not isinstance(fields, list):
            raise TypeError(
                'Поле "fields" должно было List',
                )
        if len(fields) != 2:
            raise KeyError(
                'Неоходимо указать два значения для проверки',
                )
        for field in fields:
            if not isinstance(field, str):
                raise TypeError(
                    'Аргумент "field" может быть только строкой',
                    )
        self.fields = fields

    def __call__(self, attrs) -> Any:
        checked_values = [
                value
                for field, value
                in attrs.items()
                if field == self.field
                and value is not None
            ]


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
        bs = attrs.get(self.best_seller)
        circ = attrs.get(self.circulation)
        publish = attrs.get(self.is_published)
        if bs is None:
            bs = serializer.instance.best_seller
        if circ is None:
            circ = serializer.instance.circulation
        if publish is None:
            publish = serializer.instance.is_published

        self._check_status_depens_on_published(bs, circ, publish)
