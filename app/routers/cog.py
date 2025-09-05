from titiler.core.factory import TilerFactory

# COG tiler router
cog_tiler = TilerFactory(router_prefix="/cog", path_dependency=lambda url: url)
router = cog_tiler.router
