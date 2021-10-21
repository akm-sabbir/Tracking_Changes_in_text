class Settings:
    app_name: str = "HCC API"
    dx_threshold: float
    parent_threshold: float
    icd10_threshold: float
    use_cache: bool

    @staticmethod
    def get_settings_dx_threshold() -> float:
        return Settings.dx_threshold

    @staticmethod
    def set_settings_dx_threshold(dx_threshold: float):
        Settings.dx_threshold = dx_threshold

    @staticmethod
    def get_settings_parent_threshold() -> float:
        return Settings.parent_threshold

    @staticmethod
    def set_settings_parent_threshold(p_threshold: float):
        Settings.parent_threshold = p_threshold

    @staticmethod
    def get_settings_use_cache() -> float:
        return Settings.use_cache

    @staticmethod
    def set_settings_use_cache(caching: bool):
        Settings.use_cache = caching

    @staticmethod
    def get_settings_icd10_threshold() -> float:
        return Settings.icd10_threshold

    @staticmethod
    def set_settings_icd10_threshold(icd_threshold: float):
        Settings.icd10_threshold = icd_threshold