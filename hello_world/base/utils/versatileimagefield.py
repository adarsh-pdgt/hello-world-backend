# Standard Library
import logging

# Third Party Stuff
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

logger = logging.getLogger(__name__)


def warm_images(instance, rendition_key_set="default_image_sizes", image_attr="image"):
    image_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set=rendition_key_set,
        image_attr=image_attr,
    )
    num_created, failed_to_create = image_warmer.warm()

    logger.info(
        "Pre-warming: no. of images pre-warmed successfully: %s, "
        "no. of images failed to pre-warm: %s, "
        "id of image: %s, "
        "model class: %s",
        num_created,
        len(failed_to_create),
        instance.id,
        type(instance).__name__,
    )
