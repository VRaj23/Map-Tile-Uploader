class SelectedParameters:
    state_id = None
    map_type = None
    crop_id = None
    year = None
    season_id = None

    def __init__(self, crop_id, year):
        self.crop_id = crop_id
        self.year = year

    def __str__(self):
        return "crop_id = "+str(self.crop_id)+", year = "+str(self.year)
