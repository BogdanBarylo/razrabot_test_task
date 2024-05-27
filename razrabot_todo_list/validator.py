def get_validate_elem(title, description):
    errors = []
    if not title:
        errors.append('title обязателен')
        return errors
    if len(title) > 255:
        errors.append('title превышает 255 символов')
    if len(description) > 255:
        errors.append('description превышает 255 символов')
    return errors
