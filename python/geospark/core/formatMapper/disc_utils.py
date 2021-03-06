from enum import Enum

from pyspark import SparkContext

from geospark.core.SpatialRDD import SpatialRDD, PolygonRDD, LineStringRDD, PointRDD
from geospark.core.jvm.translate import SpatialObjectLoaderAdapter
from geospark.utils.decorators import require


class DiscLoader:

    @classmethod
    def load(cls, sc: SparkContext, path: str) -> SpatialRDD:
        raise NotImplementedError()


class IndexDiscLoader:

    @classmethod
    def load(cls, sc: SparkContext, path: str):
        jvm = sc._jvm
        index_rdd = SpatialObjectLoaderAdapter(jvm).load_index_rdd(sc._jsc, path)
        return index_rdd


class PolygonRDDDiscLoader(DiscLoader):

    @classmethod
    @require(["SpatialObjectLoaderAdapter"])
    def load(cls, sc: SparkContext, path: str) -> SpatialRDD:
        jvm = sc._jvm
        polygon_rdd = PolygonRDD()
        srdd = SpatialObjectLoaderAdapter(jvm).load_polygon_spatial_rdd(sc._jsc, path)
        polygon_rdd.set_srdd(srdd)
        return polygon_rdd


class PointRDDDiscLoader(DiscLoader):

    @classmethod
    @require(["SpatialObjectLoaderAdapter"])
    def load(cls, sc: SparkContext, path: str) -> SpatialRDD:
        jvm = sc._jvm
        polygon_rdd = PointRDD()
        srdd = SpatialObjectLoaderAdapter(jvm).load_point_spatial_rdd(sc._jsc, path)
        polygon_rdd.set_srdd(srdd)
        return polygon_rdd


class LineStringRDDDiscLoader(DiscLoader):

    @classmethod
    @require(["SpatialObjectLoaderAdapter"])
    def load(cls, sc: SparkContext, path: str) -> SpatialRDD:
        jvm = sc._jvm
        line_string_rdd = LineStringRDD()
        srdd = SpatialObjectLoaderAdapter(jvm).load_line_string_spatial_rdd(sc._jsc, path)
        line_string_rdd.set_srdd(srdd)
        return line_string_rdd


class SpatialRDDDiscLoader(DiscLoader):

    @classmethod
    @require(["SpatialObjectLoaderAdapter"])
    def load(cls, sc: SparkContext, path: str) -> SpatialRDD:
        jvm = sc._jvm
        spatial_rdd = SpatialRDD()
        srdd = SpatialObjectLoaderAdapter(jvm).load_spatial_rdd(sc._jsc, path)
        spatial_rdd.set_srdd(srdd)
        return spatial_rdd


class GeoType(Enum):
    POINT = "POINT"
    POLYGON = "POLYGON"
    LINESTRING = "LINESTRING"
    GEOMETRY = "GEOMETRY"


loaders = {
    GeoType.POINT: PointRDDDiscLoader,
    GeoType.POLYGON: PolygonRDDDiscLoader,
    GeoType.LINESTRING: LineStringRDDDiscLoader,
    GeoType.GEOMETRY: SpatialRDDDiscLoader
}


def load_spatial_rdd_from_disc(sc: SparkContext, path: str, geometry_type: GeoType):
    """

    :param sc:
    :param path:
    :param geometry_type:
    :return:
    """
    return loaders[geometry_type].load(sc, path)


def load_spatial_index_rdd_from_disc(sc: SparkContext, path: str):

    return IndexDiscLoader.load(sc, path)