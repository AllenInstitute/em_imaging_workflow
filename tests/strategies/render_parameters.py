from argschema.fields import Bool, Float, Int, Nested, Str, InputDir
from argschema.schemas import DefaultSchema
from render_module import RenderParameters


class SIFTPointMatchClientParameters(DefaultSchema):
    owner = Str(
        required=True,
        description="Point match collection owner")
    collection = Str(
        required=True,
        description="Name of point match collection to save point matches")
    pairJson = Str(
        required=True,
        description="Full path to the input tile pair json file")
    SIFTfdSize = Int(
        required=False,
        default=8,
        description="SIFT feature descriptor size: how many samples per row and column")
    SIFTsteps = Int(
        required=False,
        default=3,
        description="SIFT steps per scale octave")
    matchMaxEpsilon = Float(
        required=False,
        default=20.0,
        description="Minimal allowed transfer error for match filtering")
    maxFeatureCacheGb = Int(
        required=False,
        default=15,
        description="Maximum memory (in Gb) for caching SIFT features")
    SIFTminScale = Float(
        required=False,
        default=0.38,
        description="SIFT minimum scale: minSize * minScale < size < maxSize * maxScale")
    SIFTmaxScale = Float(
        required=False,
        default=0.82,
        description="SIFT maximum scale: minSize * minScale < size < maxSize * maxScale")
    renderScale = Float(
        required=False,
        default=0.3,
        description="Render canvases at this scale")
    matchRod = Float(
        required=False,
        default=0.92,
        description="Ratio of distances for matches")
    matchMinInlierRatio = Float(
        required=False,
        default=0.0,
        description="Minimal ratio of inliers to candidates for match filtering")
    matchMinNumInliers = Int(
        required=False,
        default=8,
        description="Minimal absolute number of inliers for match filtering")
    matchMaxNumInliers = Int(
        required=False,
        default=200,
        description="Maximum number of inliers for match filtering")

class PointMatchClientParameters(RenderParameters):
    sparkhome = Str(
        required=False,
        default="/allen/aibs/shared/image_processing/volume_assembly/utils/spark",
        description="Path to the spark home directory")
    logdir = Str(
        required=False,
        default="/allen/aibs/shared/image_processing/volume_assembly/logs/spark_logs",
        description="Directory to store spark logs")
    jarfile = Str(
        required=True,
        description="Full path to the spark point match client jar file")
    SIFTParameters = Nested(SIFTPointMatchClientParameters)
