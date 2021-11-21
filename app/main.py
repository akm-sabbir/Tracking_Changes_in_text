import logging.config
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import app_base_path
from app.exception.exception_handler import ExceptionHandler
from app.router import routers_base_path
from app.util.config_manager import ConfigManager
from app.util.import_util import ImportUtil
from app.Settings import Settings


app = FastAPI()
#allow cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
ConfigManager.initiate_config()
ExceptionHandler.initiate_exception_handlers(app)
__dx_threshold = ConfigManager.get_specific_config(section="entity_threshold", key="dx_threshold")
Settings.set_settings_dx_threshold(dx_threshold=float(__dx_threshold))

__icd10_threshold = ConfigManager.get_specific_config(section="icd10cm_threshold", key="icd10_threshold")
Settings.set_settings_icd10_threshold(icd_threshold=float(__icd10_threshold))

__parent_threshold = ConfigManager.get_specific_config(section="parents_threshold", key="parent_threshold")
Settings.set_settings_parent_threshold(p_threshold=float(__parent_threshold))

__caching_usage = ConfigManager.get_specific_config(section="caching_facility", key="use_cache")
Settings.set_settings_use_cache(caching=bool(__caching_usage))
# add routers

__router_modules = ImportUtil.import_modules_from_directory_as_list(routers_base_path)
for router_module in __router_modules:
    app.include_router(router_module.router, prefix=router_module.prefix)

# initiate logging
logging_folder = ConfigManager.get_specific_config(section="logging", key="folder")

__exclusion_list_folder = ConfigManager.get_specific_config(section="exclusion", key="list_")
exclusion_list_ = os.path.join(os.path.join(os.path.dirname(app_base_path), __exclusion_list_folder), "exclusions.json")
Path(os.path.join(os.path.dirname(app_base_path), logging_folder)).mkdir(exist_ok=True)

Settings.set_exclusion_dict(path_=exclusion_list_)

Settings.start_initialize_dictionary()

logging_config_file_path = os.path.join(os.path.dirname(app_base_path), 'logging.ini')
logging.config.fileConfig(logging_config_file_path,
                          defaults={'date': datetime.now().strftime('%Y-%m-%d-%H-%M-%S')},
                          # specifies value for %(date)s in logging.ini file
                          disable_existing_loggers=False)