from rest_framework_csv.renderers import CSVRenderer


class CustomCSVRenderer(CSVRenderer):
    header = ['Rank', 'Player', 'Score']

    def render(self, data, media_type=None, renderer_context=None, writer_opts=None):
        if data is None:
            data = []
        else:
            data = [{'Rank': index + 1, 'Player': item['player'], 'Score': item['score']} for index, item in enumerate(data)]
            if not data:
                data = [{}]
        return super().render(data, media_type, renderer_context, writer_opts)
