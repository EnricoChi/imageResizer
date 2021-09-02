from progress.bar import FillingCirclesBar


class ProgressBar(FillingCirclesBar):
    suffix = '%(index)d/%(max)d'
    color = 'yellow'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        folder = args[0]
        self.message = f'Processing "{folder}"'
