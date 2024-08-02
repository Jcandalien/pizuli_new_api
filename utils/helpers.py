from typing import Type, TypeVar
from tortoise.models import Model
from utils.exceptions import NotFoundError, BadRequestError
from tortoise.exceptions import IntegrityError

T = TypeVar('T', bound=Model)

async def create_object(model: Type[T], **kwargs) -> T:
    """
    Create a new object of the given model.

    Args:
        model: The Tortoise ORM model class
        **kwargs: The fields and values for the new object

    Returns:
        The created object

    Raises:
        BadRequestError: If there's an integrity error (e.g., unique constraint violation)
    """
    try:
        obj = await model.create(**kwargs)
        return obj
    except IntegrityError as e:
        raise BadRequestError(f"Could not create {model.__name__}: {str(e)}")

async def update_object(obj: Model, **kwargs) -> Model:
    """
    Update an existing object with the given fields.

    Args:
        obj: The existing object to update
        **kwargs: The fields and new values to update

    Returns:
        The updated object

    Raises:
        BadRequestError: If there's an integrity error during the update
    """
    try:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await obj.save()
        return obj
    except IntegrityError as e:
        raise BadRequestError(f"Could not update {obj.__class__.__name__}: {str(e)}")

async def delete_object(obj: Model) -> None:
    """
    Delete the given object.

    Args:
        obj: The object to delete

    Raises:
        BadRequestError: If there's an error during deletion
    """
    try:
        await obj.delete()
    except Exception as e:
        raise BadRequestError(f"Could not delete {obj.__class__.__name__}: {str(e)}")

async def get_object_or_404(model: Type[T], **kwargs) -> T:
    """
    Get an object of the given model or raise a 404 error.

    Args:
        model: The Tortoise ORM model class
        **kwargs: The fields to filter by

    Returns:
        The found object

    Raises:
        NotFoundError: If the object is not found
    """
    obj = await model.get_or_none(**kwargs)
    if not obj:
        raise NotFoundError(f"{model.__name__} not found")
    return obj