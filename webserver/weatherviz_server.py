# a server for the weatherviz app

# See: https://docs.graphene-python.org/en/latest/quickstart/
import graphene
import json


class WeatherMeasureType(graphene.ObjectType):
    datetime = graphene.Int()
    temp_day = graphene.Float()
    pressure = graphene.Float()
    humidity = graphene.Int()
    weather = graphene.String()
    clouds = graphene.Int()
    rain = graphene.Float()
    uvi = graphene.Float()


class GeoCoordType(graphene.ObjectType):
    lon = graphene.Float()
    lat = graphene.Float()


class CityType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    country = graphene.String()
    coord = graphene.Field(GeoCoordType)
    weather_data = graphene.Field(
        graphene.List(WeatherMeasureType),
    )

    def resolve_weather_data(self, info, **kwargs):
        for d in self._weather_data:
            yield WeatherMeasureType(
                datetime=d['dt'],
                temp_day=d['temp']['day'],
                pressure=d['pressure'],
                weather=d['weather'][0]['main'],
                rain=d.get('rain'),
                # TODO moarrrr!
            )


class Query(graphene.ObjectType):
    city = graphene.Field(
        graphene.List(CityType),
        # some pagination
        limit=graphene.Int(),
        offset=graphene.Int(),
        # filtering
        name=graphene.String(),
    )

    def resolve_city(self, info, name=None, limit=None, offset=0, **kwargs):
        with open("daily_14.json") as jsonl_file:
            import itertools
            lines = itertools.islice(jsonl_file, offset, offset + limit)
            for line in lines:
                try:
                    d = json.loads(line.strip())
                    city_d = d['city']
                    # TODO name filter
                    obj = CityType(
                        id=d['city']['id'],
                        name=d['city']['name'],
                        country=d['city']['country'],
                        coord=GeoCoordType(**d['city']['coord']),
                    )
                    obj._weather_data = d['data']
                    yield obj
                except Exception as e:
                    import sys
                    print(f'{e}: {line}', file=sys.stderr)

schema = graphene.Schema(query=Query)


# See: https://github.com/graphql-python/flask-graphql
import flask
from flask_graphql import GraphQLView

app = flask.Flask(__name__)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
))

# Optional, for adding batch query support (used in Apollo-Client)
app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view(
    'graphql-batch',
    schema=schema,
    batch=True,
))

@app.route('/')
def landing():
    return flask.redirect(flask.url_for('graphql', query='''\
query {
  city(limit:3, offset: 1234) {
    id
    name
    country
    coord {
      lon
      lat
    }
    weatherData {
      tempDay
      rain
    }
  }
}
'''))

if __name__ == '__main__':
    app.run()
