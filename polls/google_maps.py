import gmaps, geopy
from ipywidgets.embed import embed_minimal_html
import ipywidgets as widgets
from IPython.display import display
API_KEY = 'AIzaSyBqmaSMESUuaWht383WqtEtLDyGff5GrKs'
gmaps.configure(api_key=API_KEY)
class ReverseGeocoder(object):
    """
    Jupyter widget for finding addresses.

    The user places markers on a map. For each marker,
    we use `geopy` to find the nearest address to that
    marker, and write that address in a text box.
    """

    def __init__(self):
        self._figure = gmaps.figure()
        self._drawing = gmaps.drawing_layer()
        self._drawing.on_new_feature(self._new_feature_callback)
        self._figure.add_layer(self._drawing)
        self._address_box = widgets.Text(
            description='Address: ',
            disabled=True,
            layout={'width': '95%', 'margin': '10px 0 0 0'}
        )
        self._geocoder = geopy.geocoders.GoogleV3(api_key=API_KEY)
        self._container = widgets.VBox([self._figure, self._address_box])

    def _get_location_details(self, location):
        return self._geocoder.reverse(location, exactly_one=True)

    def _clear_address_box(self):
        self._address_box.value = ''

    def _show_address(self, location):
        location_details = self._get_location_details(location)
        if location_details is None:
            self._address_box.value = 'No address found'
        else:
            self._address_box.value = location_details.address

    def _new_feature_callback(self, feature):
        try:
            location = feature.location
        except AttributeError:
            return  # Not a marker

        # Clear address box to signify to the user that something is happening
        self._clear_address_box()

        # Remove all markers other than the one that has just been added.
        self._drawing.features = [feature]

        # Compute the address and display it
        self._show_address(location)

    def google_map(seld):
        from gmaps.datasets import load_dataset_as_df
        df_earth = load_dataset_as_df('earthquakes')
        # print(df_earth.head())

        locations = df_earth[['latitude', 'longitude']]
        weights = df_earth['magnitude']
        fig = gmaps.figure()
        fig.add_layer(gmaps.heatmap_layer(locations, weights=weights))
        embed_minimal_html('jordan_map.html', views=[fig])
        return fig

    def render(self):
        return self._container


class AcledExplorer(object):
    """
    Jupyter widget for exploring the ACLED dataset.

    The user uses the slider to choose a year. This renders
    a heatmap of civilian victims in that year.
    """

    def __init__(self, df):
        self._df = df
        self._heatmap = None
        self._slider = None
        initial_year = min(self._df['year'])

        title_widget = widgets.HTML(
            '<h3>Civilian casualties in Africa, by year</h3>'
            '<h4>Data from <a href="https://www.acleddata.com/">ACLED project</a></h4>'
        )

        map_figure = self._render_map(initial_year)
        controls = self._render_controls(initial_year)
        self._container = widgets.VBox([title_widget, controls, map_figure])

    def render(self):
        display(self._container)

    def _on_year_change(self, change):
        year = self._slider.value
        self._heatmap.locations = self._locations_for_year(year)
        self._total_box.value = self._total_casualties_text_for_year(year)
        return self._container

    def _render_map(self, initial_year):
        fig = gmaps.figure(map_type='HYBRID')
        self._heatmap = gmaps.heatmap_layer(
            self._locations_for_year(initial_year),
            max_intensity=100,
            point_radius=8
        )
        fig.add_layer(self._heatmap)
        return fig

    def _render_controls(self, initial_year):
        self._slider = widgets.IntSlider(
            value=initial_year,
            min=min(self._df['year']),
            max=max(self._df['year']),
            description='Year',
            continuous_update=False
        )
        self._total_box = widgets.Label(
            value=self._total_casualties_text_for_year(initial_year)
        )
        self._slider.observe(self._on_year_change, names='value')
        controls = widgets.HBox(
            [self._slider, self._total_box],
            layout={'justify_content': 'space-between'}
        )
        return controls

    def _locations_for_year(self, year):
        return self._df[self._df['year'] == year][['latitude', 'longitude']]

    def _total_casualties_for_year(self, year):
        return int(self._df[self._df['year'] == year]['year'].count())

    def _total_casualties_text_for_year(self, year):
        return '{} civilian casualties'.format(self._total_casualties_for_year(year))


class OutletExplorer(object):

    def __init__(self, df):
        """
        Jupyter widget for exploring KFC and Starbucks outlets

        Using checkboxes, the user chooses whether to include
        Starbucks, KFC outlets, both or neither.
        """
        self._df = df
        self._symbol_layer = None

        self._starbucks_symbols = self._create_symbols_for_chain(
            'starbucks', 'rgba(0, 150, 0, 0.4)')
        self._kfc_symbols = self._create_symbols_for_chain(
            'kfc', 'rgba(150, 0, 0, 0.4)')

        title_widget = widgets.HTML(
            '<h3>Explore KFC and Starbucks locations</h3>'
            '<h4>Data from <a href="http://ratings.food.gov.uk">UK Food Standards Agency</a></h4>'
        )
        controls = self._render_controls(True, True)
        map_figure = self._render_map(True, True)
        self._container = widgets.VBox(
            [title_widget, controls, map_figure])

    def render(self):
        """ Render the widget """
        display(self._container)

    def _render_map(self, initial_include_starbucks, initial_include_kfc):
        """ Render the initial map """
        fig = gmaps.figure(layout={'height': '500px'})
        symbols = self._generate_symbols(True, True)
        self._symbol_layer = gmaps.Markers(markers=symbols)
        fig.add_layer(self._symbol_layer)
        return fig

    def _render_controls(
            self,
            initial_include_starbucks,
            initial_include_kfc
    ):
        """ Render the checkboxes """
        self._starbucks_checkbox = widgets.Checkbox(
            value=initial_include_starbucks,
            description='Starbucks'
        )
        self._kfc_checkbox = widgets.Checkbox(
            value=initial_include_kfc,
            description='KFC'
        )
        self._starbucks_checkbox.observe(
            self._on_controls_change, names='value')
        self._kfc_checkbox.observe(
            self._on_controls_change, names='value')
        controls = widgets.VBox(
            [self._starbucks_checkbox, self._kfc_checkbox])
        return controls

    def _on_controls_change(self, obj):
        """
        Called when the checkboxes change

        This method builds the list of symbols to include on the map,
        based on the current checkbox values. It then updates the
        symbol layer with the new symbol list.
        """
        include_starbucks = self._starbucks_checkbox.value
        include_kfc = self._kfc_checkbox.value
        symbols = self._generate_symbols(
            include_starbucks, include_kfc)
        # Update the layer with the new symbols:
        self._symbol_layer.markers = symbols

    def _generate_symbols(self, include_starbucks, include_kfc):
        """ Generate the list of symbols to includs """
        symbols = []
        if include_starbucks:
            symbols.extend(self._starbucks_symbols)
        if include_kfc:
            symbols.extend(self._kfc_symbols)
        return symbols

    def _create_symbols_for_chain(self, chain, color):
        chain_df = self._df[self._df['chain_name'] == chain]
        symbols = [
            gmaps.Symbol(
                location=(latitude, longitude),
                stroke_color=color,
                fill_color=color,
                scale=2
            )
            for latitude, longitude in
            zip(chain_df["latitude"], chain_df["longitude"])
        ]
        return symbols