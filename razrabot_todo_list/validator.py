def get_validate_elem(title, description):
    errors = []
    if len(title) > 255:
        errors.append(f'{title} превышает 255 символов')
    if len(description) > 255:
        errors.append(f'{description} превышает 255 символов')
    if not title:
        errors.append('title обязателен')
    return errors