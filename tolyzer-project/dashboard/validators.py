def validate_file_extension(value):
    print("hi")
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.gml', '.csv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only .gml and .csv files are allowed.')